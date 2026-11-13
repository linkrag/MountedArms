# Decisões do projeto (e por quê)

## Do usuário (Felipe) — não reverter sem perguntar
- **Fonte fora de `Mods`** (7/nov/2026, escolha do usuário entre as opções): o fonte e os docs ficam em `RimWorld/_dev/src/<mod>`; `Mods/<mod>` é cópia gerada pelo deploy (só About, LoadFolders.xml, 1.6, Bin), e o upload continua pelo botão do jogo. Alternativa recusada: manter tudo e publicar pelo SteamCMD a partir de uma cópia limpa (exige login no SteamCMD e proíbe o botão do jogo).
- **RimWorld 1.6 e 1.7** (25/out/2026): manter as duas versões. O SDK .NET 10 foi instalado na máquina para compilar ("pode instalar o sdk").
- **Texturas** são geradas por mim (script `tools/gen_tex.py`); ele não edita sprites.
- **Balanceamento vanilla-friendly**; alcance vanilla calibrado contra mini-turret (28,9), fuzil (25,9), sniper (41,5), lança-granadas (~38,9).
- **Alcance no CE = o do próprio CE** ("ele está há muito tempo no jogo, vamos dar ele como balanceado"). Foi pedido comparar com armas reais; ficou decidido usar as turretas/armas do CE e do vanilla como régua, não proporção real.
- **Realismo** foi implementado antes de criar mais torretas (calor do cano, giro, dispersão) para que novas torretas só precisem preencher o template.
- **Calor no CE**: com os carregadores do CE as torretas quase nunca esquentam. Decisão dele: **deixar como está**, "posso balancear no futuro". Os números de T (segundos até superaquecer) foram escolhas minhas de design (M134 40 s, M240 60 s, M2 90 s, Mk19 120 s, Mk44 75 s), sem base em dado real.
- **Arco de tiro**: as quatro primeiras montadas (M240, M134, M2, Mk19) têm **360°** ("algumas dessas armas montadas e tripuladas possuem arco de 360; se todas possuírem, mantemos"). O sistema de arco limitado existe (vanilla `arcDegrees`, CE `CompFireArc`) para torretas futuras, mas está sem uso. Não funcionou bem em M2/Mk19 na época do teste.
- **Morteiro M252**: "se não for um morteiro com facilidade de mobilidade, onde podemos levar para outros mapas, ou montar de forma fácil, como realmente é um morteiro de 81 mm, não faz sentido termos isso". Por isso é minifiável, leve, barato e de montagem rápida.
- **Botão "atacar um lugar no mundo"** (do CE, em artilharia) não faz sentido para o M252 e para a bateria → escondido.
- **Bateria de foguetes guiados**: queria fogo **indireto em arco, como morteiro**, com o **mesmo alcance do morteiro do jogo** (vanilla 500 / CE 700), compensando com mais precisão e mais cooldown. Configuração base: a torreta de mísseis do mod Glitter Tech (já nos patches do CE).
- **Foguetes diretos** continuam existindo como torreta separada (80 mm S-8).
- TOW: alcance deve ser longo ("achei pequeno").
- CIWS: rajada maior (60). Depois (out/2026): no CE vira CIWS real, interceptando projéteis.
- Lote 4 pedido pelo usuário ("pode fazer todos"): ZU-23-2, Avenger/Stinger (contra drop pods), Goalkeeper, CIWS laser. Interceptação é só do CE; no vanilla essas torretas atiram no chão.
- **Lançamento mais realista** (pesquisa: Stinger soft launch ~8,5 m; TOW motor de voo ~7 m; foguetes em pod com lançamento quente): só efeitos visuais, porque a interceptação do CE assume voo linear.
- **Giro e energia realistas**: CIWS gira rápido (100 °/s) e consome mais (700 W); Bofors é manual, mais lento (25/20 °/s) e sem energia.
- **Bofors 40 mm L/60**: o usuário descreveu o antiaéreo naval de 40 mm com 2 ou 4 canos e atirador sentado entre eles; pediu **as duas versões** (duplo Mk 1 e quádruplo Mk 2). No CE intercepta **projéteis e drop pods** além do tiro no chão.
- Torretas pedidas depois do Mk44: TOW, foguetes 70 mm, CIWS 20 mm, morteiro 81 mm ("pode fazer os outros 4").

