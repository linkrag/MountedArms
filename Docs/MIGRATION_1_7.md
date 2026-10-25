# Migração para RimWorld 1.7 (Waylith), vale para os dois mods

Atualizado em 25/out/2026, jogo 1.7.4985 rev1269. Ainda não testado em jogo.

## O que mudou no jogo (verificado na pasta do jogo)
- Saiu a Unity. Runtime .NET 10 (CoreCLR, `RimWorld.runtimeconfig.json` `tfm net10.0`), Vulkan, bibliotecas `Brutal.*` e `Waylith.*`.
- Não existe mais `RimWorldWin64_Data/Managed`. As DLLs do jogo estão na **raiz** da pasta do jogo: `Assembly-CSharp.dll` (Verse + RimWorld), `UnityStubs.dll` (a API Unity, inclusive `Unity.Mathematics`), `mscorlib.dll`/`netstandard.dll` (facades), `System.Runtime.dll`, `System.Private.CoreLib.dll`, `System.Collections.dll`.
- `runtimeconfig`: `AssemblyNameRedirects = UnityEngine*=UnityStubs; Unity.*=UnityStubs`, e vinculação tolerante (`LaxAssemblyBinding`, `LaxMemberSignatures`, `LaxTypeRefResolution`, `LaxPrivateFieldNames`, `SkipAccessChecks`...). Por isso DLLs compiladas para 1.6 tendem a carregar sem recompilar.
- `JitPatchableAssemblies = Assembly-CSharp`. Hipótese: métodos pequenos de **outros** assemblies (CE) podem ser inlinados e escapar de patches Harmony. Os nossos alvos no CE hoje são virtuais ou grandes.
- Harmony 1.7 = **Harmony 3** (`2009463077/1.7/Assemblies/0Harmony.dll`). Ele checa tipo e nome de `__instance`/`__result`/parâmetros.
- Dubs Rimatomics já tem pasta `1.7`. `NuclearStrike.Yield` continua `public float`.
- **Combat Extended** instalado (16.7.4) declara só 1.6. Não há build 1.7 oficial (o CE tem um branch `1.7-Test`; existe um port não oficial no Workshop com packageId desconhecido).

## O que foi feito
- `About.xml` dos dois mods: `supportedVersions` 1.6 + 1.7.
- `LoadFolders.xml` dos dois mods: bloco `<v1.7>` igual ao `<v1.6>`, reaproveitando as pastas `1.6/` e as DLLs de 1.6 (uma só cópia de cada assembly).
- Nenhuma DLL foi recompilada.

## Auditoria de compatibilidade (25/out, sem rodar o jogo)
A checagem foi feita por metadados (System.Reflection.Metadata contra o `Assembly-CSharp` 1.7, `UnityStubs` e Harmony 3) e por sondas compiladas contra o 1.7.

**OK no 1.7 vanilla:**
- **Referências da `MountedArms.dll`:** as 139 resolvem no 1.7.
- **Patches Harmony:** `Projectile.Launch` (8 args, mesmos nomes de parâmetro), `TurretTop.TurretTopTick`, `Building_TurretGun.IsValidTarget`/`OrderAttack`.
- **Campos privados acessados por reflexão:** `burstShotsLeft`, `burstCooldownTicksLeft`, `burstWarmupTicksLeft`, `ResetCurrentTarget`, `parentTurret`. Mesmo papel no IL do 1.7, inclusive o truque de segurar o warmup em 1.
- **API de efeitos:** `FleckMaker`, `CameraShaker.DoShake`, `SoundDef.Named`, `MaterialPool`.
- **XML:** campos dos defs vanilla, defNames vanilla referenciados e chaves de tradução (English e PortugueseBrazilian).
- **`MountedArmsFx.dll`:** compila contra o 1.7.

**Quebrado:**
- Os quatro scripts de build (`Source/build.sh`, `SourceFx/build_fx.ps1`, `SourceCE/build_ce.ps1`, Strategic `Source/build.ps1`) apontam para `RimWorldWin64_Data/Managed`, Harmony 1.6 e `Unity.Mathematics.dll`, que não existem mais.
- Também não conseguem gerar DLL para 1.6, porque o jogo local agora é 1.7.
- `tools/check.py` e `check_ce.py` fixam a pasta `1.6`. Funcionam enquanto o conteúdo continuar em `1.6/`.

**Pendente de CE 1.7 (RISCO):**
- **Camada CE do Mounted Arms:** a `MountedArmsCE.dll` e todos os alvos dentro do CE (`ProjectileCE.Launch`, `Building_TurretGunCE.GetGizmos`, `Command_ArtilleryTarget`).
- **Strategic inteiro:** `HostilitySheller.TryStartShelling`, `ProjectileCE_CIWS.Tick`, `ProjectileCE.DrawRotation`, `AmmoThing.TryDetonate`, `Verb_ShootMortarCE`, `LerpedTrajectoryWorker`, `CompExplosiveCE`, os presets de shelling.
- **Recompilação:** a `MountedArmsCE.dll` e a `MountedArmsStrategic.dll` não recompilam contra o 1.7 enquanto o CE for o de 1.6. O CE 16.7.4 referencia `UnityEngine.CoreModule`, que não se unifica com `UnityStubs` em tempo de compilação (CS0012/CS0508). Em execução, o redirecionamento deve resolver.
- **`PatchAll()` sem try/catch:** `MountedArmsCE.cs:18` e Strategic `Settings.cs:33`. Se um alvo do CE mudar no 1.7, os patches seguintes não são aplicados. Corrigir quando houver CE 1.7, junto com a recompilação.
- **`Thing __instance`:** `MountedArms.cs:30` declara a classe base. O Harmony 3 deve aceitar, mas não foi provado.
- **Port não oficial do CE:** se o packageId dele não for `CETeam.CombatExtended`, o `IfModActive` e a dependência do Strategic não o reconhecem.

## Toolchain no 1.7
- **Sem SDK .NET** na máquina; só os runtimes 6 e 8. O csc do .NET Framework (C# 5) compila contra o 1.7 com:
  `/noconfig /nostdlib /r:<jogo>\mscorlib.dll /r:netstandard.dll /r:System.Runtime.dll /r:System.Private.CoreLib.dll /r:System.Collections.dll /r:Assembly-CSharp.dll /r:UnityStubs.dll /r:<Harmony 1.7>`
- **`Source/` principal do Mounted Arms:** é C# 6+ e precisa de Roslyn. O caminho recomendado é o SDK .NET 10 (a wiki recomenda .NET 10; VS2022 não suporta).
- **DLL recompilada para 1.7:** referencia `UnityStubs` e não roda no 1.6. Ao recompilar, separar o conteúdo comum (Defs, Textures, Languages, Patches) das `Assemblies` por versão, para não carregar duas cópias.

## Teste a fazer (usuário)
1. Abrir o 1.7 com Harmony, os dois mods **sem CE**: o Mounted Arms vanilla deve carregar sem erros e as torretas devem atirar, aquecer e girar. O Strategic exige CE e deve só acusar a dependência faltando.
2. Com o CE 16.7.4 (1.6) ativo: ver se o próprio CE carrega no 1.7. Se carregar, testar as camadas CE e o Strategic como no 1.6.
3. Mandar o log. No 1.7 o local ainda não foi confirmado: o `Player.log` em `AppData/LocalLow/Ludeon Studios/...` ainda é do 1.6.
