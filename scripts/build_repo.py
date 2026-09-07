#!/usr/bin/env python3
from pathlib import Path
import gzip, hashlib, io, tarfile, time

ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / "pool"

def read_ar(path):
    data = path.read_bytes()
    if not data.startswith(b"!<arch>\n"):
        raise ValueError("not a Debian ar archive")
    pos = 8
    out = {}
    while pos + 60 <= len(data):
        header = data[pos:pos+60]
        name = header[0:16].decode("utf-8", "replace").strip().rstrip("/")
        size = int(header[48:58].decode("ascii").strip())
        body = data[pos+60:pos+60+size]
        out[name] = body
        pos += 60 + size
        if pos % 2:
            pos += 1
    return out

def decompress_control(data, name):
    if name.endswith(".gz"):
        import gzip
        return gzip.decompress(data)
    if name.endswith(".xz"):
        import lzma
        return lzma.decompress(data)
    if name.endswith(".bz2"):
        import bz2
        return bz2.decompress(data)
    if name.endswith(".zst"):
        # Ubuntu runner normally has zstd; Python stdlib does not.
        import subprocess
        p = subprocess.run(["zstd", "-d", "-q", "-c"], input=data,
                           stdout=subprocess.PIPE, check=True)
        return p.stdout
    return data

def get_control(deb):
    members = read_ar(deb)
    control_name = next((n for n in members if n.startswith("control.tar")), None)
    if not control_name:
        raise ValueError("control.tar.* missing")
    tar_data = decompress_control(members[control_name], control_name)
    with tarfile.open(fileobj=io.BytesIO(tar_data), mode="r:*") as tf:
        member = next((m for m in tf.getmembers()
                       if m.name.lstrip("./") == "control"), None)
        if not member:
            raise ValueError("DEBIAN/control missing")
        return tf.extractfile(member).read().decode("utf-8", "replace").strip()

def parse_control(text):
    fields = {}
    key = None
    for line in text.splitlines():
        if line.startswith((" ", "\t")) and key:
            fields[key] += "\n" + line
        elif ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            fields[key] = value.strip()
    return fields

def digest(path, algo):
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

entries = []
for deb in sorted(POOL.glob("*.deb")):
    try:
        fields = parse_control(get_control(deb))
        required = ["Package", "Version", "Architecture"]
        missing = [x for x in required if x not in fields]
        if missing:
            raise ValueError("missing fields: " + ", ".join(missing))

        lines = []
        # Preserve all fields from control, excluding fields we generate.
        for k, v in fields.items():
            if k not in {"Filename", "Size", "MD5sum", "SHA1", "SHA256", "SHA512"}:
                lines.append(f"{k}: {v}")

        lines.extend([
            f"Filename: ./pool/{deb.name}",
            f"Size: {deb.stat().st_size}",
            f"MD5sum: {digest(deb, 'md5')}",
            f"SHA1: {digest(deb, 'sha1')}",
            f"SHA256: {digest(deb, 'sha256')}",
            f"SHA512: {digest(deb, 'sha512')}",
        ])
        entries.append("\n".join(lines))
        print(f"Indexed: {deb.name}")
    except Exception as e:
        print(f"WARNING: {deb.name}: {e}")

packages = "\n\n".join(entries)
if packages:
    packages += "\n"

(ROOT / "Packages").write_text(packages, encoding="utf-8", newline="\n")
with gzip.open(ROOT / "Packages.gz", "wb", compresslevel=9) as f:
    f.write(packages.encode("utf-8"))

release = [
    "Origin: DebRepo",
    "Label: DebRepo",
    "Suite: stable",
    "Codename: stable",
    "Architectures: iphoneos-arm iphoneos-arm64",
    "Components: main",
    "Description: DebRepo jailbreak repository by RenG1n",
    f"Date: {time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.gmtime())}",
    "",
]

for algo, title in [("md5", "MD5Sum:"), ("sha256", "SHA256:"), ("sha512", "SHA512:")]:
    release.append(title)
    for name in ("Packages", "Packages.gz"):
        p = ROOT / name
        release.append(f" {digest(p, algo)} {p.stat().st_size:16d} {name}")

(ROOT / "Release").write_text("\n".join(release) + "\n",
                             encoding="utf-8", newline="\n")

print(f"Done: {len(entries)} package(s) indexed.")
