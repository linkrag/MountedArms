# Catálogo de torretas

Todas aparecem na aba **Militar** do Architect (`MA_Military`, desde 2/nov/2026, não testada no jogo; o Strategic usa a mesma aba por patch). Valores conferidos nos XML em out/2026. "Testado" = confirmado pelo usuário em jogo. Custos: Steel/Plasteel/CompInd (ComponentIndustrial)/CompSp (ComponentSpacer). Todas têm `CompProperties_Explosive` (explode ao tomar dano), `CompProperties_TurretSlew` (arcDegrees 0 = 360°) e MuzzleExtension (exceto morteiro/bateria).

## Vanilla
| defName (turret / gun) | Tipo / base | Custo | Energia | WorkToBuild | Pesquisa | Verbo (alcance, min, rajada, ticks) | Warmup / cooldown | Status |
|---|---|---|---|---|---|---|---|---|
| MA_Turret_M240_MG / MA_Gun_M240_MG | auto (MA_AutoTurretBase) | 220/0/4/0 | 100 W | 9000 | MA_Research_GPMG | 31,9 · – · 5 · 5 | 0,6 / 3,4 | testado |
| MA_Turret_M134_Minigun / MA_Gun_M134_Minigun | auto | 320/40/8/0 | 350 W | 18000 | MA_Research_Rotary | 28,9 · – · 16 · 3 | 1,2 / 4,2 | testado |
| MA_Turret_Gatling / MA_Gun_Gatling | tripulada (carreta de madeira; +60 WoodLog) | 140/0/2/0 | – | 6000 | MA_Research_Gatling | 29,9 · – · 1 (tiro único contínuo) | 0 / 0,15 | testado (vanilla e CE) |
| MA_Turret_M2_Browning / MA_Gun_M2_Browning | tripulada (MA_MannedTurretBase) | 260/0/3/0 | – | 10000 | MA_Research_HMG | 40,9 · – · 4 · 9 | 1,0 / 3,4 | testado |
| MA_Turret_Mk19_AGL / MA_Gun_Mk19_AGL | tripulada | 400/80/8/2 | – | 20000 | MA_Research_AGL | 38,9 · 8,9 · 4 · 16 | 1,6 / 4,5 | testado |
| MA_Turret_Mk44_Autocannon / MA_Gun_Mk44_Autocannon | auto | 450/90/10/0 | 250 W | 22000 | MA_Research_Autocannon | 44,9 · – · 6 · 10 | 1,8 / 3,0 | testado |
| MA_Turret_TOW_ATGM / MA_Gun_TOW_ATGM | tripulada | 300/60/6/2 | – | 22000 | MA_Research_ATGM | 71,9 · 14,9 · 1 | 2,5 / 8,0 | NÃO confirmado |
| MA_Turret_Hydra_Pod / MA_Gun_Hydra_Pod | auto (foguetes 80mm S-8; defNames guardam "Hydra/70mm" por histórico) | 350/50/8/0 | 200 W | 20000 | MA_Research_Rockets | 49,9 · 9,9 · 7 · 5 | 2,4 / 5,5 | NÃO confirmado |
| MA_Turret_CIWS_Vulcan / MA_Gun_CIWS_Vulcan | auto | 400/120/8/2 | 700 W | 30000 | MA_Research_CIWS | 33,9 · – · 60 · 2 | 0,8 / 3,0 | NÃO confirmado |
| MA_Turret_M252_Mortar / MA_Gun_M252_Mortar | tripulada, portátil (BaseArtilleryBuilding, minifiável, Mass 12) | 30/0/3/0 | – | 1200 | MA_Research_Mortar | 200 · 19,9 · 1 (isMortar) | 3,0 / 14,0 | NÃO confirmado |
| MA_Turret_Bofors_Twin / MA_Gun_Bofors_Twin | tripulada 2x2 | 380/0/6/0 | – | 16000 | MA_Research_Bofors | 42,9 · – · 4 · 15 | 1,4 / 3,5 | NÃO confirmado |
| MA_Turret_Bofors_Quad / MA_Gun_Bofors_Quad | tripulada 3x3 (interação (0,0,-2)) | 600/60/10/0 | – | 26000 | MA_Research_BoforsQuad | 42,9 · – · 8 · 8 | 1,6 / 3,5 | NÃO confirmado |
| MA_Turret_ZU23_AA / MA_Gun_ZU23_AA | tripulada 2x2 | 260/0/4/0 | – | 9000 | MA_Research_ZU23 | 36,9 · – · 10 · 3 | 1,0 / 3,0 | NÃO confirmado |
| MA_Turret_Avenger / MA_Gun_Avenger | auto 2x2 | 240/0/6/0 | 150 W | 14000 | MA_Research_Stinger | 49,9 · 7,9 · 2 · 40 | 2,0 / 8,0 | NÃO confirmado |
| MA_Turret_Goalkeeper / MA_Gun_Goalkeeper | auto 2x2 | 550/150/12/3 | 900 W | 34000 | MA_Research_Goalkeeper | 38,9 · – · 40 · 1 | 0,6 / 3,5 | NÃO confirmado |
| MA_Turret_LaserCIWS / MA_Gun_LaserCIWS | auto 2x2 (+20 ouro) | 300/120/8/4 | 2000 W | 30000 | MA_Research_LaserCIWS | 44,9 · – · 3 · 10 | 1,5 / 2,0 | NÃO confirmado |
| MA_Turret_APKWS_Battery / MA_Gun_APKWS_Battery | auto, fogo indireto (isMortar, projétil flyOverhead) | 380/60/8/1 | 250 W | 26000 | MA_Research_Missiles | 500 · 29,9 · 6 · 10 | 3,0 / 22,0 | NÃO confirmado |