## Técnicas (minhas)
- **1.6 + 1.7 (25/out/2026):** conteúdo comum em `1.6/` e DLLs por versão em `Bin/<versão>`, o mesmo esquema do Strategic.
  - Não movi o conteúdo para `Common/`: assim nenhum caminho muda em defs, texturas, ferramentas e docs.
  - As referências vêm do `Krafs.Rimworld.Ref`, porque compilar a 1.6 sem o jogo 1.6 instalado exige referências de fora.
  - A 1.7 compila contra o CE 1.6 com fachadas, enquanto não houver CE 1.7.
- Uma camada CE separada, carregada por `LoadFolders IfModActive`, em vez de patches condicionais.
- Harmony só para: origem do projétil/clarão (`Projectile.Launch` prefix), giro (`TurretTop.TurretTopTick`), arco (`Building_TurretGun.IsValidTarget`/`OrderAttack`), filtro de gizmo do CE (`Building_TurretGunCE.GetGizmos`).
- `CompBarrelHeat` usa só API pública + reflexão em `burstCooldownTicksLeft`/`burstWarmupTicksLeft`/`ResetCurrentTarget` para funcionar nos dois mundos.
- Patch XML: `PatchOperationMakeGunCECompatible` para armas; ops manuais para o building. Detalhes em `Docs/CE_NOTES.md`.
- Sem `aimedBurstShotCount` (warning do CE), sem `noSnapshot` nas armas de burst > 1 não-artilharia (Mk19 quebrava). Artilharia CE (Glitter Tech) usa `noSnapshot` + `noSingleShot`.
- Mods do usuário que podem conflitar e já foram checados quando ele perguntou: a lista não foi registrada nos docs (o `Docs/STATUS.md` só guarda a linha "Ambiente").

## Gatling (out/2026)
- Modelo: Colt M1883 (10 canos, .45-70 Government, tambor Accles 104, ~600 rpm sustentado na manivela; arma ~90 kg). Fontes: Wikipedia "Gatling gun", American Rifleman "Model 1883 and No. 353 Gatling Guns".
- Equilíbrio: é a torreta de entrada. Exige só `Gunsmithing` (antes de `GunTurrets`), sem energia, aço + madeira + 2 componentes; em troca é mais fraca que a M240 (dano, AP, precisão, alcance). Abre o caminho do M134 (pré-requisito de `MA_Research_Rotary`).
- Sem rajadas (pedido do usuário, realismo): a Gatling atira enquanto gira a manivela. Modelado como tiro único com cooldown curto (vanilla e CE), precisão ruim e fumaça de pólvora negra por tiro; o limite é o calor (vanilla) e o tambor + calor (CE). No CE o modo de mira é `SuppressFire` (fogo de varredura), não `AimedShot`.
- CE: usa a munição .45-70 do próprio CE; alcance 55 = análogo rifle por ferrolho do CE (decisão "alcance CE usa o alcance do próprio CE").

## Aba "Militar" do Architect (2/nov/2026)
- Pedido do usuário: as torretas saem do Security e ganham a própria aba, compartilhada com o Mounted Arms Strategic. A categoria `MA_Military` (order 310, logo após Security) vive neste mod; o Strategic a usa por patch condicional (ver `../MountedArmsStrategic/Docs/DECISIONS.md`). Sem ícone, como as categorias do vanilla.

## Versionamento (13/nov/2026)
- Pedido do usuário: changelog e versão nas descrições da Oficina.
- SemVer. 1.0.0 = 1ª publicação na Oficina (7/nov/2026). MINOR = recurso novo, PATCH = só correção ou ajuste. Uma versão por dia com mudança visível (não sabemos quais dias foram enviados à Oficina; a próxima subida leva tudo).
- Fonte da verdade: `Docs/CHANGELOG.md` (inglês, texto de jogador, sem nomes internos nem "não testado"). Antes de cada "Atualizar na Oficina": subir `<modVersion>` no `About.xml`, o `CHANGELOG.md` e a seção Changelog da `WORKSHOP_DESCRIPTION.txt` juntos, à mão. A descrição precisa ficar abaixo de 8000 caracteres.
