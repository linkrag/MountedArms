# Ferramentas e fluxo

## Compilar a DLL
`Source/build.sh` (variáveis `RW` = pasta do RimWorld, `HARMONY` = 0Harmony.dll). Equivalente:
`mcs -target:library -debug- -optimize+ -out:1.6/Assemblies/MountedArms.dll -r:$M/Assembly-CSharp.dll -r:$M/UnityEngine.dll -r:$M/UnityEngine.CoreModule.dll -r:$M/netstandard.dll -r:0Harmony.dll Source/*.cs`
com `M=<RimWorld>/RimWorldWin64_Data/Managed`. A DLL é ignorada pelo git.

## DLL de efeitos (com e sem CE)
`powershell -File SourceFx/build_fx.ps1` → `1.6/Assemblies/MountedArmsFx.dll` (C# 5, refs jogo + Harmony + Unity.Mathematics). Existe separada porque a DLL principal usa C# 6 (`nameof`) e a máquina só tem o csc do .NET Framework (C# 5); sem mono/Roslyn. Compile ANTES da DLL só-CE (ela referencia a Fx). Jogo fechado.

## DLL só-CE
`powershell -File SourceCE/build_ce.ps1` → `1.6/CE/Assemblies/MountedArmsCE.dll` (csc do .NET Framework, C# 5, contra o mscorlib do jogo; refs CE + Harmony 1.6). `-Out <pasta>` compila em outro lugar (útil com o jogo aberto, que trava a DLL). Ignorada pelo git.

## Validadores
`python tools/check.py` e `python tools/check_ce.py` (env `RW_ROOT`, `CE_ROOT`). Falsos positivos conhecidos: `MISSING manWorkType Violent` e `XPATH MATCHES NOTHING` nos Conditionals de `comps` (bateria, Bofors, CIWS, ZU-23, Avenger, Goalkeeper, laser), e `MISSING` para `MA_AmmoSet_APKWS_Indirect`/`MA_Bullet_APKWS_Indirect_HE`/`MA_AmmoSet_FIM92`/`MA_Bullet_FIM92_Stinger`/`MA_Bullet_LaserPulse` (definidos em `1.6/CE/Defs`, que o script não lê). `check_ce.py` precisa de `lxml` (`pip install lxml`).
`python tools/check_defnames.py`: falha se algum ThingDef termina em dígito (rodar SEMPRE antes de entregar).
`python tools/gen_tex.py` gera texturas.

## Armadilhas
- Não faça grep/find recursivo em toda a pasta Steam (timeout).
- defNames não podem terminar em dígito.
- Git local sem identidade global: `git -c user.name=... -c user.email=... commit`.
- Em sessões na nuvem, deletar arquivos na máquina do usuário exige permissão; o git pode deixar `.lock`.
- Commits terminam com os trailers `Co-Authored-By`/`Claude-Session` indicados pelo ambiente.
