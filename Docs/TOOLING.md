# Ferramentas e fluxo

## Compilar a DLL
`Source/build.sh` (variáveis `RW` = pasta do RimWorld, `HARMONY` = 0Harmony.dll). Equivalente:
`mcs -target:library -debug- -optimize+ -out:1.6/Assemblies/MountedArms.dll -r:$M/Assembly-CSharp.dll -r:$M/UnityEngine.dll -r:$M/UnityEngine.CoreModule.dll -r:$M/netstandard.dll -r:0Harmony.dll Source/*.cs`
com `M=<RimWorld>/RimWorldWin64_Data/Managed`. A DLL é ignorada pelo git.

## Validadores
`python tools/check.py` e `python tools/check_ce.py` (env `RW_ROOT`, `CE_ROOT`). Falsos positivos conhecidos: `MISSING manWorkType Violent` e `XPATH MATCHES NOTHING` nos Conditionals de `comps` (bateria, Bofors, CIWS), e `MISSING` para `MA_AmmoSet_APKWS_Indirect`/`MA_Bullet_APKWS_Indirect_HE` (definidos em `1.6/CE/Defs`, que o script não lê). `check_ce.py` precisa de `lxml` (`pip install lxml`).
`python tools/gen_tex.py` gera texturas.

## Armadilhas
- Não faça grep/find recursivo em toda a pasta Steam (timeout).
- defNames não podem terminar em dígito.
- Git local sem identidade global: `git -c user.name=... -c user.email=... commit`.
- Em sessões na nuvem, deletar arquivos na máquina do usuário exige permissão; o git pode deixar `.lock`.
- Commits terminam com os trailers `Co-Authored-By`/`Claude-Session` indicados pelo ambiente.
