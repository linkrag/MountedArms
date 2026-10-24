# Builds 1.6/Assemblies/MountedArmsFx.dll (launch effects; loaded with and without CE; no CE references).
# .NET Framework compiler (C# 5), against the game's own mscorlib. Close the game first (it locks the DLL);
# -Out builds elsewhere to just check the compile.
param(
    [string]$RW = "F:\Steam\steamapps\common\RimWorld",
    [string]$Harmony = "F:\Steam\steamapps\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll",
    [string]$Out = ""
)
$ErrorActionPreference = "Stop"
$csc = "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
$m = "$RW\RimWorldWin64_Data\Managed"
$root = Split-Path $PSScriptRoot -Parent
$out = if ($Out) { $Out } else { "$root\1.6\Assemblies" }
New-Item -ItemType Directory -Force $out | Out-Null
& $csc /nologo /noconfig /target:library /optimize+ /debug- /nostdlib /out:"$out\MountedArmsFx.dll" `
    /r:"$m\mscorlib.dll" /r:"$m\System.dll" /r:"$m\System.Core.dll" /r:"$m\Assembly-CSharp.dll" `
    /r:"$m\UnityEngine.dll" /r:"$m\UnityEngine.CoreModule.dll" /r:"$m\netstandard.dll" /r:"$m\Unity.Mathematics.dll" `
    /r:"$Harmony" `
    "$PSScriptRoot\*.cs"
if ($LASTEXITCODE -ne 0) { throw "csc failed ($LASTEXITCODE)" }
Get-FileHash "$out\MountedArmsFx.dll" -Algorithm MD5 | Select-Object Hash, Path
