# AGENTS.md — Mounted Arms (guia para agentes de código)

Leia este arquivo inteiro antes de mexer em qualquer coisa. Detalhes ficam em `Docs/` (índice no fim).

## O que é o projeto
Mod de RimWorld **1.6** (`packageId: linkrag.mountedarms`, autor Felipe) que adiciona **torretas baseadas em armas montadas modernas** (M240, M134, M2, Mk19, Mk44, TOW, foguetes 80mm, CIWS 20mm, morteiro M252, bateria de foguetes guiados), com equilíbrio "vanilla-friendly" e uma **camada de compatibilidade com Combat Extended (CE)** carregada só quando o CE está ativo. Requer Harmony; nenhum DLC.

## Quem é o usuário e como trabalhar com ele
- Felipe, brasileiro. **Responda em português (BR)**, de forma concisa e direta. Engenheiro Java/Spring/Kafka, modder de RimWorld com vários mods; testa no jogo e envia logs.
- Ele **verifica as suas respostas e corrige**. Seja honesto: separe o que foi verificado (código, log, fonte) do que é hipótese; diga "não testei" quando for o caso. Não invente comportamento do jogo/CE: leia o código/defs.
- Decisões dele que valem: ver `Docs/DECISIONS.md` (ex.: as quatro primeiras montadas têm arco 360°; calibração de calor no CE fica como está; alcance CE usa o alcance do próprio CE; o morteiro M252 só existe se for realmente portátil).
- Você não consegue rodar o jogo. Entregue o trabalho pronto para teste e peça o log (`Player.log` do jogo) com o que ele observou.

## Estrutura
```
About/About.xml          metadados (precisa de Harmony)
LoadFolders.xml          1.6 sempre; 1.6/CE só com CETeam.CombatExtended
1.6/Defs/                Research.xml, Weapons.xml, Buildings.xml (vanilla)
1.6/CE/Patches/MountedArms_CE.xml   toda a camada CE
1.6/Assemblies/MountedArms.dll      compilado (NÃO versionado; ver Docs/TOOLING.md)
1.6/Languages/{English,PortugueseBrazilian}/Keyed/MountedArms.xml
1.6/Textures/MountedArms/<Nome>_{Base,Top,Icon}.png
Source/                  C# (MountedArms.cs, BarrelHeat.cs, SlewArc.cs, build.sh) — NÃO referencia CE
SourceCE/                C# só-CE (botão Descarregar, efeitos de lançamento no CE), build_ce.ps1 → 1.6/CE/Assemblies/MountedArmsCE.dll
SourceFx/                C# 5 (efeitos de lançamento, LaunchFxExtension), build_fx.ps1 → 1.6/Assemblies/MountedArmsFx.dll (com e sem CE)
Docs/                    regras, decisões, notas CE, status, ferramentas
tools/                   scripts de geração de textura e checagem de XML
```

## Regras de ouro (cada uma custou um bug)
1. **defName de ThingDef nunca termina em dígito.** Prefixo `MA_` (`MA_Turret_*`, `MA_Gun_*`, `MA_Research_*`, projéteis `MA_Bullet_*`/`MA_Missile_*`/`MA_Rocket_*`).
2. Patches XML rodam **antes** da herança: para mudar algo herdado, patchear a base abstrata (`@Name="MA_TurretBase"`). Listas (`li`) herdadas são **somadas**, não substituídas.
3. Projétil explosivo precisa de `forcedMissRadius` no verbo.
4. Comp de energia vai em cada torreta, nunca na base.
5. **Vanilla:** alcance de torreta não-morteiro < ~75 (AvoidGrid usa range+4 e o jogo só tem células até raio ~79,8; `DrawRadiusRing` quebra em 120). Torreta de alcance grande: `ai_combatDangerous=false` e sem `PlaceWorker_ShowTurretRadius`.
6. **CE:**
   - O tempo de mira vem de `warmupTime` do **verbo**; o CE ignora `turretBurstWarmupTime`.
   - Toda arma precisa de `FireModes` com `aiAimMode` AimedShot (sem isso: snapshot → "mira mas não dispara", bug do Mk19 e do TOW).
   - **Nunca** `aimedBurstShotCount` ≥ burst (só gera aviso e desliga o modo rajada; omita o campo).
   - Remover o comp `CompProperties_Refuelable` no patch (munição vem do CE).
   - Alcance: use os análogos do CE (`Docs/CE_NOTES.md`). Artilharia em CE: `Verb_ShootMortarCE` + `CompProperties_Charges`, **sem** `NonSnapTurretExtension`.
