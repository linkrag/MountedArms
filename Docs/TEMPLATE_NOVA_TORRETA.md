# Molde: adicionar uma torreta nova

Troque `XXX` (nome), os números e os textos. Siga RULES.md.

## Checklist
1. Escolher arma real + análogos: vanilla (alcance/cadência) e CE (Gun_* do CE em `Defs/ThingDefs_Misc/Weapons_Turrets.xml` e `Patches/Core/ThingDefs_Misc/Weapons_Guns.xml`).
2. Texturas: `XXX_Base`, `XXX_Top` (aponta para leste), `XXX_Icon` (gen_tex.py).
3. Weapons.xml: projétil `MA_Bullet_XXX` + gun `MA_Gun_XXX` (sem dígito no fim do defName).
4. Buildings.xml: turret `MA_Turret_XXX` (filho de `MA_AutoTurretBase` ou `MA_MannedTurretBase`).
5. Research.xml: `MA_Research_XXX`.
6. Calcular `heatPerShot` (fórmula em RULES.md 6b) vanilla e CE.
7. Patch CE (`MountedArms_CE.xml`): MakeGunCECompatible, MultiBarrelExtension, building (statBases, cooldown, remover Refuelable) e troca de `heatPerShot`.
8. Rodar `check.py` e `check_ce.py`; compilar DLL se mudou C#.
9. Testar vanilla e CE: construir, energia/operador, mirar, atirar, recarregar, superaquecer, tomar dano.

## Turret (Buildings.xml)
```xml
<ThingDef ParentName="MA_AutoTurretBase">
  <defName>MA_Turret_XXX</defName>
  <label>XXX</label>
  <description>...</description>
  <graphicData><texPath>MountedArms/XXX_Base</texPath><graphicClass>Graphic_Single</graphicClass><drawSize>(2,2)</drawSize></graphicData>
  <uiIconPath>MountedArms/XXX_Icon</uiIconPath>
  <costList><Steel>250</Steel><ComponentIndustrial>4</ComponentIndustrial></costList>
  <building>
    <turretGunDef>MA_Gun_XXX</turretGunDef>
    <turretBurstWarmupTime>1.0</turretBurstWarmupTime>
    <turretBurstCooldownTime>3.0</turretBurstCooldownTime>
    <turretTopDrawSize>2.1</turretTopDrawSize>
  </building>
  <comps>
    <li Class="CompProperties_Power"><compClass>CompPowerTrader</compClass><basePowerConsumption>100</basePowerConsumption></li>
    <li Class="CompProperties_Explosive"><explosiveRadius>3.9</explosiveRadius><explosiveDamageType>Bomb</explosiveDamageType><startWickOnDamageTaken><li>Bullet</li></startWickOnDamageTaken></li>
    <li Class="MountedArms.CompProperties_BarrelHeat"><heatPerShot>0.03</heatPerShot><coolPerSecond>0.02</coolPerSecond><resumeAt>0.5</resumeAt><smokeAt>0.7</smokeAt></li>
    <li Class="CompProperties_Refuelable">...barril de aço (só vanilla)...</li>
  </comps>
  <modExtensions><li Class="MountedArms.MuzzleExtension"><distance>0.6</distance><flashScale>9</flashScale></li></modExtensions>
</ThingDef>
```
(Copie a estrutura real de uma turret existente; este bloco é só o esqueleto.)

## Patch CE (MountedArms_CE.xml)
```xml
<Operation Class="CombatExtended.PatchOperationMakeGunCECompatible">
  <defName>MA_Gun_XXX</defName>
  <statBases><RangedWeapon_Cooldown>0.5</RangedWeapon_Cooldown><SightsEfficiency>1</SightsEfficiency><ShotSpread>0.1</ShotSpread><SwayFactor>1.2</SwayFactor><Bulk>20</Bulk></statBases>
  <Properties><recoilAmount>1.0</recoilAmount><verbClass>CombatExtended.Verb_ShootCE</verbClass><hasStandardCommand>true</hasStandardCommand>
    <defaultProjectile>Bullet_...</defaultProjectile><warmupTime>1.5</warmupTime><range>62</range><ticksBetweenBurstShots>6</ticksBetweenBurstShots><burstShotCount>10</burstShotCount>
    <soundCast>...</soundCast><soundCastTail>GunTail_Medium</soundCastTail><muzzleFlashScale>9</muzzleFlashScale><recoilPattern>Mounted</recoilPattern></Properties>
  <AmmoUser><magazineSize>100</magazineSize><reloadTime>9</reloadTime><ammoSet>AmmoSet_...</ammoSet></AmmoUser>
  <FireModes><aiUseBurstMode>FALSE</aiUseBurstMode><aiAimMode>AimedShot</aiAimMode><noSingleShot>true</noSingleShot></FireModes>
</Operation>
```
Para granadas/explosivos: alcance e `minRange` do análogo CE (AGS-30: 62 / 8) e NÃO usar `aimedBurstShotCount` igual ou maior que o burst (gera aviso no CE e desliga o modo rajada; omitir o campo).
