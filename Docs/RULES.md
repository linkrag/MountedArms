# Mounted Arms — regras do projeto

Documento de referência para criar novas torretas sem quebrar o que já foi acertado.
packageId: `linkrag.mountedarms` · RimWorld 1.6 e 1.7 · Depende de Harmony · CE opcional.

## 0. Documentação
- **Depois de toda implementação ou modificação, atualize os MDs afetados** (STATUS, TURRETS, DECISIONS, CE_NOTES, HISTORY, TOOLING, MIGRATION_1_7, README, AGENTS e o CLAUDE.md quando o fluxo mudar) no mesmo commit. Pedido do usuário: os docs são a memória do projeto entre sessões. Vale também para o Mounted Arms Strategic e o Bill Organizer, e a regra está escrita nos `CLAUDE.md` (lidos por padrão) de `Mods/` e de cada mod.

## 1. Estrutura
- `About/About.xml`, `LoadFolders.xml` (1.6 e 1.7: conteúdo em `1.6/`, DLLs em `Bin/<versão>`; `1.6/CE` e `Bin/<versão>/CE` só carregam com `CETeam.CombatExtended`).
- `1.6/Defs`: Research.xml, Weapons.xml, Buildings.xml, DesignationCategories.xml (aba "Militar" do Architect) · `1.6/Textures/MountedArms/<Nome>_{Base,Top,Icon}.png`
- `Bin/<versão>/Assemblies/MountedArms.dll` e `MountedArmsFx.dll`, `Bin/<versão>/CE/Assemblies/MountedArmsCE.dll` ← `build.ps1` (SDK .NET 10, as duas versões; ver `Docs/TOOLING.md`).
- `1.6/CE/Patches/MountedArms_CE.xml`: toda a camada CE.

## 2. Regras de defs (erros já cometidos)
- defName de ThingDef **nunca termina em dígito** (use `_MG`, `_AGL`, `x51mm`…).
- Prefixo `MA_`: `MA_Turret_*`, `MA_Gun_*`, `MA_Bullet_*`, `MA_Research_*`.
- Projétil explosivo (e só ele) precisa de `forcedMissRadius` (1.9 como o lança-granadas vanilla) no verbo.
- Comp de energia vai **em cada torreta**, nunca na base abstrata (duplica CompPowerTrader).
- Patches XML rodam antes da herança: para mudar algo herdado, patchear a base abstrata (`@Name="MA_TurretBase"`).
- Todo turret: ThingDef + gun + projétil + pesquisa + 3 texturas + entrada na camada CE.
- **Aba do Architect:** `<designationCategory>MA_Military</designationCategory>` (herdada de `MA_TurretBase`; base vanilla, como o M252, declara explicitamente). Prédio novo do Strategic entra pelo patch `MountedArmsStrategic/1.6/MountedArms/Patches/MilitaryCategory.xml`.
- Explosão ao tomar dano: `CompProperties_Explosive` (mantido também no CE).

## 3. Texturas
- Topo (`_Top`) aponta para **LESTE**; pivô = centro do canvas; cano ~0,6 célula à frente do pivô.
- `turretTopDrawSize` ajustado por arma. Gerador: `gen_tex.py`.
- Origem do projétil/flash: vanilla = Harmony (`MuzzleExtension` distance/flashScale, verbo com `muzzleFlashScale` 0); CE = `CombatExtended.MultiBarrelExtension` offset (0, 0.6) na gun.

## 4. Operação
- Automática (energia): precisa de gerador, cadência alta, mira lenta.
- Manual (`CompProperties_Mannable`, célula de interação): mais precisa, sem energia.
- Vanilla: barril consome aço (`CompProperties_Refuelable`, `consumeFuelPerShot` 1). CE: sem refuel — usa munição do CE (remover o comp no patch).

## 5. Balanceamento
**Vanilla (vanilla-friendly):** referências = mini-turret (28,9), fuzil (25,9), sniper (41,5), lança-granadas (≈38,9).
| Arma | alcance | observação |
|---|---|---|
| M240 | 31,9 | auto, 100 W |
| M134 | 28,9 | auto, 350 W, burst 16 |
| M2 | 40,9 | manual |
| Mk19 | 38,9 (min 8,9) | manual, caro, tech avançada |
| Mk44 30 mm | 44,9 | auto, 250 W, pesquisa MA_Research_Autocannon, T de calor 75 s |
| TOW ATGM | 71,9 (min 14,9) | tripulada, 1 mísseis/tiro, pesquisa MA_Research_ATGM, sem calor |
| Foguetes 80mm (S-8) | 49,9 (min 9,9) | auto, 200 W, salva de 7, pesquisa MA_Research_Rockets, sem calor |
| CIWS 20mm | 33,9 | auto, 450 W, rajada 60, pesquisa MA_Research_CIWS, T de calor ~60 s |
| Morteiro M252 81mm | 200 (min 19,9) | tripulada, PORTÁTIL (minifiável), WorkToBuild 1200, Mass 12, pesquisa MA_Research_Mortar |

