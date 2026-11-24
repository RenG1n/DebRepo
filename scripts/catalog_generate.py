#!/usr/bin/env python3
"""Generate DebRepo catalog + reports from real APT indexes.

Metadata only: no .deb payloads are downloaded or republished here.
"""
import bz2, gzip, json, lzma, re, sys, hashlib
from pathlib import Path

FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):\s?(.*)$")
BT = chr(96)

REPOS = {
    "bigboss":  ("BigBoss",  "http://apt.thebigboss.org/repofiles/cydia/"),
    "chariz":   ("Chariz",   "https://repo.chariz.com/"),
    "havoc":    ("Havoc",    "https://havoc.app/"),
    "poomsmart":("PoomSmart","https://poomsmart.github.io/repo/"),
    "sparkdev": ("SparkDev", "https://sparkdev.me/"),
    "bingner":  ("Bingner",  "https://apt.bingner.com/"),
}

MANDATORY = [
 ("SnowBoard","Appearance","com.spark.snowboard","Theming engine","https://sparkdev.me/"),
 ("Cylinder","Animations","com.r333d.cylinder","Original page-turn animations","http://apt.thebigboss.org/"),
 ("Cylinder Reborn","Animations","com.ryannair05.cylinder","Maintained Cylinder fork","https://repo.chariz.com/"),
 ("Eclipse 12","Appearance","com.gmoran.eclipse12","Dark mode (iOS 12)",""),
 ("Noctis12","Appearance","com.laughingquoll.noctis12","Dark mode (iOS 12)",""),
 ("Jellyfish","LockScreen","xyz.royalapps.jellyfish","Lock screen clock",""),
 ("Axon","LockScreen","com.baw.axon","Grouped notifications",""),
 ("Zenith","SpringBoard","com.muirey03.zenith","App grid",""),
 ("HuddyX","SpringBoard","com.maximehip.huddyx","HUD replacement",""),
 ("Notifica","Notifications","com.tomt000.notifica","Notification redesign",""),
 ("Shuffle","Appearance","com.ivancic.shuffle","Settings redesign",""),
 ("BetterCCXI","ControlCenter","com.ichitaso.betterccxi","CC modules",""),
 ("Xen HTML","Appearance","com.matchstic.xenhtml","Widget engine",""),
 ("BadgeMeNot","Appearance","com.ahmad.badgemenot","Badge control",""),
 ("Filza","Utilities","com.tigisoftware.filza","File manager","https://tigisoftware.com/"),
 ("iCleaner Pro","Utilities","org.altervista.exilecom.icleanerpro","System cleaner","https://ib-soft.net/"),
 ("iCleaner","Utilities","org.altervista.exilecom.icleaner","Free cleaner","https://ib-soft.net/"),
 ("Safari Plus","Safari","com.opa334.safariplus","Browser enhancements","https://opa334.github.io/"),
 ("RealCC","ControlCenter","com.jakeashacks.realcc","Real CC toggles",""),
 ("CopyLog","Utilities","me.tomt000.copylog","Clipboard history",""),
 ("BioProtect XS","Security","net.limneos.bioprotectxs","Biometric app lock (paid)","https://limneos.net/"),
 ("AutoUnlockX","Security","com.smartbear.autounlockx","Face ID auto unlock",""),
 ("Cercube","YouTube","com.cercube.ios","YouTube suite (paid)","https://cercube.com/"),
 ("YouTubePatcher","YouTube","com.cydiageek.youtubepatcher","YouTube patcher",""),
 ("YouTube Tools","YouTube","com.tomaszpoliszuk.youtubetools","YouTube tools",""),
 ("Youtubed","YouTube","com.tomaszpoliszuk.youtubed","YouTube downloader",""),
 ("Rocket for Instagram","Instagram","me.alfhaily.rocket","Instagram suite (paid)","https://rocketapp.me/"),
 ("InstagramPlus","Instagram","com.instagramplus.tweak","Instagram enhancer",""),
 ("BetterTelegram","Telegram","com.cydiageek.bettertelegram","Telegram enhancer",""),
 ("TikTok God","TikTok","com.cydiageek.tiktokgod","TikTok enhancer",""),
]

EXTRA_TOKENS = ["tiktok","youtube","instagram","telegram","snowboard","xenhtml","cylinder","badge",
                "notification","statusbar","battery","keyboard","safari","ccsupport","haptic",
                "gesture","theme","privacy","security","cleaner","filza","dock","lockscreen",
                "springboard","homescreen","wallpaper","volume","brightness","clipboard","passcode"]

BAD_SECTIONS = ("addon", "iconoclasm", "sbsettings", "flipswitch", "lockinfo", "ringtones")

GOOD_SECTIONS = ("tweaks", "themes", "utilities", "system", "appearance")

def read_index(p):
    d = p.read_bytes()
    if d[:2] == b"\x1f\x8b": d = gzip.decompress(d)
    elif d[:3] == b"BZh": d = bz2.decompress(d)
    elif d[:6] == b"\xfd7zXZ\x00": d = lzma.decompress(d)
    return d.decode("utf-8", "replace")

