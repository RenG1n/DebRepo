#!/usr/bin/env python3
"""Build a verified tweak catalog for DebRepo from real APT indexes.

Reads downloaded Packages indexes (plain, .gz, .bz2, .xz) and extracts
metadata only. It never downloads or republishes .deb payloads.
"""
import bz2, gzip, json, lzma, re, sys
from pathlib import Path

# name -> (category, search regex on Package/Name fields, notes)
TARGETS = [
    # A. Interface customization
    ("SnowBoard",            "Appearance",      r"snowboard",                 "SparkDev theming engine"),
    ("Cylinder",             "Animations",      r"^com\.rplus\.cylinder|^cylinder$", "rplus page animations"),
    ("Eclipse 12",           "Appearance",      r"eclipse",                   "dark mode"),
    ("Noctis12",             "Appearance",      r"noctis",                    "dark mode"),
    ("Jellyfish",            "LockScreen",      r"jellyfish",                 "lock screen clock"),
    ("Axon",                 "LockScreen",      r"(^|\.)axon($|\.)",          "grouped notifications"),
    ("Zenith",               "SpringBoard",     r"zenith",                    "app grid"),
    ("HuddyX",               "SpringBoard",     r"huddy",                     "HUD replacement"),
    ("Notifica",             "Notifications",   r"notifica",                  "notification redesign"),
    ("Shuffle",              "Appearance",      r"(^|\.)shuffle($|\.)",       "settings redesign"),
    ("BetterCCXI",           "ControlCenter",   r"bettercc",                  "CC modules"),
    ("Xen HTML",             "Appearance",      r"xenhtml|xen html",          "widget engine"),
    ("BadgeMeNot",           "Appearance",      r"badgeme",                   "badge control"),
    # B. System utilities
    ("Filza",                "Utilities",       r"filza",                     "file manager"),
    ("iCleaner Pro",         "Utilities",       r"icleaner",                  "cleaner"),
    ("Safari Plus",          "Safari",          r"safariplus",                "browser enhancements"),
    ("RealCC",               "ControlCenter",   r"realcc",                    "real CC toggles"),
    ("CopyLog",              "Utilities",       r"copylog",                   "clipboard history"),
    ("BioProtect XS",        "Security",        r"bioprotect",                "biometric app lock"),
    ("AutoUnlockX",          "Security",        r"autounlock",                "face id auto unlock"),
    # C. YouTube
    ("Cercube",              "YouTube",         r"cercube",                   "YouTube enhancement suite"),
    ("YouTubePatcher",       "YouTube",         r"youtubepatcher",            "patch-based YouTube mod"),
    ("YouTube Tools",        "YouTube",         r"youtubetools|youtube tools","Tomasz Poliszuk tools"),
    ("Youtubed",             "YouTube",         r"youtubed",                  "YouTube downloader"),
    # D. Instagram
    ("Rocket for Instagram", "Instagram",       r"rocket.*instagram|instagram.*rocket", "Majd Alfhaily"),
    ("InstagramPlus",        "Instagram",       r"instagramplus|instagram plus", "Instagram enhancer"),
    # E. Telegram
    ("BetterTelegram",       "Telegram",        r"bettertelegram",            "Telegram enhancer"),
    # F. TikTok
    ("TikTok God",           "TikTok",          r"tiktok",                    "TikTok enhancer"),
]

FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):\s?(.*)$")


def read_index(path: Path) -> str:
    data = path.read_bytes()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    elif data[:3] == b"BZh":
        data = bz2.decompress(data)
    elif data[:6] == b"\xfd7zXZ\x00":
        data = lzma.decompress(data)
    return data.decode("utf-8", "replace")


def parse_paragraphs(text: str):
    out, cur, key = [], {}, None
    for line in text.splitlines():
        if not line.strip():
            if cur:
                out.append(cur)
            cur, key = {}, None
            continue
        if line[0] in " \t" and key:
            cur[key] += "\n" + line.strip()
            continue
        m = FIELD_RE.match(line)
        if m:
            key = m.group(1)
            cur[key] = m.group(2).strip()
    if cur:
        out.append(cur)
    return out


def ver_tuple(s):
    return [int(x) for x in re.findall(r"\d+", s)[:3]] or [0]


def firmware_bounds(depends: str):
    lo = hi = None
    for kind, op, ver in re.findall(r"firmware\s*\(\s*(>=|<=|>>|<<|=)\s*([0-9.]+)\s*\)", depends):
        if op in (">=", ">>"):
            lo = ver if lo is None or ver_tuple(ver) > ver_tuple(lo) else lo
        elif op in ("<=", "<<", "="):
            hi = ver if hi is None or ver_tuple(ver) < ver_tuple(hi) else hi
    return lo, hi


def main():
    idx_dir = Path(sys.argv[1])
    repo_root = Path(sys.argv[2])
    indexes = {}
    for p in sorted(idx_dir.glob("*.index")):
        try:
            paras = parse_paragraphs(read_index(p))
            indexes[p.stem] = paras
            print(f"{p.stem}: {len(paras)} packages")
        except Exception as e:
            print(f"{p.stem}: SKIP {e}")

    found = {}
    for name, category, pattern, note in TARGETS:
        rx = re.compile(pattern, re.I)
        hits = []
        for repo, paras in indexes.items():
            for para in paras:
                hay = (para.get("Package", "") + " " + para.get("Name", ""))
                if rx.search(hay):
                    hits.append((repo, para))
        # prefer rootful iphoneos-arm builds, then newest version
        def score(item):
            repo, p = item
            arch = p.get("Architecture", "")
            rootful = 1 if arch == "iphoneos-arm" else 0
            return (rootful, ver_tuple(p.get("Version", "0")))
        hits.sort(key=score, reverse=True)
        found[name] = (category, note, hits[:20])

    print("\n=== MATCH SUMMARY ===")
    for name, (cat, note, hits) in found.items():
        print(f"{name:22s} {len(hits):3d} hits" + (f"  e.g. {hits[0][1].get('Package')}" if hits else "  NOT FOUND"))

    out = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({k: {"category": v[0], "note": v[1],
                                       "matches": [{"repo": r, "fields": p} for r, p in v[2]]}
                                   for k, v in found.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
        print("raw dump:", out)


if __name__ == "__main__":
    main()
