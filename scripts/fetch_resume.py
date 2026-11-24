import hashlib, json, os, sys, time, urllib.request, urllib.error

JOBS = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)

def fetch(url, start, end, timeout=25, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "Range": f"bytes={start}-{end}",
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_8 like Mac OS X) AppleWebKit/605.1.15",
                "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 404):
                raise
            last = e; time.sleep(1)
        except Exception as e:
            last = e; time.sleep(1)
    raise last

def download(url, dest, total, step=32768):
    have = os.path.getsize(dest) if os.path.exists(dest) else 0
    if have > total:
        os.remove(dest); have = 0
    if have == total:
        return have
    f = open(dest, "ab")
    pos = have
    stall = 0
    while pos < total:
        end = min(pos + step - 1, total - 1)
        try:
            chunk = fetch(url, pos, end)
        except Exception as e:
            print(f"    chunk fail at {pos}: {str(e)[:40]}", flush=True)
            stall += 1
            if stall >= 6: raise RuntimeError("stalled")
            time.sleep(2); continue
        if not chunk:
            stall += 1
            if stall >= 6: raise RuntimeError("empty")
            continue
        f.write(chunk); f.flush(); pos += len(chunk); stall = 0
    f.close()
    return pos

results = []
for job in JOBS:
    name, url, total, sha = job["file"], job["url"], int(job["size"]), job.get("sha256", "").lower()
    dest = os.path.join(OUT, name)
    t0 = time.time()
    try:
        size = download(url, dest, total)
        h = hashlib.sha256(open(dest, "rb").read()).hexdigest()
        st = "OK" if (not sha or h == sha) else "SHA_MISMATCH"
        results.append((job["id"], name, size, st))
        print(f"{job['id']:34s} {size:>9}/{total:<9} {st:12s} {time.time()-t0:5.1f}s", flush=True)
    except Exception as e:
        results.append((job["id"], name, 0, "FAIL " + str(e)[:40]))
        print(f"{job['id']:34s} FAIL {str(e)[:60]}  {time.time()-t0:5.1f}s", flush=True)
print("DONE", flush=True)
