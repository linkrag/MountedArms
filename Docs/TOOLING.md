# Ferramentas e fluxo

## Compilar as DLLs (RimWorld 1.6 e 1.7)
`powershell -File build.ps1`, com o **jogo fechado** (ele trava as DLLs). Precisa do **SDK .NET 10**, instalado em 25/out/2026 com `winget install Microsoft.DotNet.SDK.10`, e de internet no primeiro build (pacotes NuGet). As DLLs são ignoradas pelo git.
- **Projetos:** um `.csproj` por DLL: `Source/MountedArms.csproj`, `SourceFx/MountedArmsFx.csproj` e `SourceCE/MountedArmsCE.csproj`.
- **Alvos (`Directory.Build.props`):**
  - `net472` = RimWorld 1.6 → `Bin/1.6/Assemblies`.
  - `net10.0` = RimWorld 1.7 → `Bin/1.7/Assemblies`.
  - A DLL só-CE vai para `Bin/<versão>/CE/Assemblies`.
- **Referências do jogo:** NuGet `Krafs.Rimworld.Ref`, `1.6.4871` e `1.7.4985-unstable`. Não precisa do jogo instalado. Quando o jogo atualizar, suba a versão no `Directory.Build.props` **dos dois mods** (cópias idênticas; manter em sincronia).
- **Harmony e CE:** vêm da pasta do Workshop (`2009463077/<versão>/Assemblies/0Harmony.dll` e `2890901044/Assemblies/CombatExtended.dll`). Nada disso é copiado para a saída. O CE é por versão: `CombatExtended16` e `CombatExtended17` no props. Quando sair um CE 1.7: `build.ps1 -CE17 <CombatExtended.dll>`, que compila a 1.7 contra ele sem as fachadas; a 1.6 continua com o CE do Workshop. Não passe `-p:CombatExtended`, porque valeria para as duas versões.
- **1.7 contra o CE 1.6:** antes de compilar a 1.7, o `build.ps1` roda `tools/unity_facades.ps1`. Esse script lê o `UnityStubs.dll` do jogo 1.7 e grava em `obj/facades`, e é o único passo que precisa do jogo 1.7 instalado. Ver `Docs/MIGRATION_1_7.md`.
- **Opções:**
  - `-Version 1.6` ou `-Version 1.7`: compila só uma versão.
  - `-Out <pasta>`: compila em outro lugar; serve para checar o build com o jogo aberto.
  - `-RW <pasta do jogo 1.7>`: indica onde está o jogo 1.7.
  - `-CE17 <dll>`: compila a 1.7 contra um CE 1.7 (ver acima).
  - `-Workshop <pasta>`: pasta `workshop/content/294100` de outra biblioteca Steam (Harmony, CE e o Mono.Cecil das fachadas).
- **Dependências fixas das fachadas (1.7):**
  - O `unity_facades.ps1` usa o csc do .NET Framework 4 do Windows (C# 5).
  - Ele usa também o Mono.Cecil embutido no Harmony **1.6** do Workshop; o Harmony 1.7 não serve.
  - Se o Harmony do Workshop perder a pasta `1.6`, o build da 1.7 quebra até trocarmos o leitor.
- **C#:** versão atual (Roslyn, `LangVersion latest`). O mesmo código compila para `net472` e para `net10.0`, então não use API que só exista no .NET 10; o build das duas versões acusa.
- **Determinístico:** o mesmo fonte gera o mesmo MD5 (o commit do git não entra na DLL: `IncludeSourceRevisionInInformationalVersion` false), e o `build.ps1` imprime o MD5 de cada DLL.
- **`dotnet build` direto:** funciona também (`dotnet build Source\MountedArms.csproj`, padrão Release, os dois alvos), mas não gera as fachadas: rode o `build.ps1` ao menos uma vez antes.
- **`MountedArmsFx.dll` separada da principal:** é histórico. Ela era C# 5 quando só havia o csc do .NET Framework, e a `MountedArmsCE.dll` a referencia (`ProjectReference`, sem cópia). Juntar as duas mudaria o carregamento sem ganho imediato.

## Validadores
`python tools/check.py` e `python tools/check_ce.py` (env `RW_ROOT`, `CE_ROOT`). Falsos positivos conhecidos: `MISSING manWorkType Violent` e `XPATH MATCHES NOTHING` nos Conditionals de `comps` (bateria, Bofors, CIWS, ZU-23, Avenger, Goalkeeper, laser), e `MISSING` para `MA_AmmoSet_APKWS_Indirect`/`MA_Bullet_APKWS_Indirect_HE`/`MA_AmmoSet_FIM92`/`MA_Bullet_FIM92_Stinger`/`MA_Bullet_LaserPulse` (definidos em `1.6/CE/Defs`, que o script não lê). `check_ce.py` precisa de `lxml` (`pip install lxml`).
`python tools/check_defnames.py`: falha se algum ThingDef termina em dígito (rodar SEMPRE antes de entregar).
`python tools/gen_tex.py` gera texturas.

## Armadilhas
- Não faça grep/find recursivo em toda a pasta Steam (timeout).
- defNames não podem terminar em dígito.
- Git local sem identidade global: `git -c user.name=... -c user.email=... commit`.
- MSBuild: uma propriedade passada na linha de comando (`-p:ModBin=...`) não pode ser reatribuída dentro do projeto. Por isso a barra final vai numa derivada, `ModBinDir`.
- MSBuild: com `AppendTargetFrameworkToOutputPath` false, os dois alvos dividiam o mesmo `obj`. Por isso o `IntermediateOutputPath` tem `$(TargetFramework)`.
- Publicar no Workshop: só `About`, `LoadFolders.xml`, `1.6/` e `Bin/`; nada de `obj/`, `Source*/`, `tools/` ou `Docs/`.
- Em sessões na nuvem, deletar arquivos na máquina do usuário exige permissão; o git pode deixar `.lock`.
- Commits terminam com os trailers `Co-Authored-By`/`Claude-Session` indicados pelo ambiente.
