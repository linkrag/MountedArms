# Migração para RimWorld 1.7 (Waylith), vale para os dois mods

Atualizado em 26/out/2026, jogo 1.7.4985 rev1269. **Ainda não testado em jogo.**

## Decisões do usuário (25/out/2026)
- Manter suporte a **1.6 e 1.7**.
- SDK .NET 10 instalado na máquina (`winget install Microsoft.DotNet.SDK.10`, versão 10.0.403), para compilar as duas versões com C# atual.

## O que mudou no jogo (verificado na pasta do jogo)
- **Engine:** saiu a Unity. Runtime .NET 10 (CoreCLR, `RimWorld.runtimeconfig.json` `tfm net10.0`), Vulkan, bibliotecas `Brutal.*` e `Waylith.*`.
- **DLLs do jogo:** não existe mais `RimWorldWin64_Data/Managed`; elas estão na **raiz** da pasta do jogo: `Assembly-CSharp.dll` (Verse + RimWorld), `UnityStubs.dll` (a API Unity, inclusive `Unity.Mathematics`), `mscorlib.dll`/`netstandard.dll` (facades), `System.*.dll`.
- **`runtimeconfig`:** `AssemblyNameRedirects = UnityEngine*=UnityStubs; Unity.*=UnityStubs`, e vinculação tolerante (`LaxAssemblyBinding`, `LaxMemberSignatures`, `LaxTypeRefResolution`, `LaxPrivateFieldNames`, `SkipAccessChecks`...).
- **`JitPatchableAssemblies = Assembly-CSharp`.** Hipótese: métodos pequenos de **outros** assemblies (CE) podem ser inlinados e escapar de patches Harmony. Os nossos alvos no CE hoje são virtuais ou grandes.
- **Harmony 1.7 = Harmony 3** (`2009463077/1.7/Assemblies/0Harmony.dll`). Ele checa tipo e nome de `__instance`/`__result`/parâmetros.
- **Dubs Rimatomics** já tem pasta `1.7`. `NuclearStrike.Yield` continua `public float`.
- **Combat Extended** instalado (16.7.4) declara só 1.6. Não há build 1.7 oficial (o CE tem um branch `1.7-Test`; existe um port não oficial no Workshop, com packageId desconhecido).

## Layout (os dois mods)
- **Conteúdo comum** continua em `1.6/` e é carregado pelas duas versões: Defs, Textures, Languages, Patches, `1.6/CE` e `1.6/Rimatomics`.
- **DLLs por versão** em `Bin/1.6/` e `Bin/1.7/`, não versionadas. No Mounted Arms, a DLL só-CE fica em `Bin/<versão>/CE/Assemblies`.
- **`LoadFolders.xml`:** `<v1.6>` carrega `/`, `1.6` e `Bin/1.6`; `<v1.7>` é igual, com `Bin/1.7`. Cada assembly é carregado uma vez só.
  - Mounted Arms: com CE, também `1.6/CE` e `Bin/<versão>/CE`.
  - Strategic (exige CE): com Rimatomics, também `1.6/Rimatomics`.
- **`About.xml`:** `supportedVersions` 1.6 e 1.7.
- **Strategic:** a pasta `1.6/Legacy1.6` foi apagada. Ela mantinha o `circularError` 2 da HIMARS só na 1.6, e o `Bin/1.6` agora já tem o código do lote 11.

## Build (SDK .NET 10)
- **Como rodar:** `powershell -File build.ps1` na raiz de cada mod, com o jogo fechado. Detalhes e opções em `Docs/TOOLING.md`.
- **Alvos e referências (`Directory.Build.props`, cópia idêntica nos dois mods; manter em sincronia):**
  - `TargetFrameworks`: `net472` = 1.6 e `net10.0` = 1.7.
  - Jogo: NuGet `Krafs.Rimworld.Ref` `1.6.4871` e `1.7.4985-unstable`.
  - Harmony (`2009463077/<versão>`) e CE (`2890901044`): da pasta do Workshop, sem cópia para a saída.
- **1.7 contra o CE 1.6:** as fachadas `UnityEngine.*` → `UnityStubs` (`tools/unity_facades.ps1`) entram só nos projetos com CE e só no alvo `net10.0`. Ver a seção abaixo.
- **Verificado em 25/out** (dump de metadados com System.Reflection.Metadata, no scratch):
  - **DLLs de 1.6 do Mounted Arms recompiladas = as testadas.** Os tipos, métodos, campos e member refs escritos à mão são os mesmos, e a referência é a mesma `Assembly-CSharp 1.6.9676.17735` (o `Krafs 1.6.4871` é o build do jogo 1.6 do usuário).
    - Diferenças: código gerado pelo compilador (iteradores) e atributos de assembly.
    - Versão do assembly: 0.0.0.0 → 1.0.0.0, nas três DLLs ao mesmo tempo.
  - **DLLs de 1.7** referenciam `System.Runtime 10`, `Assembly-CSharp 1.7.9790.38077` (o do jogo), `UnityStubs` e `0Harmony 3.0`. As que usam CE não referenciam mais `UnityEngine.*`.
  - **Strategic 1.7:** a DLL nova é equivalente à que a sessão anterior compilou com csc + fachadas, e a de 1.6 tem a mesma superfície que a de 1.7.
  - **Builds determinísticos:** o mesmo MD5 compilando em pastas diferentes.
    - Na revisão de 26/out apareceu um furo: o SDK gravava o commit do git no `AssemblyInformationalVersion`, e o MD5 mudava a cada commit.
    - Corrigido com `IncludeSourceRevisionInInformationalVersion` false. Os MD5 mudaram uma vez por isso, e o código não mudou.

