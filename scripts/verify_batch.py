import hashlib, io, json, shutil, sys, tarfile
from pathlib import Path
def read_ar(data):
    if not data.startswith(b"!<arch>\n"): raise ValueError("not ar")
    pos, out = 8, {}
    while pos + 60 <= len(data):
        h = data[pos:pos+60]
        name = h[0:16].decode("utf-8","replace").strip().rstrip("/")
        size = int(h[48:58].decode("ascii").strip())
        out[name] = data[pos+60:pos+60+size]
        pos += 60 + size
        if pos % 2: pos += 1
    return out
def decomp(b,n):
    if n.endswith(".gz"): return __import__("gzip").decompress(b)
    if n.endswith(".xz"): return __import__("lzma").decompress(b)
    if n.endswith(".bz2"): return __import__("bz2").decompress(b)
    return b
def control(path):
    m = read_ar(Path(path).read_bytes())
    cn = next((n for n in m if n.startswith("control.tar")), None)
    if not cn: raise ValueError("no control.tar")
    with tarfile.open(fileobj=io.BytesIO(decomp(m[cn], cn)), mode="r:*") as tf:
        mem = next((x for x in tf.getmembers() if x.name.lstrip("./") == "control"), None)
        return tf.extractfile(mem).read().decode("utf-8","replace")
def parse(t):
    f,k={},None
    for line in t.splitlines():
        if line[:1] in (" ","\t") and k: f[k]+=" "+line.strip(); continue
        if ":" in line:
            k,v=line.split(":",1); f[k.strip()]=v.strip()
    return f
src=Path(sys.argv[1]); pool=Path(sys.argv[2]); meta=json.load(open(sys.argv[3],encoding="utf-8-sig"))
added=[]; bad=[]
for deb in sorted(src.glob("*.deb")):
    if deb.name.startswith("jellyfish"): continue
    try:
        data = deb.read_bytes()
        if not data: bad.append((deb.name,"empty")); continue
        c = parse(control(deb))
        exp = (meta.get(deb.name,{}).get("sha256") or "").lower()
        sha = hashlib.sha256(data).hexdigest()
        if exp and sha != exp: bad.append((deb.name,"sha mismatch")); continue
        if c.get("Architecture") not in ("iphoneos-arm","all"): bad.append((deb.name,"arch "+str(c.get("Architecture")))); continue
        dest = pool/deb.name
        if dest.exists(): bad.append((deb.name,"already in pool")); continue
        shutil.copy2(deb,dest)
        added.append({"package":c.get("Package"),"name":c.get("Name"),"version":c.get("Version"),
                      "arch":c.get("Architecture"),"file":deb.name,"size":len(data),"sha256":sha,
                      "depends":c.get("Depends"),"section":c.get("Section"),"author":c.get("Author")})
    except Exception as e:
        bad.append((deb.name,str(e)[:60]))
print(json.dumps({"added":len(added),"failed":len(bad)},indent=1))
for b in bad: print(" !",b)
json.dump(added, open(sys.argv[4],"w",encoding="utf-8"), indent=1, ensure_ascii=False)
