# Mounted Arms

Mod de RimWorld 1.6 e 1.7 que adiciona **torretas baseadas em armas montadas modernas**, com balanceamento "vanilla-friendly" e uma camada de compatibilidade com **Combat Extended** (carregada só quando o CE está ativo). Requer **Harmony**; nenhum DLC.

- packageId: `linkrag.mountedarms` · autor: Felipe
- Aba de pesquisa própria: "Mounted Arms"
- Aba própria "Militar" no menu de construção (Architect), compartilhada com o Mounted Arms: Strategic quando os dois estão ativos

## Torretas
| Torreta | Tipo | Resumo |
|---|---|---|
| Gatling | tripulada, sem energia | 10 canos na manivela, .45-70; a primeira torreta (só Gunsmithing) |
| M240 | automática (energia) | metralhadora de uso geral 7,62 mm |
| M134 Minigun | automática | rotativa 7,62 mm, rajada longa |
| M2 Browning | tripulada | .50 BMG, longo alcance |
| Mk19 | tripulada | lançador de granadas 40 mm |
| Mk44 Bushmaster | automática | canhão 30 mm |
| TOW | tripulada | míssil anti-blindado, 1 tiro, alcance longo |
| Foguetes 80 mm | automática | salva de 7 foguetes diretos |
| CIWS 20 mm | automática | rotativa 20 mm, rajada de 60 |
| Morteiro M252 | tripulada, **portátil** | 81 mm, minifiável, montagem rápida |
| Bateria de foguetes guiados | automática | fogo indireto em arco, como morteiro |
| ZU-23-2 | tripulada | 23 mm duplo leve e barato; no CE intercepta projéteis e drop pods |
| Avenger (Stinger) | automática | vanilla: mísseis leves contra o chão; CE: só abate drop pods |
| Goalkeeper 30 mm | automática | CIWS pesado de 7 canos; no CE intercepta projéteis |
| Sistema laser | automática (2000 W) | sem munição; no CE intercepta projéteis |
| Bofors 40 mm duplo / quádruplo | tripulada, 360° | antiaéreo naval L/60; no CE intercepta projéteis e drop pods |

Detalhes e números: `Docs/TURRETS.md`.

## Recursos
- Superaquecimento do cano, velocidade de giro (slew) e dispersão por calor/rajada (vanilla); no CE usa os sistemas do próprio CE.
- Projétil e clarão saem do cano (patch Harmony).
- Vanilla: o cano consome aço. CE: munição do CE (7,62x51, .50 BMG, 40x53, 30x173, BGM-71, 80 mm S-8, 20x102, 81 mm...).
- Explosão ao tomar dano (`CompProperties_Explosive`).

## Instalação / desenvolvimento
Fonte em `RimWorld/_dev/src/MountedArms`; o jogo carrega a cópia em `RimWorld/Mods/MountedArms` que o `build.ps1` publica (`tools/deploy.ps1`: só About, LoadFolders.xml, 1.6, Bin). As DLLs (`Bin/1.6`, `Bin/1.7`) não são versionadas: compile com `powershell -File build.ps1` (SDK .NET 10; ver `Docs/TOOLING.md`). Ordem de carga: depois de Harmony, DLCs e CE.

## Documentação do projeto
`AGENTS.md` (guia para agentes de código — comece por ele), `Docs/RULES.md`, `Docs/DECISIONS.md`, `Docs/TURRETS.md`, `Docs/CE_NOTES.md`, `Docs/STATUS.md`, `Docs/HISTORY.md`, `Docs/TOOLING.md`, `Docs/TEMPLATE_NOVA_TORRETA.md`, `Docs/MIGRATION_1_7.md`. Regra: toda implementação ou modificação atualiza esses MDs no mesmo commit.
