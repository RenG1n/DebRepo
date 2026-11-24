import json, hashlib, os, sys, time, urllib.request
TARGET = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
STEP = 32768

def get(url, headers, tries=2, timeout=45):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e; time.sleep(1)
    raise last

for pid, meta in sorted(TARGET.items()):
    name = (meta.get("filename") or meta["url"].split("/")[-1]).split("/")[-1]
    dest = os.path.join(OUT, name)
    exp = (meta.get("sha256") or "").lower()
    if os.path.exists(dest):
        h = hashlib.sha256(open(dest, "rb").read()).hexdigest()
        if not exp or h == exp:
            print(f"{pid:42s} SKIP", flush=True); continue
    try:
        buf = bytearray(); pos = 0
        while True:
            c = get(meta["url"], {"Range": f"bytes={pos}-{pos+STEP-1}", "User-Agent": "DebRepo/1.0"})
            if not c: break
            buf.extend(c); pos = len(buf)
            if len(c) < STEP: break
            if len(buf) > 4_000_000: break
        open(dest, "wb").write(bytes(buf))
        h = hashlib.sha256(bytes(buf)).hexdigest()
        st = "OK" if (not exp or h == exp) else "SHA_MISMATCH"
        print(f"{pid:42s} {len(buf):>8} {st}", flush=True)
    except Exception as e:
        print(f"{pid:42s} ERROR {str(e)[:60]}", flush=True)
print("DONE", flush=True)