**CE:** usar o alcance das torretas equivalentes do próprio CE (considerado balanceado).
| Arma | alcance CE | análogo CE |
|---|---|---|
| M240 | 62 | Gun_M240B |
| M134 | 62 | Gun_Minigun |
| Mk19 | 62 (min 8) | Gun_AGSThirty |
| M2 | 75 | Gun_KPV |
| Mk44 | 78 | Gun_AutocannonTurret (AmmoSet_30x173mmNATO) |
| TOW | 100 (min 24) | acima do Gun_SniperTurret (86), míssil guiado de longo alcance; AmmoSet_BGM71 |
| Foguetes 80mm | 62 (min 12) | AmmoSet_80mmRocket_direct (o APKWS 70mm do CE é projétil aéreo e demora muito) |
| CIWS 20mm | 68 | AmmoSet_20x102mmNATO |
| M252 | 450 (min 24) | mortar do CE tem 700; M252 é mais curto, cargas 30/50/70 |
Outras âncoras CE: MediumTurret 55, HeavyTurret 55, Autocannon 78, Sniper turret 86, Flak 92 (min 16), CIWS 55/105.

- Tempo de mira no CE vem do **warmupTime do verbo** (CE ignora `turretBurstWarmupTime`). Vanilla usa o do building.
- CE: stats em `statBases` (Bulk, ShotSpread, SwayFactor, SightsEfficiency), `AmmoUser` (magazineSize, reloadTime, ammoSet), `FireModes`.
- Custo cresce com: tech level, componentes (Industrial → Spacer), plasteel, WorkToBuild, pesquisa.
- Habilidade do operador **não** altera a precisão da torreta manual (só o stat do building).

## 6. Fluxo de trabalho
1. Definir arma real + análogo vanilla/CE (alcance, munição, cadência).
2. Criar gun, projétil, building, pesquisa, texturas (vanilla).
3. Criar patch CE (MakeGunCECompatible + MultiBarrel + building).
4. Checar: referências, defNames, texturas, XML do patch (scripts `check.py`, `check_ce.py`).
5. Compilar DLL se mudou C#.
6. Testar vanilla e CE: construir, energia/operador, mirar, atirar, recarregar, tomar dano (explosão), ver log.
- Bug CE conhecido/corrigido: Mk19 mirava e não atirava; causa: `FireModes` ausente/errado (snapshot). Resolvido com `aiAimMode AimedShot`, `aiUseBurstMode FALSE`, `noSingleShot` e sem `noSnapshot` (ver Docs/CE_NOTES.md).

## 6b. Superaquecimento do cano (implementado)
- `MountedArms.CompProperties_BarrelHeat` (Source/BarrelHeat.cs), vale para vanilla e CE (usa só API pública + o campo `burstCooldownTicksLeft`).
- Calor 0..1; cada tiro soma `heatPerShot`, esfria `coolPerSecond`/s. Em 1.0 a torreta trava (não inicia rajadas) até cair a `resumeAt`; fumaça acima de `smokeAt`; texto no painel e mensagem ao jogador.
- Fórmula para calibrar: `heatPerShot = (1/T + coolPerSecond) / tirosPorSegundo`, onde T = segundos de fogo contínuo até superaquecer e tirosPorSegundo = burst / (warmup + (burst-1)*ticks/60 + cooldown). Alvos de T: M240 60 s, M134 40 s, M2 90 s, Mk19 120 s (coolPerSecond 0.02).
- CE dispara mais rápido (cooldown menor): valores de `heatPerShot` diferentes, trocados no patch CE (PatchOperationReplace por defName).
- Textos em `1.6/Languages/{English,PortugueseBrazilian}/Keyed`.
- Pendente de teste em jogo; ajustar T se travar cedo/tarde demais.

