# Histórico de bugs e correções

1. Mk19 mirava e não disparava (CE) → `FireModes` incorreto; resolvido com `aiUseBurstMode FALSE`, `aiAimMode AimedShot`, `noSingleShot`.
2. DLL antiga em jogo → conferir md5 após copiar; commitar com novo nome e `mv`.
3. `ShotsPerBurst` é protected → usa `shots=1` por tick.
4. Warning `aimedBurstShotCount` ≥ burst → removido.
5. Arco de tiro limitado não funcionou em M2/Mk19 → abandonado; todas 360°.
6. Calor nunca dispara no CE por causa do tamanho dos carregadores → mantido.
7. "Not enough squares ... 79.9" (TOW vanilla) → alcance 71,9; "radius ring 120" (TOW CE) → 100.
8. NRE `CompChangeableProjectile.GetParentStoreSettings` (M252 CE) → `fixedStorageSettings` na gun.
9. "Atacar mundo" no M252 → `CeGizmoFilter`.
10. Foguetes 70 mm APKWS direto em CE: voo >1 min → S-8 80 mm.
11. Bateria: vanilla "Not enough squares 254" → `ai_combatDangerous` false + `placeWorkers` Inherit=False. CE: tiros fora do mapa → APKWS com speed 173 (Launch usa Max(carga, speed)) e gravityFactor 1; projétil próprio com speed 0 + gravityFactor 5 (pendente de teste).
14. Interceptação não abatia a retaliação → opção do CE "Enable CIWS" estava desligada; ligada, o Phalanx abate.
15. (Strategic) Minuteman errava 30+ células no mapa-mundo → penalidades fixas de luz/fumaça e erro de distância do tiro global do CE; resolvido com `Verb_ShootGuidedCE`.
16. (Strategic) Minuteman convencional r24,9 derrubava o FPS no impacto → raio 19,5 (limite = Tomahawk do CE).
13. Erro meu (lote 4): `MA_Turret_ZU23`, `MA_Gun_ZU23`, `MA_Ammo_FIM92`, `MA_Bullet_FIM92` (e `MAS_*_M777` no Strategic) terminavam em dígito → config error no carregamento. Renomeados para `_ZU23_AA`, `_FIM92_Stinger`, `_M777_Howitzer`; criado `tools/check_defnames.py`.
12. Erro meu: replace-all trocou o burst do Mk19 (4→6) em vez da bateria; corrigido por sed por linha.
