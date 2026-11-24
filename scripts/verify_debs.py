#!/usr/bin/env python3
"""Verify downloaded DEBs (structure + checksum) and copy them into pool/."""
import hashlib, io, json, os, shutil, sys, tarfile
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

def read_ar(data):
    if not data.startswith(b"!<arch>\n"):
        raise ValueError("not an ar archive")
    pos, out = 8, {}
    while pos + 60 <= len(data):
        hdr = data[pos:pos+60]
        name = hdr[0:16].decode("utf-8", "replace").strip().rstrip("/")
        size = int(hdr[48:58].decode("ascii").strip())
        out[name] = data[pos+60:pos+60+size]
        pos += 60 + size
        if pos % 2: pos += 1
    return out

def decomp(b, n):
    if n.endswith(".gz"): return __import__("gzip").decompress(b)
    if n.endswith(".xz"): return __import__("lzma").decompress(b)
    if n.endswith(".bz2"): return __import__("bz2").decompress(b)
    return b

def control_of(path):
    members = read_ar(Path(path).read_bytes())
    cn = next((n for n in members if n.startswith("control.tar")), None)
    if not cn: raise ValueError("no control.tar")
    with tarfile.open(fileobj=io.BytesIO(decomp(members[cn], cn)), mode="r:*") as tf:
        m = next((x for x in tf.getmembers() if x.name.lstrip("./") == "control"), None)
        if not m: raise ValueError("no control file")
        return tf.extractfile(m).read().decode("utf-8", "replace")

def parse(text):
    f, k = {}, None
    for line in text.splitlines():
        if line[:1] in (" ", "\t") and k: f[k] += " " + line.strip(); continue
        if ":" in line:
            k, v = line.split(":", 1); k = k.strip(); f[k] = v.strip()
    return f

src = Path(sys.argv[1]); pool = Path(sys.argv[2]); meta = json.load(open(sys.argv[3], encoding="utf-8-sig"))
by_name = {}
for pid, m in meta.items():
    by_name[(m.get("filename") or m["url"].split("/")[-1]).split("/")[-1]] = (pid, m)

added, skipped, failed = [], [], []
for deb in sorted(src.glob("*.deb")):
    try:
        data = deb.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        c = parse(control_of(deb))
        pid = c.get("Package", "?")
        m = by_name.get(deb.name)
        exp = (m[1].get("sha256") or "").lower() if m else ""
        if exp and sha != exp:
            failed.append((deb.name, "SHA256 mismatch")); continue
        if c.get("Architecture") not in ("iphoneos-arm", "all"):
            skipped.append((deb.name, "arch " + str(c.get("Architecture")))); continue
        if not data:
            failed.append((deb.name, "empty")); continue
        dest = pool / deb.name
        if dest.exists():
            skipped.append((deb.name, "already in pool")); continue
        shutil.copy2(deb, dest)
        added.append({"package": pid, "version": c.get("Version"), "arch": c.get("Architecture"),
                      "file": deb.name, "size": len(data), "sha256": sha,
                      "depends": c.get("Depends"), "name": c.get("Name")})
    except Exception as e:
        failed.append((deb.name, str(e)[:100]))

print(json.dumps({"added": len(added), "skipped": len(skipped), "failed": len(failed)}, indent=1))
for a in added: print(" + %-42s v%-14s %8d  %s" % (a["package"], a["version"], a["size"], a["file"]))
for s in skipped: print(" = skipped:", s)
for f in failed: print(" ! failed:", f)
Path(sys.argv[4]).write_text(json.dumps(added, indent=1, ensure_ascii=False), encoding="utf-8")