Notas vanilla:
- Calor (CompProperties_BarrelHeat): M240/M134/M2/Mk19/Mk44/CIWS (alvos de T: 60/40/90/120/75/60 s); Gatling T 15 s de fogo contínuo (0,0130; heatSpread 2,5, burstSpread 0). TOW, foguetes, morteiro e bateria não têm calor.
- Refuelable (aço): barril (M240...), mísseis (TOW cap 4), foguetes (cap 21), CIWS (cap 1200, mult 10), M252 (cap 30), bateria (cap 24).
- Gatling (Colt M1883, 10 canos, .45-70, tambor Accles 104, ~600 rpm sustentado na manivela): a torreta mais antiga do mod. MA_Research_Gatling (600, prereq vanilla Gunsmithing, **sem** GunTurrets nem bancada avançada) e virou pré-requisito de MA_Research_Rotary (M134 = "Gatling elétrica"). **Fogo contínuo** (vanilla e CE): rajada 1, mira 0 e cooldown curto da torreta, então atira sem parar e reescolhe o alvo a cada tiro (`Building_TurretGun`/`Building_TurretGunCE` procuram alvo a cada ciclo); quem para é o calor (e o tambor no CE). Vanilla: 0,15 s, mas o `Building_TurretGun.Tick` só tenta atirar em `IsHashIntervalTick(10)` (código 1.0; 1.6 não conferido), então ~10 ticks por tiro ≈ 360 rpm (6 tiros/s; um colono no lugar de uma guarnição de 4), 14 dano / AP 0,20 / bala 60, precisão 0,40/0,30/0,18/0,08, ShootingAccuracyTurret 0,90. Ciclo: ~15 s de fogo a frio, depois ~7,5 s de fogo e 25 s travada (≈23% do tempo atirando, ~21 de DPS bruto sustentado; forte de perto, ruim de longe). Fumaça de pólvora negra a cada tiro via `MountedArms.LaunchFxExtension` na gun (ejectPuffs 1, puffSize 0,6, flashSize 0). Explosão 2,9; giro 30 °/s; barril 600 tiros (~90 s), 60 aço por recarga completa.
- Pesquisas extras: MA_Research_Mortar (prereq vanilla Mortars), MA_Research_ATGM (AGL), MA_Research_Rockets (HMG+Mortars), MA_Research_CIWS (Rotary+Autocannon), MA_Research_Missiles (Rockets+ATGM).