## 6c-a. (decisão: as quatro montadas têm arco de 360°, `arcDegrees` 0 e sem CompFireArc no CE; o sistema de arco fica pronto para torretas futuras que tenham arco limitado)
## 6c. Giro, arco e dispersão (implementado, pendente de teste)
- **Vanilla** (`Source/SlewArc.cs`, `CompProperties_TurretSlew`): topo gira `degreesPerSecond` (Harmony em `TurretTop.TurretTopTick`) e a rajada só começa com o cano a menos de `aimTolerance`° do alvo; `arcDegrees` limita o campo de tiro (centro = rotação do prédio; só faz sentido nas manuais, que são rotacionáveis); alvos fora do arco são recusados (`IsValidTarget`/`OrderAttack`). Linhas do arco aparecem ao selecionar.
- **CE**: a mesma coisa usa os sistemas do CE: `CombatExtended.NonSnapTurretExtension` (`speed` em graus POR TICK) e `CompProperties_FireArc` (M2 e Mk19). O comp vanilla fica inerte em `Building_TurretGunCE`.
- **Dispersão vanilla** (`CompProperties_BarrelHeat.heatSpread/burstSpread`, patch em `Projectile.Launch`): erro de mira em células (a 20 células) = calor*heatSpread + tirosNaRajada*burstSpread. No CE o recuo/dispersão já é do próprio CE.
- Velocidades: vanilla 55/40/40/30 °/s (M240/M134/M2/Mk19); CE 0.9/0.65/0.65/0.5 °/tick (CE = vanilla ÷ 60).
- Ajuste por realismo (out/2026): CIWS 100 °/s (servo tipo Phalanx; CE 1,67) e 700 W; Bofors manual (volantes) duplo 25 °/s (CE 0,42), quádruplo 20 °/s (CE 0,33), sem energia. Os Bofors navais reais tinham acionamento elétrico-hidráulico (~25–30 °/s); mantidos manuais por decisão do usuário.

## 7. Próximas melhorias de realismo
**Vanilla**
- Munição em cinta/caixa: capacidade e recarga manual em vez de só aço.
- Tripé/montagem: tempo de instalação, ou bônus quando parada vs. móvel.
- Ruído/alerta: tiro pesado atrai inimigos; flash de cano diurno/noturno.
- Estojos ejetados (fleck/filth) como o CE.
- Som e flash por arma; sombra e animação de recuo no sprite.
- Dano a estruturas/cobertura por calibre (.50 e granada atravessam).
- Linhas de pesquisa mais fiéis (calibre → sistemas).
- Variantes: montagem em veículo/bunker, versão leve/portátil.
**CE**
- Munições alternativas por arma (AP, tracer, incendiária, HE/HEDP no Mk19) com `AmmoSet` próprio.
- Alimentador/autoloader adjacente para torretas automáticas.
- Modos de tiro e supressão ajustados por arma; estabilidade com bipé/tripé.
- Spread/Sway/Bulk por montagem; blindagem do shield da torreta.
- Granada em arco (lobbed) e alcance/ângulo mínimo realista para AGL.
- Estoques de munição e custo de produção coerentes com o ecossistema CE.
- Patches opcionais para mods populares (ex.: pacote de munição extra).
**Novas torretas (candidatas)**
- Canhão automático 30 mm, ATGM (míssil guiado, mínimo/máximo), CIWS (base: `CIWSExample.xml` do CE), morteiro leve, torre antiaérea.


## Decisão: morteiro portátil
O M252 só faz sentido se for realmente móvel: é um prédio minifiável (empacota em item, vai em caravana, reinstala rápido), leve (Mass 12), barato e de montagem curta (WorkToBuild 1200), mais preciso e de alcance menor que o morteiro pesado.

## Limites de raio do jogo
- Vanilla: `AvoidGrid` das torretas usa `range + ~4`; `GenRadial` só tem células até raio ~79,8, então o range vanilla de uma torreta (Building_TurretGun) deve ficar **abaixo de ~75** (exceto morteiros).
- `DrawRadiusRing` (colocação) falha com raio 120; manter range CE ≤ ~100 para torretas não-morteiro.
- CE: toda arma com burst 1 também precisa de `<FireModes><aiAimMode>AimedShot</aiAimMode></FireModes>` (sem isso o padrão é snapshot e a torreta mira mas não dispara, como no Mk19 e TOW). Exceção: arma de fogo contínuo em tiro único (Gatling) usa `SuppressFire` sem `noSnapshot`, porque em torreta o `AimedShot` soma `Lerp(30, 240, dist/100)` ticks de mira a **cada** rajada (`Verb_ShootCE.WarmupComplete`); as torretas do próprio CE (`Gun_M240B`, `Gun_AGSThirty`) usam SuppressFire.

## Bateria de foguetes guiados (fogo indireto, estilo morteiro)
- `MA_Turret_APKWS_Battery`: auto, 250 W, pesquisa `MA_Research_Missiles`. Fogo em arco, alvo em ponto do chão, rajada de 6, sem calor. Botão "atacar mundo" escondido (`NoWorldStrikeExtension`).
- Vanilla: verbo `isMortar` + projétil `flyOverhead`, range 500 (= morteiro vanilla), min 29,9, forcedMissRadius 5 (morteiro: 9), cooldown 22, mira 3,0 s, `ai_combatDangerous` false, `placeWorkers Inherit="False"` só com TurretTop (anel de raio e AvoidGrid quebram com alcance grande).
- CE: `Verb_ShootMortarCE` range 700, min 32, `CompProperties_Charges` 30/50/70/90, mag 24, reload 8, `noSnapshot`/`noSingleShot`, sem `NonSnapTurretExtension`. Bug aberto: tiros fora do mapa (ver Docs/STATUS.md).
