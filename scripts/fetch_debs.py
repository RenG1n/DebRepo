import json, hashlib, os, sys, time, urllib.request
TARGET = json.load(open(sys.argv[1], encoding="utf-8-sig"))
OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
STEP = 65536

def get(url, headers, tries=4, timeout=120):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last = e; time.sleep(1.5)
    raise last

def whole(url):
    return get(url, {"User-Agent": "DebRepo/1.0"})

def chunked(url):
    buf = bytearray(); pos = 0
    while True:
        c = get(url, {"Range": f"bytes={pos}-{pos+STEP-1}", "User-Agent": "DebRepo/1.0"})
        if not c: break
        buf.extend(c); pos = len(buf)
        if len(c) < STEP: break
    return bytes(buf)

ok = fail = skip = 0
for pid, meta in sorted(TARGET.items()):
    name = (meta.get("filename") or meta["url"].split("/")[-1]).split("/")[-1]
    dest = os.path.join(OUT, name)
    exp = (meta.get("sha256") or "").lower()
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        h = hashlib.sha256(open(dest, "rb").read()).hexdigest()
        if not exp or h == exp:
            print(f"{pid:45s} SKIP (already ok)", flush=True); skip += 1; continue
    try:
        data = whole(meta["url"]) if meta["repo"] == "bigboss" else chunked(meta["url"])
        open(dest, "wb").write(data)
        h = hashlib.sha256(data).hexdigest()
        st = "OK" if (not exp or h == exp) else "SHA_MISMATCH"
        print(f"{pid:45s} {len(data):>9} {st}", flush=True)
        ok += 1 if st == "OK" else 0
        fail += 0 if st == "OK" else 1
    except Exception as e:
        print(f"{pid:45s} ERROR {str(e)[:70]}", flush=True); fail += 1
print(json.dumps({"ok": ok, "fail": fail, "skip": skip}))
