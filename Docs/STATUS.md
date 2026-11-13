# Status atual (atualize sempre que o usuário testar algo)

> **RimWorld 1.6 e 1.7 (25/out/2026):** conteúdo comum em `1.6/`; DLLs por versão em `Bin/1.6` e `Bin/1.7`, compiladas juntas pelo `build.ps1` (SDK .NET 10). **Testado em jogo em 26/out: carrega e funciona no 1.7 sem CE e com o CE 16.7.4.** Auditoria, riscos e toolchain: `MountedArms/Docs/MIGRATION_1_7.md`. Contexto anterior: `MountedArmsStrategic/Docs/HANDOFF.md`.

## Passo de "Até X" do Stinger (13/nov/2026) - deploy feito, **NÃO testado no jogo**
- `MakeMA_Ammo_FIM92_Stinger` (`1.6/CE/Defs/MountedArms_CE_Ammo.xml`) herdava `targetCountAdjustment` 20 do `AmmoRecipeBase` do CE, mas faz 4 por construção: agora `<targetCountAdjustment>4</targetCountAdjustment>` (o -/+ de "Até X" anda pelo lote). Achado pela auditoria do Colony Organizer, que também corrige isso em runtime; aqui vale mesmo sem ele. Regra para receitas novas com base no `AmmoRecipeBase`: declarar `targetCountAdjustment` = contagem do produto.

## Oficina Steam e fonte fora de `Mods` (7/nov/2026)
- Publicado na Oficina pelo usuário (ID 3835654835). O 1º upload levou a pasta inteira (Docs, Source, .git...): o fonte foi para `RimWorld/_dev/src/MountedArms` e `Mods/MountedArms` virou cópia limpa gerada por `tools/deploy.ps1` (chamado pelo `build.ps1`). Build 1.6 + 1.7 e deploy rodados com sucesso; a cópia tem só `About/`, `LoadFolders.xml`, `1.6/`, `Bin/`. **Falta:** "Atualizar na Oficina Steam" no jogo (troca conteúdo e thumb) e confirmar que o jogo carrega a cópia nova sem erro (**não testado no jogo**).
- Novo `About/Preview.png` (1280x720, `tools/gen_preview.py`) e descrição da Oficina em `Docs/WORKSHOP_DESCRIPTION.txt` (BBCode; colar à mão na página, o jogo não reenvia descrição). Detalhes: `../MountedArms/Docs/TOOLING.md` (seção "Fonte x cópia publicada").
- Achado da checagem da descrição: `AGENTS.md` regra 8 diz que o `BarrelHeat` fica inerte no CE, mas `Source/BarrelHeat.cs` atua em qualquer `Building_Turret` (vanilla e CE). Rever a regra (não alterada).


Ambiente: RimWorld 1.6 ou 1.7 (o jogo local está no 1.7.4985 desde 25/out/2026), Harmony, Combat Extended 16.7.4 (o usuário testa só no CE por enquanto). Jogo em `F:\Steam\steamapps\common\RimWorld`. DLLs: `build.ps1` (gera 1.6 e 1.7), com o jogo fechado.

## Confirmado funcionando em jogo
- M240, M134, M2, Mk 19 (CE com burst 4), Mk44 (vanilla e CE), sistemas de calor/giro/dispersão.
- **APKWS rocket battery (CE)**: acerta o alvo (projétil próprio `MA_Bullet_APKWS_Indirect_HE`: speed 0 + gravityFactor 5), ogiva HE (Bomb 156, raio 3,5) e dispersão da salva (`ShotSpread` 1,5, `circularError` 1) aprovadas.
- **Mk 15 Phalanx CIWS (CE)**: intercepta granadas de morteiro da retaliação — depende da opção do CE **"Enable CIWS"** (estava desligada no teste anterior, por isso nada era abatido).
- **Lote 5**: botão Descarregar (DLL só-CE `MountedArmsCE.dll`, Harmony postfix em `Building_TurretGunCE.GetGizmos` para defs `MA_*`), nomes reais nos `label`, CIWS 20 mm mais preciso (CE ShotSpread 0,03, SwayFactor 0,6, recuo 0,6; vanilla heatSpread 1, burstSpread 0,012).

## Migração para 1.7 (25/out/2026, NÃO testada)
- **DLLs por versão** em `Bin/1.6` e `Bin/1.7` (`build.ps1`, SDK .NET 10, referências `Krafs.Rimworld.Ref`). As DLLs antigas de `1.6/Assemblies` e `1.6/CE/Assemblies` saíram.
- **DLLs de 1.6 recompiladas:** pelo dump de metadados, são equivalentes às testadas. Não dá para testar em jogo nesta máquina, que agora é 1.7.
- **DLLs de 1.7 nativas:** a `MountedArmsCE.dll` foi compilada contra o CE 16.7.4 com as fachadas `UnityEngine.*` → `UnityStubs`.
- Testes e riscos: `Docs/MIGRATION_1_7.md`.