def paragraphs(text):
    out, cur, key = [], {}, None
    for line in text.splitlines():
        if not line.strip():
            if cur: out.append(cur)
            cur, key = {}, None
            continue
        if line[0] in " \t" and key:
            cur[key] += " " + line.strip()
            continue
        m = FIELD.match(line)
        if m:
            key = m.group(1); cur[key] = m.group(2).strip()
    if cur: out.append(cur)
    return out

def vt(s):
    return tuple(int(x) for x in re.findall(r"\d+", s)[:3]) or (0,)

def fw(dep):
    lo = hi = None
    for op, v in re.findall(r"firmware\s*\(?\s*(>=|<=|>>|<<|=)\s*([0-9.]+)", dep or ""):
        if op in (">=", ">>"):
            lo = v if lo is None or vt(v) > vt(lo) else lo
        else:
            hi = v if hi is None or vt(v) < vt(hi) else hi
    return lo, hi

def assess(f):
    arch = f.get("Architecture", "")
    dep = f.get("Depends", "") or ""
    lo, hi = fw(dep)
    issues, verdict = [], "VERIFIED"
    if arch == "iphoneos-arm64":
        issues.append("rootless (iphoneos-arm64) - not usable on Chimera rootful")
        verdict = "NOT COMPATIBLE"
    elif arch not in ("iphoneos-arm", "all"):
        issues.append("architecture " + arch)
        verdict = "UNVERIFIED"
    if "ellekit" in dep.lower():
        issues.append("depends on ellekit (rootless era)")
        verdict = "NOT COMPATIBLE"
    if lo and vt(lo) > (12, 5, 8):
        issues.append("requires iOS >= " + lo)
        verdict = "NOT COMPATIBLE"
    if hi and vt(hi) < (12, 0, 0):
        issues.append("supports only iOS <= " + hi)
        verdict = "NOT COMPATIBLE"
    return verdict, issues, lo, hi

