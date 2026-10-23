import os, glob, re, sys
from lxml import etree
# RW_ROOT = RimWorld install folder; CE_ROOT = CE workshop folder (steam/workshop/content/294100/2890901044)
rw  = os.environ.get("RW_ROOT", os.path.expanduser("~/mnt/RimWorld"))
mod = os.path.join(rw, "Mods/MountedArms/1.6")
ce  = os.environ.get("CE_ROOT", os.path.expanduser("~/mnt/2890901044"))

# merged doc of our defs (what the patches run against)
merged = etree.Element("Defs")
for p in sorted(glob.glob(mod + "/Defs/*.xml")):
    for e in etree.parse(p).getroot(): merged.append(e)

patch = etree.parse(mod + "/CE/Patches/MountedArms_CE.xml").getroot()
bad = 0; n = 0
# 1) xpaths of vanilla patch operations must match >=1 node in our defs
for op in patch.iter("Operation"):
    cls = op.get("Class")
    if cls == "CombatExtended.PatchOperationMakeGunCECompatible":
        dn = op.findtext("defName")
        ok = merged.xpath(f'ThingDef[defName="{dn}"]')
        n += 1
        if not ok: print("NO GUN DEF", dn); bad += 1
        continue
    xp = op.findtext("xpath")
    xp = re.sub(r"\s+", " ", xp).strip()
    xp = xp.replace("[ ", "[").replace(" ]", "]")
    hits = merged.xpath("/" + xp if xp.startswith("Defs") else xp, ) if False else etree.ElementTree(merged).xpath("/" + xp)
    n += 1
    if not hits: print("XPATH MATCHES NOTHING:", cls, xp[:110]); bad += 1
print(f"{n} operations checked, {bad} problem(s)")

# 2) referenced defs exist in vanilla (all DLC) + CE
pool = set()
for p in glob.glob(os.path.join(rw, "Data/*/Defs/**/*.xml"), recursive=True) + glob.glob(ce + "/Defs/**/*.xml", recursive=True):
    try:
        for e in etree.parse(p).getroot().iter():
            dn = e.find("defName") if isinstance(e.tag, str) else None
            if dn is not None and dn.text: pool.add(dn.text.strip())
    except Exception: pass
refs = set()
for tag in ("defaultProjectile","soundCast","soundCastTail","ammoSet"):
    for e in patch.iter(tag): refs.add((tag, e.text.strip()))
for tag, v in sorted(refs):
    print(("OK      " if v in pool else "MISSING ") + tag + " " + v)
