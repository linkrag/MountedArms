# Histórico de bugs e correções

## Lições do Strategic, lote 11 (26/out/2026)
- **Salva do CE travada no 1º tiro:** o `LockRotationAndAngle` reaproveita a mira do 1º tiro em toda a rajada contra célula ou prédio. Aumentar o `circularError` só desloca a salva inteira; o espalhamento por míssil tem de ser feito no verbo (`Verb_ShootGuidedCE.ShiftTarget`).
- **Bomb ×4:** o Bomb multiplica o dano por 4 em prédios e plantas. Para tirar HP exato, use um DamageDef próprio com fatores 1 (`MAS_BlastWave`).
- **`TakeDamage` × `Destroy`:**
  - O `TakeDamage` letal chama o `Kill`; o `Destroy(KillFinalize)` não.
  - Boomshroom (Odyssey) e coisas com `explodeOnKilled` explodem no `Kill`.
  - `CompExplosive.destroyedThroughDetonation = true` faz a coisa virar destroço sem explodir.
- **Parede de montanha imortal:**
  - Nunca segure um sustentador de teto em 1 de HP: depois disso o dano vira 0 e ele nunca mais cai.
  - O desabamento vanilla roda no `MapPreTick` do tick seguinte. Derrubar todos os sustentadores no fim da onda dá um desabamento só.
- **Fallout do Rimatomics:** o `NuclearStrike` só cria o `NuclearFallout` com `Yield > 150` (o mesmo limite liga a explosão completa em long events). O fallout dele tem taxa constante, e o toxic buildup multiplica pela `ToxicEnvironmentResistance`, então é 0 para quase todos; quem mata é a radiação (`DubUtils.applyRads`). Antes de culpar a versão do jogo, leia o IL das duas versões. Depois do `FatalRad`, o `applyRads` joga toda dose nele: radiação contínua mata em horas.
- **Shell quebrado em sessão longa:**
  - Se Bash, PowerShell e Write falham com ENOENT em `%TEMP%\claude\<sessão>\tasks`, a pasta temporária da sessão foi apagada.
  - Só Read, Grep e Edit continuam funcionando, e os subagentes também falham.
  - Não insista: atualize os docs e abra uma sessão nova para compilar e commitar.

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
17. Efeitos de lançamento: a DLL principal usa C# 6 e a máquina só tem C# 5 → nova `MountedArmsFx.dll` separada em vez de recompilar a principal.
18. (Strategic) Minuteman travou o jogo: desabamento de teto em cascata e rocha natural destruída → teto arrancado antes, HP direto, rocha intocada.
19. Chama dos foguetes no meio do sprite: `CompProjectileFleck` do CE usa o deslocamento do tick × originOffset → `CompProperties_Exhaust` no bocal.
20. (Strategic) Explosões grandes passaram a usar zonas reais de sobrepressão (Kingery-Bulmash), em todos os mísseis de grande impacto.
21. (Strategic) Explosão por zonas feita num tick só: ~1 s de travamento e sem efeito visual → onda de choque espalhada em ticks, com efeito vanilla por célula.
22. O jogo local passou para o 1.7 (sem `RimWorldWin64_Data` e sem Unity), e os scripts csc/mcs deixaram de funcionar. Foram trocados pelo SDK .NET 10 com alvo duplo (`net472` e `net10.0`, referências `Krafs.Rimworld.Ref`) e DLLs em `Bin/<versão>`. A 1.7 compila contra o CE 1.6 com fachadas.
    - Bug no meio do caminho: `-p:ModBin` passado na linha de comando não podia ser reatribuído no props, e a saída foi para `ma-bin1.6`. Corrigido com a propriedade derivada `ModBinDir`.
    - A revisão independente (26/out) achou mais quatro problemas:
      - o SDK gravava o commit do git na DLL (o MD5 mudava a cada commit);
      - os dois alvos dividiam o mesmo `obj` (um build sem `-f` pôs uma DLL net10 em `Bin/1.6`, 1 vez em 19);
      - `.gitignore` com `bin/`, que no Windows ignorava `Bin/` inteira;
      - `-Out` relativo era resolvido em cada pasta de projeto.
      Os quatro foram corrigidos.
13. Erro meu (lote 4): `MA_Turret_ZU23`, `MA_Gun_ZU23`, `MA_Ammo_FIM92`, `MA_Bullet_FIM92` (e `MAS_*_M777` no Strategic) terminavam em dígito → config error no carregamento. Renomeados para `_ZU23_AA`, `_FIM92_Stinger`, `_M777_Howitzer`; criado `tools/check_defnames.py`.
12. Erro meu: replace-all trocou o burst do Mk19 (4→6) em vez da bateria; corrigido por sed por linha.
