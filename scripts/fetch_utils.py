import hashlib, json, os, subprocess, sys, time
JOBS = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(os.environ.get("TEMP","."), "_u.bin"); CH = os.path.join(os.environ.get("TEMP","."), "_uc.bin")

def plain(url, dest):
    if os.path.exists(TMP):
        try: os.remove(TMP)
        except OSError: pass
    subprocess.run(["curl.exe","-sS","-L","--max-time","300","-o",TMP,url], capture_output=True, timeout=340)
    return os.path.getsize(TMP) if os.path.exists(TMP) else 0

def chunked(url, dest, total):
    buf = bytearray()
    if os.path.exists(dest) and 0 < os.path.getsize(dest) < total:
        buf = bytearray(open(dest,"rb").read())
    pos = len(buf); stall = 0
    while pos < total:
        end = min(pos + 20000 - 1, total - 1)
        if os.path.exists(CH):
            try: os.remove(CH)
            except OSError: pass
        try:
            subprocess.run(["curl.exe","-sS","-L","--max-time","40","-r",f"{pos}-{end}","-o",CH,url],
                           capture_output=True, timeout=55)
        except Exception:
            pass
        data = open(CH,"rb").read() if os.path.exists(CH) else b""
        if not data:
            stall += 1
            if stall >= 6: break
            time.sleep(1); continue
        buf.extend(data); pos = len(buf); stall = 0
        open(dest,"wb").write(bytes(buf))
    return pos

for j in JOBS:
    dest = os.path.join(OUT, j["file"]); total = int(j["size"]); t0 = time.time()
    if os.path.exists(dest) and os.path.getsize(dest) == total:
        print(f"{j['id']:34s} SKIP", flush=True); continue
    if j["repo"] in ("havoc", "chariz"):
        size = chunked(j["url"], dest, total)
    else:
        size = plain(j["url"], dest)
        if size and os.path.exists(TMP):
            os.replace(TMP, dest)
    have = os.path.getsize(dest) if os.path.exists(dest) else 0
    h = hashlib.sha256(open(dest,"rb").read()).hexdigest() if have else ""
    exp = (j.get("sha256") or "").lower()
    st = "OK" if (have == total and (not exp or h == exp)) else ("PARTIAL" if have != total else "SHA_MISMATCH")
    print(f"{j['id']:34s} {have:>9}/{total:<9} {st:11s} {time.time()-t0:5.1f}s", flush=True)
print("DONE", flush=True)
