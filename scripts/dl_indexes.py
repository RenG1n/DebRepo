#!/usr/bin/env python3
import os, sys, time, urllib.request, urllib.error

TARGETS = [
    ("chariz",   "https://repo.chariz.com/Packages"),
    ("sparkdev", "https://sparkdev.me/Packages"),
    ("havoc",    "https://havoc.app/Packages"),
    ("bigboss",  "http://apt.thebigboss.org/repofiles/cydia/dists/stable/main/binary-iphoneos-arm/Packages.bz2"),
]
OUT = sys.argv[1]
STEP = 20000

def fetch(url, start, end, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}",
                                                       "User-Agent": "DebRepo-Catalog/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
                cr = r.headers.get("Content-Range")
                total = None
                if cr and "/" in cr:
                    t = cr.split("/")[-1]
                    total = int(t) if t.isdigit() else None
                return data, total
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(1)
    raise RuntimeError("unreachable")

def download(name, url):
    path = os.path.join(OUT, name + ".index")
    data0, total = fetch(url, 0, STEP - 1)
    buf = bytearray(data0)
    if total and len(buf) >= total:
        open(path, "wb").write(buf)
        print(f"{name}: {len(buf)}/{total} (single chunk)", flush=True)
        return
    pos = len(buf)
    while total is None or pos < total:
        try:
            chunk, t2 = fetch(url, pos, pos + STEP - 1)
        except Exception as e:
            print(f"{name}: FAILED at {pos}: {e}", flush=True)
            break
        if not chunk:
            break
        if t2:
            total = t2
        buf.extend(chunk)
        pos = len(buf)
    open(path, "wb").write(buf)
    print(f"{name}: {len(buf)}/{total}", flush=True)

for n, u in TARGETS:
    try:
        download(n, u)
    except Exception as e:
        print(f"{n}: ERROR {e}", flush=True)
print("CHUNK_ALL_DONE", flush=True)