## Auditoria de compatibilidade (25/out, sem rodar o jogo)
A checagem foi feita por metadados (System.Reflection.Metadata contra o `Assembly-CSharp` 1.7, `UnityStubs` e Harmony 3) e por sondas compiladas contra o 1.7.

**OK no 1.7 vanilla:**
- **Referências da `MountedArms.dll` (1.6):** as 139 resolvem no 1.7. Desde 25/out existe também a DLL nativa de 1.7.
- **Patches Harmony:** `Projectile.Launch` (8 args, mesmos nomes de parâmetro), `TurretTop.TurretTopTick` e `Building_TurretGun.IsValidTarget`/`OrderAttack`.
- **Campos privados acessados por reflexão:** `burstShotsLeft`, `burstCooldownTicksLeft`, `burstWarmupTicksLeft`, `ResetCurrentTarget` e `parentTurret`. Mesmo papel no IL do 1.7, inclusive o truque de segurar o warmup em 1.
- **API de efeitos:** `FleckMaker`, `CameraShaker.DoShake`, `SoundDef.Named` e `MaterialPool`.
- **XML:** campos dos defs vanilla, defNames vanilla referenciados e chaves de tradução (English e PortugueseBrazilian).

**Corrigido em 25–26/out:** os três scripts do Mounted Arms (csc/mcs contra `RimWorldWin64_Data/Managed`) e o `Source/build.ps1` do Strategic (csc, uma versão por vez conforme o jogo instalado) foram trocados pelo `build.ps1` com o SDK, que gera as duas versões.

**Sem mudança:** `tools/check.py` e `check_ce.py` continuam lendo `1.6/`, que segue sendo a pasta de conteúdo.

**Pendente de CE 1.7 (RISCO):**
- **Camada CE do Mounted Arms:** todos os alvos dentro do CE (`ProjectileCE.Launch`, `Building_TurretGunCE.GetGizmos`, `Command_ArtilleryTarget`).
- **Strategic inteiro:** `HostilitySheller.TryStartShelling`, `ProjectileCE_CIWS.Tick`, `ProjectileCE.DrawRotation`, `AmmoThing.TryDetonate`, `Verb_ShootMortarCE`, `LerpedTrajectoryWorker`, `CompExplosiveCE` e os presets de shelling.
- **Quando sair um CE 1.7:** `build.ps1 -CE17 <CombatExtended.dll do CE 1.7>`. Isso compila a 1.7 contra ele sem as fachadas, e a 1.6 continua com o CE do Workshop. Para deixar isso permanente:
  - mude, no `Directory.Build.props` dos dois mods, o padrão de `CombatExtended17` para a DLL nova e o de `CEFacades` para `false`;
  - tire do `build.ps1` o passo das fachadas (hoje ele só pula esse passo com `-CE17`);
  - confira se o `IfModActive`/packageId do CE 1.7 é o mesmo.
- **`PatchAll()` sem try/catch:** `MountedArmsCE.cs:18` e Strategic `Settings.cs:33`. Se um alvo do CE mudar no 1.7, os patches seguintes não são aplicados. Agora dá para recompilar; falta decidir se corrigimos já.
- **`Thing __instance`:** `MountedArms.cs:30` declara a classe base. O Harmony 3 deve aceitar, mas não foi provado.
- **Port não oficial do CE:** se o packageId dele não for `CETeam.CombatExtended`, o `IfModActive` e a dependência do Strategic não o reconhecem.

## Compilar contra o CE 1.6 na 1.7
- **Causa do erro:** o CS0012/CS0508 vem dos nomes `UnityEngine.CoreModule`/`IMGUIModule`/`TextRenderingModule`/`InputLegacyModule`/`UI` que o CE referencia. O jogo só os redireciona para `UnityStubs` em tempo de execução.
- **Solução:** assemblies de fachada com esses nomes, contendo só `[assembly: TypeForwardedTo(...)]` para cada tipo público `UnityEngine*`/`Unity.Mathematics` do `UnityStubs`.
  - A lista de tipos é lida com o Mono.Cecil do Harmony 1.6.
  - Script: `tools/unity_facades.ps1`, uma cópia em cada mod (mesmo conteúdo; manter em sincronia). Ele lê o `UnityStubs.dll` do jogo 1.7 e grava em `obj/facades`; o `build.ps1` o chama antes de compilar a 1.7.
- **Avisos silenciados no `Directory.Build.props`:** CS1701/CS1702 (versões de CoreLib e de `Assembly-CSharp` pedidas pelo CE e pelas fachadas) e CS1684 (`Unity.Collections.NativeArray`, não usado).
- **A DLL resultante roda só na 1.7**, porque referencia `UnityStubs` e o `Assembly-CSharp` 1.7. Por isso cada versão tem a sua pasta `Bin/<versão>`.

## Teste a fazer (usuário)
1. **1.7 sem CE**, com Harmony e Mounted Arms: deve carregar sem erros, e as torretas devem atirar, aquecer e girar. O Strategic exige CE e deve só acusar a dependência faltando.
2. **1.7 com o CE 16.7.4 (1.6):** primeiro, ver se o próprio CE carrega. Se carregar, testar a camada CE do Mounted Arms (Descarregar, efeitos de lançamento) e o Strategic (lotes 10 e 11, ver o `STATUS` dele).
3. **Mandar o log.** No 1.7 o local ainda não foi confirmado: o `Player.log` em `AppData/LocalLow/Ludeon Studios/...` ainda é do 1.6.
4. **1.6** não dá para testar nesta máquina, porque o jogo local é 1.7.
   - As DLLs de 1.6 do Mounted Arms foram comparadas por metadados com as testadas.
   - A do Strategic agora inclui o lote 11, que não foi testado em nenhuma versão.
