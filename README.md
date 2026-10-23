# Mounted Arms

Mod de RimWorld 1.6 que adiciona **torretas baseadas em armas montadas modernas**, com balanceamento "vanilla-friendly" e uma camada de compatibilidade com **Combat Extended** (carregada só quando o CE está ativo). Requer **Harmony**; nenhum DLC.

- packageId: `linkrag.mountedarms` · autor: Felipe
- Aba de pesquisa própria: "Mounted Arms"

## Torretas
| Torreta | Tipo | Resumo |
|---|---|---|
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
| Bofors 40 mm duplo / quádruplo | tripulada, 360° | antiaéreo naval L/60; no CE intercepta projéteis e drop pods |

Detalhes e números: `Docs/TURRETS.md`.

## Recursos
- Superaquecimento do cano, velocidade de giro (slew) e dispersão por calor/rajada (vanilla); no CE usa os sistemas do próprio CE.
- Projétil e clarão saem do cano (patch Harmony).
- Vanilla: o cano consome aço. CE: munição do CE (7,62x51, .50 BMG, 40x53, 30x173, BGM-71, 80 mm S-8, 20x102, 81 mm...).
- Explosão ao tomar dano (`CompProperties_Explosive`).

## Instalação / desenvolvimento
Pasta do mod em `RimWorld/Mods/MountedArms`. A DLL (`1.6/Assemblies/MountedArms.dll`) não é versionada: compile com `Source/build.sh` (ver `Docs/TOOLING.md`). Ordem de carga: depois de Harmony, DLCs e CE.

## Documentação do projeto
`AGENTS.md` (guia para agentes de código — comece por ele), `Docs/RULES.md`, `Docs/DECISIONS.md`, `Docs/TURRETS.md`, `Docs/CE_NOTES.md`, `Docs/STATUS.md`, `Docs/HISTORY.md`, `Docs/TOOLING.md`, `Docs/TEMPLATE_NOVA_TORRETA.md`.