def main():
    idx_dir = Path(sys.argv[1]); root = Path(sys.argv[2])
    db = {}
    for p in sorted(idx_dir.glob("*.index")):
        if p.stat().st_size == 0: continue
        repo = p.stem
        for f in paragraphs(read_index(p)):
            pid = f.get("Package")
            if not pid: continue
            rec = dict(f); rec["_repo"] = repo
            db.setdefault(pid, []).append(rec)

    def best(pid):
        recs = db.get(pid) or []
        if not recs: return None
        rootful = [r for r in recs if r.get("Architecture") == "iphoneos-arm"]
        pool = rootful or recs
        return sorted(pool, key=lambda r: vt(r.get("Version", "0")))[-1]

    entries = []
    for name, cat, pid, note, page in MANDATORY:
        r = best(pid)
        if not r:
            entries.append({"name": name, "package": pid, "category": cat, "status": "NOT FOUND",
                            "note": note, "searched_indexes": ["bigboss", "chariz", "havoc", "poomsmart"]})
            continue
        verdict, issues, lo, hi = assess(r)
        entries.append({
            "name": name, "package": r["Package"], "catalog_version": r.get("Version"),
            "name_in_index": r.get("Name"), "developer": r.get("Author") or r.get("Maintainer"),
            "category": cat, "section": r.get("Section"), "architecture": r.get("Architecture"),
            "ios_min": lo, "ios_max": hi, "depends": (r.get("Depends") or "").replace("\n", " "),
            "conflicts": (r.get("Conflicts") or "").replace("\n", " ")[:200],
            "source_repo": REPOS.get(r["_repo"], (r["_repo"], ""))[1],
            "filename_in_index": r.get("Filename"), "installed_size": r.get("Installed-Size"),
            "description": (r.get("Description") or "").replace("\n", " ")[:300],
            "status": verdict, "issues": issues, "note": note, "official_page": page or None,
            "ios12": "compatible" if verdict == "VERIFIED" else "not compatible/unknown",
            "chimera": "expected OK (rootful, substrate-compatible)" if verdict == "VERIFIED" else "n/a",
            "distribution": "NOT DISTRIBUTABLE (commercial/proprietary; catalog only)",
            "deb_added": False,
        })

    mandatory_ids = {e["package"] for e in entries}
    extra = []
    for pid, recs in db.items():
        if pid in mandatory_ids: continue
        r = best(pid)
        if not r: continue
        if r.get("Architecture") != "iphoneos-arm": continue
        verdict, issues, lo, hi = assess(r)
        if verdict != "VERIFIED": continue
        dep_l = (r.get("Depends") or "").lower()
        sec_l = (r.get("Section") or "").strip().lower()
        if lo:
            if vt(lo) < (10, 0, 0): continue
        else:
            if not sec_l.startswith("tweaks"): continue
            if "mobilesubstrate" not in dep_l: continue
            if any(m in dep_l for m in ("winterboard", "libhide", "gsc.", "weeloader", "weebrowser")): continue
        nm = (r.get("Name") or "")
        if not nm: continue
        if any(b in sec_l for b in BAD_SECTIONS): continue
        if sec_l and not any(sec_l.startswith(g) for g in GOOD_SECTIONS): continue
        low = (nm + " " + pid).lower()
        if not any(re.search(r"\b" + k + r"\b", low) for k in EXTRA_TOKENS): continue
        extra.append({"name": nm, "package": pid, "version": r.get("Version"),
                      "developer": r.get("Author") or r.get("Maintainer"), "section": r.get("Section"),
                      "architecture": r.get("Architecture"), "ios_min": lo, "ios_max": hi,
                      "depends": (r.get("Depends") or "").replace("\n", " ")[:200],
                      "source_repo": REPOS.get(r["_repo"], (r["_repo"], ""))[1],
                      "status": "PARTIALLY VERIFIED",
                      "distribution": "NOT DISTRIBUTABLE without author permission; catalog only"})
    extra.sort(key=lambda x: (x["section"] or "", x["name"]))
    extra = extra[:150]

    cats = {"appearance": ["Appearance", "Animations"],
            "system": ["SpringBoard", "LockScreen", "ControlCenter", "Notifications", "Security",
                       "Privacy", "Utilities", "Battery", "Network", "Safari", "Keyboard", "StatusBar"],
            "youtube": ["YouTube"], "instagram": ["Instagram"], "telegram": ["Telegram"], "tiktok": ["TikTok"]}
    cdir = root / "catalog"; cdir.mkdir(exist_ok=True)
    written = {}
    for fname, sections in cats.items():
        rows = [e for e in entries if e["category"] in sections]
        (cdir / (fname + ".json")).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written[fname] = len(rows)
    (cdir / "additional-candidates.json").write_text(json.dumps(extra, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written["additional"] = len(extra)
    external = [e for e in entries if e["status"] in ("NOT COMPATIBLE", "NOT DISTRIBUTABLE")]
    (cdir / "external-packages.json").write_text(json.dumps(external, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(written, indent=1))

    rdir = root / "reports"; rdir.mkdir(exist_ok=True)
    md = ["# Совместимость с iOS 12 / 12.5.8 — iPhone 6 (arm64, Chimera, rootful)", "",
          "Данные получены из реальных индексов APT (BigBoss, Chariz, Havoc, PoomSmart).",
          "Проверялись поля Architecture, Depends (в т.ч. firmware ...), Conflicts.", "",
          "| Твик | Package | Версия | Архитектура | iOS min | Статус |", "|---|---|---|---|---|---|"]
    for e in entries:
        md.append("| %s | %s | %s | %s | %s | %s |" % (
            e["name"], BT + e["package"] + BT, e.get("catalog_version") or "-",
            e.get("architecture") or "-", e.get("ios_min") or "-", e["status"]))
    md += ["", "## Замечания", "",
           "- iphoneos-arm = rootful (подходит для Chimera). iphoneos-arm64 = rootless (не подходит).",
           "- Chimera использует libhooker, который предоставляет mobilesubstrate; зависимость от mobilesubstrate сама по себе не блокирует установку.",
           "- Совместимость определена по метаданным индекса. Реальная работа на устройстве не проверялась."]
    (rdir / "compatibility.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    src = ["# Источники", "", "Индексы, реально использованные при анализе:", ""]
    for p in sorted(idx_dir.glob("*.index")):
        if p.stat().st_size == 0: continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        n = p.stem
        src.append("- %s (%s) — %d байт, sha256 %s..." % (REPOS.get(n, (n, ""))[1] or n, n, p.stat().st_size, h[:16]))
    src += ["", "Где искать отсутствующие пакеты:", "- Packix (закрыт, часть пакетов мигрировала в Havoc)",
            "- https://sparkdev.me/", "- https://repo.chariz.com/", "- https://havoc.app/",
            "- https://apt.thebigboss.org/"]
    (rdir / "sources.md").write_text("\n".join(src) + "\n", encoding="utf-8")

    miss = ["# Ненайденные пакеты", "",
            "Проверены индексы: BigBoss, Chariz, Havoc, PoomSmart (индекс SparkDev недоступен на момент анализа).", ""]
    for e in entries:
        if e["status"] == "NOT FOUND":
            miss.append("- %s (%s) — идентификатор не найден в проверенных индексах; возможно, пакет размещён на Packix/приватном репозитории или переименован." % (e["name"], BT + e["package"] + BT))
    (rdir / "missing-packages.md").write_text("\n".join(miss) + "\n", encoding="utf-8")

    stats = {
        "mandatory_total": len(entries),
        "verified": sum(1 for e in entries if e["status"] == "VERIFIED"),
        "not_compatible": sum(1 for e in entries if e["status"] == "NOT COMPATIBLE"),
        "not_found": sum(1 for e in entries if e["status"] == "NOT FOUND"),
        "additional_candidates": len(extra),
    }
    print(json.dumps(stats, indent=1))

if __name__ == "__main__":
    main()
