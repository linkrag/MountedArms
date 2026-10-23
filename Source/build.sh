#!/bin/sh
# Builds 1.6/Assemblies/MountedArms.dll (needs mono's mcs and 0Harmony.dll from brrainz.harmony)
# usage: RW=/path/to/RimWorld HARMONY=/path/to/0Harmony.dll sh Source/build.sh
M="$RW/RimWorldWin64_Data/Managed"
cd "$(dirname "$0")"
mcs -target:library -debug- -optimize+ -out:../1.6/Assemblies/MountedArms.dll \
  -r:$M/Assembly-CSharp.dll -r:$M/UnityEngine.dll -r:$M/UnityEngine.CoreModule.dll \
  -r:$M/netstandard.dll -r:"$HARMONY" MountedArms.cs BarrelHeat.cs SlewArc.cs
