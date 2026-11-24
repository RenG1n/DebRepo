import hashlib, json, os, subprocess, sys, time
JOBS = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(os.environ.get("TEMP", "."), "_dl.bin")

for job in JOBS:
    name = job["file"]; dest = os.path.join(OUT, name)
    if os.path.exists(dest) and os.path.getsize(dest) == int(job["size"]):
        print(f"{job['id']:40s} SKIP", flush=True); continue
    if os.path.exists(dest):
        os.remove(dest)
    if os.path.exists(TMP):
        try: os.remove(TMP)
        except OSError: pass
    r = subprocess.run(["curl.exe", "-sS", "-L", "--max-time", "240", "-o", TMP, job["url"]],
                       capture_output=True, timeout=280)
    if not os.path.exists(TMP):
        print(f"{job['id']:40s} FAIL no file", flush=True); continue
    size = os.path.getsize(TMP)
    if size != int(job["size"]):
        print(f"{job['id']:40s} SIZE {size} != {job['size']}", flush=True); continue
    os.replace(TMP, dest)
    h = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    exp = (job.get("sha256") or "").lower()
    print(f"{job['id']:40s} OK {size:>8} {'sha-ok' if (not exp or h == exp) else 'SHA-MISMATCH'}", flush=True)
print("DONE", flush=True)
