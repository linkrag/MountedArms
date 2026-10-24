# Status atual (atualize sempre que o usuário testar algo)

Ambiente: RimWorld 1.6, Harmony, Combat Extended 16.7.4 (o usuário testa só no CE por enquanto). Jogo em `F:\Steam\steamapps\common\RimWorld`. DLLs: `Source/build.sh` (principal) e `SourceCE/build_ce.ps1` (só-CE), com o jogo fechado.

## Confirmado funcionando em jogo
- M240, M134, M2, Mk 19 (CE com burst 4), Mk44 (vanilla e CE), sistemas de calor/giro/dispersão.
- **APKWS rocket battery (CE)**: acerta o alvo (projétil próprio `MA_Bullet_APKWS_Indirect_HE`: speed 0 + gravityFactor 5), ogiva HE (Bomb 156, raio 3,5) e dispersão da salva (`ShotSpread` 1,5, `circularError` 1) aprovadas.
- **Mk 15 Phalanx CIWS (CE)**: intercepta granadas de morteiro da retaliação — depende da opção do CE **"Enable CIWS"** (estava desligada no teste anterior, por isso nada era abatido).
- **Lote 5**: botão Descarregar (DLL só-CE `1.6/CE/Assemblies/MountedArmsCE.dll`, Harmony postfix em `Building_TurretGunCE.GetGizmos` para defs `MA_*`), nomes reais nos `label`, CIWS 20 mm mais preciso (CE ShotSpread 0,03, SwayFactor 0,6, recuo 0,6; vanilla heatSpread 1, burstSpread 0,012).

## Ajustes desta rodada (NÃO testados)
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

## Notas de interceptação (CE)
- Precisa da opção "Enable CIWS". Tripuladas (Bofors, ZU-23) só interceptam com alguém operando. Os botões de "segurar fogo" de CIWS desligam a interceptação.
- O verbo CIWS só dispara se a posição prevista do projétil entra no alcance no próximo segundo e o tiro chega a tempo; giro lento atrasa. Diagnóstico: modo de depuração do CE + "Draw intercept checks".

## Pendências
- Usuário cria o remote Git e envia a URL.
