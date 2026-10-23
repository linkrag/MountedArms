import os, re, sys, glob
import xml.etree.ElementTree as ET
from PIL import Image
# RW_ROOT = RimWorld install folder (default: path used in the cloud VM)
root = os.environ.get("RW_ROOT", os.path.expanduser("~/mnt/RimWorld"))
mod = os.path.join(root, "Mods/MountedArms/1.6")

# collect all defNames + Names from Core + DLCs + this mod
defs = set(); names = set()
for p in glob.glob(os.path.join(root, "Data/*/Defs/**/*.xml"), recursive=True) + glob.glob(mod + "/Defs/*.xml"):
    try: t = ET.parse(p)
    except Exception as e: print("PARSE FAIL", p, e); continue
    for e in t.getroot().iter():
        dn = e.find("defName")
        if dn is not None and dn.text: defs.add(dn.text.strip())
        if e.get("Name"): names.add(e.get("Name"))

bad = 0
def need(kind, v, pool):
    global bad
    if v not in pool: print("MISSING", kind, v); bad += 1

refs = {"turretGunDef","defaultProjectile","damageDef","soundCast","soundCastTail","manWorkType","tab","requiredResearchBuilding"}
for p in glob.glob(mod + "/Defs/*.xml"):
    r = ET.parse(p).getroot()
    for e in r.iter():
        if e.get("ParentName"): need("ParentName", e.get("ParentName"), names | defs)
        if e.tag in refs and e.text and e.text.strip(): need(e.tag, e.text.strip(), defs)
        if e.tag == "li" and e.text and e.text.strip():
            par = None
    for tag in ("researchPrerequisites","prerequisites"):
        for e in r.iter(tag):
            for li in e.findall("li"): need(tag, li.text.strip(), defs)
    for e in r.iter("fuelFilter"):
        for li in e.iter("li"): need("fuelFilter", li.text.strip(), defs)
    for e in r.iter("costList"):
        for c in e: need("costList", c.tag, defs)
print("reference check:", "OK" if not bad else f"{bad} problem(s)")

# duplicate defNames inside mod
seen = {}
for p in glob.glob(mod + "/Defs/*.xml"):
    for e in ET.parse(p).getroot().iter("defName"):
        seen[e.text] = seen.get(e.text, 0) + 1
print("duplicate defNames:", [k for k, v in seen.items() if v > 1] or "none")

# textures referenced exist
tex = set()
for p in glob.glob(mod + "/Defs/*.xml"):
    for tag in ("texPath","uiIconPath"):
        for e in ET.parse(p).getroot().iter(tag):
            if e.text.startswith("MountedArms/"): tex.add(e.text)
for t in sorted(tex):
    f = os.path.join(mod, "Textures", t + ".png")
    print(("OK  " if os.path.exists(f) else "MISSING ") + t)

# texture sanity
for f in sorted(glob.glob(mod + "/Textures/MountedArms/*.png")):
    im = Image.open(f).convert("RGBA"); a = im.split()[3]
    bb = a.getbbox(); px = sum(1 for v in a.getdata() if v > 10)
    print(f"{os.path.basename(f):16s} size={im.size} bbox={bb} opaque={px/ (im.size[0]*im.size[1]):.0%}")