7. Arma de artilharia vanilla (`isMortar`) precisa de `<building><fixedStorageSettings>/<defaultStorageSettings>` na **gun** (senão NRE em `CompChangeableProjectile` no CE).
8. `CompProperties_BarrelHeat`, `CompProperties_TurretSlew` e as Harmony patches de arco/giro só afetam `Building_TurretGun` (vanilla); em CE (`Building_TurretGunCE` não herda dele) são inertes — o CE tem seus próprios sistemas (`NonSnapTurretExtension`, `CompFireArc`).
9. Botão "atacar tile do mundo" do CE em artilharia: escondido com `MountedArms.NoWorldStrikeExtension` (Harmony em `Building_TurretGunCE.GetGizmos`).
10. **Docs sempre atualizados:** toda edição atualiza os MDs afetados no mesmo commit (ver `Docs/RULES.md` §0).
11. **Edição de arquivos com replace em massa:** confira que o padrão casou na linha certa (já trocamos o `burstShotCount` do Mk19 em vez do da bateria). Depois de editar, valide o XML e releia o trecho.

## Fluxo para criar/alterar uma torreta
Use `Docs/TEMPLATE_NOVA_TORRETA.md` (checklist + esqueletos XML). Resumo: arma real + análogos vanilla/CE → gun/projétil/building/pesquisa/3 texturas (vanilla) → patch CE → checar (`tools/check_defnames.py`, `tools/check.py`, `tools/check_ce.py`, lxml) → compilar se mudou C# → testar vanilla **e** CE → atualizar `Docs/` → commit.

## Estado atual
Veja `Docs/STATUS.md`. Em resumo: M240/M134/M2/Mk 19/Mk44 testados (vanilla e CE); bateria APKWS (CE) corrigida e confirmada; Phalanx intercepta no CE (com a opção "Enable CIWS"); botão Descarregar e nomes reais confirmados. Bofors, ZU-23-2, Avenger, Goalkeeper, Iron Beam, TOW, B-8 e M252 ainda **não confirmados**. Companheiro: `../MountedArmsStrategic` (mísseis/artilharia estratégica, só-CE).

## Convenções
- Git: branch `main`; commits curtos e no imperativo. Não versione a DLL nem o `.git` de terceiros. Sem remote ainda (o usuário criará o remote).
- Idiomas: código/XML/defs em inglês; docs e conversa em português.
- Textos de jogador novos: Keyed em English **e** PortugueseBrazilian.
- Não adicione dependências ao About sem pedir.

## Índice dos docs
| Arquivo | Conteúdo |
|---|---|
| `README.md` | visão geral para humanos |
| `Docs/RULES.md` | regras do projeto, tabelas de alcance, sistemas de realismo |
| `Docs/DECISIONS.md` | decisões do usuário e do projeto, com o motivo |
| `Docs/TURRETS.md` | catálogo de cada torreta (defNames, custos, números vanilla e CE, status) |
| `Docs/CE_NOTES.md` | tudo que sabemos do CE (munições, projéteis, verbos, armadilhas) |
| `Docs/STATUS.md` | testes feitos, pendências, bugs abertos, próximos passos |
| `Docs/HISTORY.md` | linha do tempo dos problemas e correções |
| `Docs/TOOLING.md` | compilar, validar, texturas, caminhos, restrições do ambiente |
| `Docs/TEMPLATE_NOVA_TORRETA.md` | checklist + esqueletos para nova torreta |