## Ajustes desta rodada (NÃO testados)
- **Aba "Militar" no Architect** (2/nov/2026): novo `DesignationCategoryDef` `MA_Military` (`1.6/Defs/DesignationCategories.xml`, order 310; PT-BR em `DefInjected`). `MA_TurretBase` e o M252 saíram de Security. Os prédios do Mounted Arms Strategic entram na mesma aba por patch (`MountedArmsStrategic/1.6/MountedArms/Patches/MilitaryCategory.xml`, só com `linkrag.mountedarms` ativo; sem ele ficam em Security).
- **Chama no bocal** (`CompProperties_Exhaust` em `MountedArmsFx.dll`) no APKWS indireto (`comps Inherit="False"` para tirar a chama herdada do CE, que ficava no meio do foguete).
- **Ignição do Stinger no CE**: posicionada ao longo da trajetória 3D (horizontal × cos do ângulo, altura desenhada +0,84 × altura em z), não mais no chão 4 células à frente em tiros íngremes (achado da revisão).
- **Lançamento com efeitos (soft launch)**, só visual (velocidade e mira intocadas; a interceptação do CE precisa de voo linear): nova DLL `MountedArmsFx.dll` (fonte `SourceFx/`, carregada com e sem CE) com `LaunchFxExtension` (no def da **arma**) + patch no `Projectile.Launch` do vanilla; no CE, patch em `ProjectileCE.Launch(Thing, Vector2, Thing)` na `MountedArmsCE.dll` (vale também para os interceptadores).
  - Stinger (Avenger): puff de ejeção + backblast, motor de voo acende a 4 células (~8,5 m reais).
  - TOW: motor de lançamento se esgota na saída do tubo (backblast 3), motor de voo a 3,5 células (~7 m reais).
  - Pod B-8 (S-8) e bateria APKWS: lançamento quente, clarão na boca.
- **Avenger (CE)** não interceptava (usuário). Tinha só o verbo de drop pods; agora também `VerbCIWSProjectile` (mísseis e granadas; pedido do usuário, jogo acima do realismo).

## Implementado, NÃO confirmado
- **BGM-71 TOW (CE)**: `FireModes aiAimMode AimedShot` (antes mirava e não disparava). Alcance vanilla 71,9 / CE 100.
- **B-8 rocket pod (CE)**: `AmmoSet_80mmRocket_direct` (o APKWS 70 mm direto voava >1 min).
- **M252 (CE)**: NRE corrigido com `fixedStorageSettings`; botão "atacar mundo" escondido (`NoWorldStrikeExtension`).
- **Bofors 40 mm L/60 duplo e quádruplo** (tripulados, 360°, sem energia, 25/20 °/s): CE 40x311mmR, alcance 86, intercepta projéteis (100) e drop pods (125) via `Building_CIWS_CE`.
- **ZU-23-2** (tripulada, 60 °/s): CE 23x152mmB, 75, mag 100, intercepta projéteis (90) e drop pods (110).
- **AN/TWQ-1 Avenger** (150 W): vanilla mísseis contra o chão; CE intercepta projéteis e drop pods (110), munição própria `MA_Ammo_FIM92_Stinger`.
- **Goalkeeper** (900 W, 100 °/s): CE 30x173mm, 78, mag 600, intercepta projéteis (100).
- **Iron Beam** (2000 W, Spacer): sem munição; CE `MA_Bullet_LaserPulse`, intercepta projéteis (100).
- Phalanx: giro 100 °/s, 700 W.
- **Gatling (Colt M1883)** — **testada pelo usuário (vanilla e CE)**, no CE a cadência ficou abaixo da do vanilla (o `AimedShot` mirava antes de cada tiro) → trocado para `SuppressFire`; **retestado**: ~10 s por tambor, a maioria dos tiros bate no chão antes do alvo a meio alcance (em AimedShot acertava em 3–4 tiros). Usuário aceitou como balanceado. Causa (código do CE): sway = (4,5 − ShootingAccuracyTurret 0,80) × SwayFactor 1,6 ≈ 5,9 (M240 ~2,9, M2 ~4,2) + AimingAccuracy do operador + sem tempo de mira. Se precisar suavizar: SwayFactor 1,2. (tripulada, sem energia, 30 °/s; out/2026): pesquisa só com Gunsmithing; fogo contínuo em tiro único (vanilla 0,15 s, CE 0,1 s), precisão ruim, fumaça a cada tiro; vanilla .45-70 próprio (14/0,20), 29,9; CE `AmmoSet_4570Gov`, 55, tambor 104. Textura gerada por `gen_tex.py` (`Gatling`). Testar: construir cedo, operar, superaquecer, trocar barril (vanilla); carregar .45-70 e disparar (CE).

## Notas de interceptação (CE)
- Precisa da opção "Enable CIWS". Tripuladas (Bofors, ZU-23) só interceptam com alguém operando. Os botões de "segurar fogo" de CIWS desligam a interceptação.
- O verbo CIWS só dispara se a posição prevista do projétil entra no alcance no próximo segundo e o tiro chega a tempo; giro lento atrasa. Diagnóstico: modo de depuração do CE + "Draw intercept checks".

## Pendências
- Usuário cria o remote Git e envia a URL.
