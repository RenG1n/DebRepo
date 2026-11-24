import hashlib, json, os, subprocess, sys, time

JOBS = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
CHUNK = 20000
TMP = os.path.join(os.environ.get("TEMP", "."), "_chunk.bin")

def grab(url, start, end):
    if os.path.exists(TMP):
        try: os.remove(TMP)
        except OSError: pass
    p = subprocess.run(["curl.exe", "-sS", "-L", "--max-time", "40",
                        "-r", f"{start}-{end}", "-o", TMP, url],
                       capture_output=True, timeout=60)
    if not os.path.exists(TMP):
        return b""
    with open(TMP, "rb") as f:
        return f.read()

for job in JOBS:
    name, url, total, sha = job["file"], job["url"], int(job["size"]), (job.get("sha256") or "").lower()
    dest = os.path.join(OUT, name)
    have = os.path.getsize(dest) if os.path.exists(dest) else 0
    if have > total:
        os.remove(dest); have = 0
    t0 = time.time(); pos = have; stall = 0
    f = open(dest, "ab")
    ok = True
    while pos < total:
        end = min(pos + CHUNK - 1, total - 1)
        data = grab(url, pos, end)
        if not data:
            stall += 1
            if stall >= 5:
                ok = False; break
            time.sleep(1); continue
        f.write(data); f.flush(); pos += len(data); stall = 0
    f.close()
    h = hashlib.sha256(open(dest, "rb").read()).hexdigest() if os.path.exists(dest) else ""
    st = "OK" if (pos == total and (not sha or h == sha)) else ("PARTIAL" if pos < total else "SHA_MISMATCH")
    print(f"{job['id']:32s} {pos:>9}/{total:<9} {st:11s} {time.time()-t0:5.1f}s", flush=True)
print("DONE", flush=True)
