# Status atual (atualize sempre que o usuário testar algo)

## Confirmado funcionando em jogo
M240, M134, M2, Mk19 (CE com burst 4), Mk44 (vanilla e CE), sistemas de calor/giro/dispersão.

## Implementado, NÃO confirmado
- **TOW (CE)**: antes mirava e não disparava; adicionado `FireModes aiAimMode AimedShot`. Testar se dispara. Alcance: vanilla 71,9 / CE 100.
- **Foguetes 80 mm (CE)**: trocado para `AmmoSet_80mmRocket_direct` (antes 70 mm APKWS demorava >1 min).
- **CIWS 20 mm**: burst 60 (vanilla ticks 2; CE mag 600).
- **M252 (CE)**: corrigido NRE com `fixedStorageSettings`; botão "atacar mundo" escondido via Harmony (`NoWorldStrikeExtension`). Verificar log e botão.

- **Bofors 40 mm duplo e quádruplo** (vanilla e CE): tripulados, 360°, sem energia. CE: 40x311mmR (análogo: Flak/Sniper turret do CE, alcance 86) + interceptação de projéteis (100) e drop pods (125) via `Building_CIWS_CE`. Testar: construção (quádruplo 3x3), tiro, calor, e no CE se abate granadas de morteiro, mísseis e drop pods (ver botões de "segurar fogo" de CIWS).
- **CIWS 20 mm no CE** virou CIWS real (`Building_CIWS_CE` + `VerbCIWSProjectile`). Testar se intercepta morteiro/mísseis e se ainda atira no chão.

- **Lote 4 (implementado, NÃO testado)**, vanilla e CE:
  - **ZU-23-2** (tripulada 2x2, 60°/s, sem energia): vanilla 36,9 · rajada 10 × 3; CE `AmmoSet_23x152mmB` (APHE), 75, mag 100, intercepta projéteis (90) e drop pods (110).
  - **Avenger** (auto 2x2, 150 W, 60°/s): vanilla = 2 mísseis Stinger explosivos contra o chão (49,9, mín 7,9; o vanilla não tem interceptação); CE = **só** abate drop pods (110), com munição própria `MA_Ammo_FIM92` (`1.6/CE/Defs`), verbo de chão removido como no patch do CE para o VFE anti-air, sem `PlaceWorker_ShowTurretRadius`.
  - **Goalkeeper** (auto 2x2, 900 W, 100°/s): vanilla 38,9 · rajada 40 × 1 (30 mm do Mk44); CE `AmmoSet_30x173mmNATO`, 78, mag 600, intercepta projéteis (100).
  - **Sistema laser** (auto 2x2, 2000 W, 100°/s, pesquisa Spacer com ChargedShot): sem munição e sem troca de cano no vanilla (só calor); CE: `MakeGunCECompatible` **sem AmmoUser** e projétil próprio `MA_Bullet_LaserPulse` (speed 400); intercepta projéteis (100). Risco: não verifiquei no código se o CE aceita a gun sem AmmoUser (o patch não exige o bloco, mas testar).

## Bug aberto
- **Bateria de foguetes guiados (CE)**: tiros iam para fora do mapa. M252 (mesmo verbo/cargas) acerta; log limpo. Causa (lida no código do CE): `ProjectileCE.Launch` usa `Max(velocidade da carga, def.projectile.speed)`; o APKWS tem speed 173, então ignorava a carga (ângulo calculado para ~50, voo a 173) e passava muito do alvo. Além disso tem `gravityFactor` 1 e as cargas assumem 5. Corrigido e **confirmado acertando** (out/2026): projétil próprio `MA_Bullet_APKWS_Indirect_HE` (speed 0 + gravityFactor 5, como a granada de 81 mm) + `MA_AmmoSet_APKWS_Indirect` (mesmo item `Ammo_70mmAPKWS_HEAT`) em `1.6/CE/Defs/MountedArms_CE_Ammo.xml`. Ajustes seguintes, NÃO testados: ogiva HE (Bomb 156, raio 3,5, fragmentos 6 grandes/10 pequenos; usuário achou o 81 mm HE com cara de estilhaço); `ShotSpread` 1,5 (0,25 não aparecia) e `circularError` 1 (`indirectFirePenalty` 0). Se o ShotSpread não ficar bom: verbo próprio que sobrescreve `LockRotationAndAngle` (DLL só-CE em `1.6/CE/Assemblies`) para cada foguete re-mirar com seu circularError; mesma ideia deve ser reproduzida no vanilla. Em salva o CE trava ângulo/direção após o 1º tiro: só o ShotSpread espalha a salva (≈16 células de alcance por grau em arco alto, ≈2,5 laterais a 150).

## Pendências
- Usuário cria o remote Git (`gh repo create mounted-arms --private --source=. --remote=origin --push`) e envia a URL.
- Atualizar `About/About.xml` (lista de torretas) — ver commit.

## Ambiente de teste
Jogo 1.6, Harmony, Combat Extended 16.7.4 (usuário testa só no CE por enquanto). Jogo em `F:\Steam\steamapps\common\RimWorld`.
