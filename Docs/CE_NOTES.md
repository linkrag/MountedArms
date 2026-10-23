# Notas sobre Combat Extended (o que sabemos, com a fonte)

Fonte local do CE: `F:\Steam\steamapps\workshop\content\294100\2890901044` (defs, patches, DLL; sem código C#). Código C# no GitHub: `CombatExtended-Continued/CombatExtended` (raw.githubusercontent.com/.../master/Source/CombatExtended/CombatExtended/...). Versão testada: 16.7.4.

## Classes / patch
- `CombatExtended.PatchOperationMakeGunCECompatible`: cria stats CE, `Properties` (verbo), `AmmoUser`, `FireModes`, `weaponTags`.
- Torreta: thingClass `CombatExtended.Building_TurretGunCE` (derivada de `Building_Turret`, **não** de `Building_TurretGun` → nossos patches Harmony vanilla de giro/arco/IsValidTarget não valem; a patch de gizmo é no `Building_TurretGunCE.GetGizmos`).
- Verbos: `Verb_ShootCE` (tiro direto), `Verb_ShootMortarCE` (artilharia).
- Giro: `CombatExtended.NonSnapTurretExtension` (`speed` em **graus por tick**, `angleWeightMultiplier`). Só para tiro direto.
- Origem do cano: `CombatExtended.MultiBarrelExtension` com `offsets` (lateral, frente) na gun: usamos (0, 0.6).
- Arco: `CompFireArc` (não usado hoje).
- Tempo de mira = `warmupTime` do verbo CE (não `turretBurstWarmupTime`).

## Armadilhas
1. **FireModes**: sempre `aiAimMode AimedShot`. Sem isso: snapshot → "mira e não dispara" (Mk19, TOW). Mk19 funcionou com `aiUseBurstMode FALSE`, `aiAimMode AimedShot`, `noSingleShot true`.
2. **aimedBurstShotCount ≥ burst**: só gera warning do CE ("burst fire shot count is same or higher than auto fire") e desliga o modo rajada; omita.
3. **Alcance e anel de colocação**: `PlaceWorker_ShowTurretRadius` quebra em raio 120 (log: "Cannot draw radius ring of radius 120"); mantenha ≤ ~100 em torretas não-morteiro.
4. **Munição APKWS 70 mm** (`AmmoSet_70mmAPKWS`/`Bullet_70mmAPKWS_HEAT`): projétil `flyOverhead` com speed 173 → só funciona como artilharia (`Verb_ShootMortarCE` + `CompProperties_Charges`). Usado direto em `Verb_ShootCE`, o voo dura mais de um minuto e não acerta.
5. **Foguete direto utilizável**: `AmmoSet_80mmRocket_direct` (S-8; HE/HEAT/Thermobaric; speed ~123–130). Outros diretos: 57 mm S5 (`AmmoSet_57mmRocket_direct`).
6. **Gizmo de ataque ao mundo**: `Command_ArtilleryTarget` aparece em `Building_TurretGunCE` quando `IsMortar`, ativo e a munição tem `shellingProps`. Escondemos via `NoWorldStrikeExtension`.
7. **Arma de artilharia com `CompProperties_ChangeableProjectile`** precisa de `building/fixedStorageSettings` na gun, senão `NullReferenceException` em `CompChangeableProjectile.GetParentStoreSettings` ao construir a torreta no CE.
8. O CE troca os verbos do `Artillery_Mortar` vanilla por `Verb_ShootMortarCE` e põe `Charges` (30/50/70/90) + `AmmoUser` (mag 1, reload 5); também patcha `BaseArtilleryBuilding` (thingClass, cooldown 2, Bulk 200, WorkToBuild 9000, remove inspectorTabs) — o M252 herda isso por ser `BaseArtilleryBuilding`.
9. `ProjectilePropertiesCE`: `gravityFactor`, `trajectoryWorker`, `shellingProps`, `isInstant`, `speed`. Altura/queda são calculadas por ângulo+velocidade+gravidade; em `Verb_ShootMortarCE` a velocidade vem da carga (`chargeSpeeds`).

## Alcances de referência (CE)
M240B 62 · Minigun 62 · AGS-30 62 (min 8) · KPV 75 · Autocannon 78 · Sniper turret 86 · Flak 92 (min 16) · CIWS (CE) 55/105 · Medium/Heavy turret 55 · Mortar 700 (min 32). Torreta de mísseis do Glitter Tech: 500 (min 30), burst 25, mag 25, reload 5, `noSnapshot` + `noSingleShot`.

## Munições usadas (AmmoSetDef)
AmmoSet_762x51mmNATO · AmmoSet_50BMG · AmmoSet_40x53mmGrenade · AmmoSet_30x173mmNATO (AP) · AmmoSet_BGM71 (Bullet_BGM71_HEAT, speed 55, dano 286, não é flyOverhead) · AmmoSet_80mmRocket_direct · AmmoSet_20x102mmNATO (AP) · AmmoSet_81mmMortarShell (HE) · AmmoSet_70mmAPKWS.

## Como o dano/alcance é "balanceado" no CE
O CE não usa um número fixo: dano vem da munição; limites práticos são cadência, tamanho do carregador, tempo de recarga, `ShotSpread`/`SwayFactor`/`SightsEfficiency` e `Bulk`. Para calibrar uma arma nova, copie o patch do análogo CE mais próximo.