## Combat Extended (camada em `1.6/CE/Patches/MountedArms_CE.xml`)
| Arma | Munição (AmmoSet → projétil padrão) | alcance (min) | warmup | burst × ticks | carregador / recarga | Notas |
|---|---|---|---|---|---|---|
| M240 | AmmoSet_762x51mmNATO → Bullet_762x51mmNATO_FMJ | 62 | 1,0 | 10 × 6 | 100 / 8,5 | |
| M134 | AmmoSet_762x51mmNATO | 62 | 2,0 | 30 × 2 | 300 / 9,2 | |
| Gatling | AmmoSet_4570Gov → Bullet_4570Gov_FMJ | 55 (= rifle por ferrolho do CE) | 0 | 1 (tiro único, cooldown da torreta 0,1 s = 600 rpm) | 104 / 10 (tambor Accles, ~10,4 s de fogo) | FireModes só `aiAimMode SuppressFire` (sem noSnapshot; AimedShot mirava 30–240 ticks antes de cada tiro); ShotSpread 0,15, Sway 1,6, SightsEfficiency 0,8, AimingAccuracy 0,60, ShootingAccuracyTurret 0,80 |
| M2 | AmmoSet_50BMG → Bullet_50BMG_FMJ | 75 | 1,8 | 6 × 7 | 100 / 9 | |
| Mk19 | AmmoSet_40x53mmGrenade → Bullet_40x53mmGrenade_HE | 62 (8) | 2,2 | 4 × 10 | 32 / 9,5 | testado em todas as munições |
| Mk44 | AmmoSet_30x173mmNATO → Bullet_30x173mmNATO_AP | 78 | 2,0 | 6 × 12 | 60 / 9,5 | |
| TOW | AmmoSet_BGM71 → Bullet_BGM71_HEAT | 100 (24) | 2,5 | 1 | 1 / 8 | FireModes só com aiAimMode AimedShot |
| Foguetes | AmmoSet_80mmRocket_direct → Bullet_80mmRocket_HE | 62 (12) | 2,4 | 7 × 5 | 21 / 9 | NÃO usar o APKWS 70mm direto (projétil flyOverhead, voo de minutos) |
| CIWS | AmmoSet_20x102mmNATO → Bullet_20x102mmNATO_AP | 68 | 1,0 | 60 × 2 | 600 / 10 | |
| M252 | AmmoSet_81mmMortarShell → Bullet_81mmMortarShell_HE | 450 (24) | 3,5 | 1 | 1 / 3 | Verb_ShootMortarCE; cargas 30/50/70 |
| Bofors duplo | AmmoSet_40x311mmR → Bullet_40x311mmR_HE | 86 | 1,6 | 4 × 15 | 16 / 6 | `Building_CIWS_CE`; CIWS projéteis 100, drop pods 125 |
| Bofors quádruplo | AmmoSet_40x311mmR → Bullet_40x311mmR_HE | 86 | 1,8 | 8 × 8 | 32 / 8 | idem |
| Bateria | MA_AmmoSet_APKWS_Indirect → MA_Bullet_APKWS_Indirect_HE (gravityFactor 5; item Ammo_70mmAPKWS_HEAT) | 700 (32) | 3,0 | 6 × 10 | 24 / 8 | Verb_ShootMortarCE; cargas 30/50/70/90; sem NonSnap |

NonSnapTurretExtension (graus por TICK): Gatling 0,5 · M240 0,9 · M134 0,65 · M2 0,65 · Mk19 0,5 · Mk44 0,6 · TOW 0,5 · Foguetes 0,65 · CIWS 1,67 · Bofors duplo 0,42 · quádruplo 0,33 · (M252 e bateria: nenhum).
CIWS 20 mm no CE: `Building_CIWS_CE` + verbo `VerbCIWSProjectile` (alcance 90, rajada 30) além do tiro no chão.
heatPerShot no CE: Gatling 0,0064 (superaquece no 4º tambor seguido) · Bofors duplo 0,0330 · quádruplo 0,0181 · M240 0,0106 · M134 0,0067 · M2 0,0186 · Mk19 0,0333 · Mk44 0,0250 · CIWS 0,0028.
