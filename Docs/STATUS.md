# Status atual (atualize sempre que o usuário testar algo)

## Confirmado funcionando em jogo
M240, M134, M2, Mk19 (CE com burst 4), Mk44 (vanilla e CE), sistemas de calor/giro/dispersão.

## Implementado, NÃO confirmado
- **TOW (CE)**: antes mirava e não disparava; adicionado `FireModes aiAimMode AimedShot`. Testar se dispara. Alcance: vanilla 71,9 / CE 100.
- **Foguetes 80 mm (CE)**: trocado para `AmmoSet_80mmRocket_direct` (antes 70 mm APKWS demorava >1 min).
- **CIWS 20 mm**: burst 60 (vanilla ticks 2; CE mag 600).
- **M252 (CE)**: corrigido NRE com `fixedStorageSettings`; botão "atacar mundo" escondido via Harmony (`NoWorldStrikeExtension`). Verificar log e botão.

## Bug aberto
- **Bateria de foguetes guiados (CE)**: ao disparar, todos os tiros vão para fora do mapa / salva de 4 em vez de 6. Hipóteses (não verificadas): `NonSnapTurretExtension` (já removido), conflito entre `Building_TurretGunCE` e verbo de artilharia sem alvo válido, velocidade/carga do `Charges` (30/50/70/90) incompatível com a distância do alvo, `ShootingAccuracyTurret`/`circularError`. Próximo passo: pedir log + qual distância do alvo, comparar com a torreta de mísseis do Glitter Tech (mesma configuração) e com o morteiro CE vanilla.

## Pendências
- Usuário cria o remote Git (`gh repo create mounted-arms --private --source=. --remote=origin --push`) e envia a URL.
- Atualizar `About/About.xml` (lista de torretas) — ver commit.

## Ambiente de teste
Jogo 1.6, Harmony, Combat Extended 16.7.4 (usuário testa só no CE por enquanto). Jogo em `F:\Steam\steamapps\common\RimWorld`.
