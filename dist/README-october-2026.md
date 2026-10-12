# October 2026 — Expansion Sprint 01 · Personal Operating System

MVP. Usar durante outubro inteiro. **Não redesenhar.** Feedback → System Lab → November v2.

## Arquivos

| Arquivo | O que é |
|---|---|
| `october-2026-planner-A5.pdf` | 106 páginas A5, pronto para gráfica (1 página por folha A5, frente e verso). |
| `october-2026-planner-A4-2up.pdf` | Mesmo conteúdo, 2 páginas A5 por folha A4 paisagem (53 folhas) — para imprimir em casa, duplex, virar na borda curta, cortar ao meio e encadernar. |
| `october-2026-digital.html` | Versão digital editável (dashboard + todas as seções). Abre em qualquer navegador; salva sozinho no navegador (localStorage). Botão **Exportar** gera um JSON de backup; **Importar** restaura. |
| `october-2026-planner-A5.html` | Fonte do PDF (para gerar a v2 em novembro). |

## Decisões de formato

- **A5 vertical** (148 × 210 mm). Motivos: cabe em qualquer bolsa; a mão não cruza a lombada ao escrever (no horizontal a linha de escrita atravessa a dobra); calendário e listas por dia cabem melhor em coluna.
- **Encadernação recomendada: wire-o (espiral duplo) ou costura aberta** — abre 360°, fica plano na mesa, permite dobrar para trás na academia/café. Capa dura fina ou PP fosco. Evitar lombada colada (não abre plana).
- **Margens**: lombada 17 mm · externa 11 mm · topo 12 mm · rodapé 13 mm. Nada de escrita a menos de 17 mm da lombada.
- **Espaço de escrita**: linhas de 10–12 mm (letra grande), caixas de checkbox 4–6 mm, pontilhado 6 mm nas áreas livres. Regra aplicada: se a caixa não cabe uma letra grande, a caixa não existe.
- **Uma página = uma pergunta.** Nunca mais de 2 blocos densos por página.

## Navegação — "Onde eu escrevo isso?"

1. **Página MAPA** (p. 2): tabela situação → página.
2. **Códigos no rodapé**: `X` Chaos · `C` Capture · `O` Overview · `M1/M2` RMM/Prioridades · `K` KPIs · `B` Backlog · `G` Guindastes · `A` Accountability · `GU` Glow Up · `CT` Content · `W1–W5` semanas · `D01–D31` dias · `R1` Route Review · `R2` Monthly Review · `R3` Body Review · `DB` Debug · `L` System Lab · `N` November RMM.
3. **Bordas coloridas** na margem externa (thumb index, visível com o planner fechado):
   preto = início · terracota = mês · cinza = semanas & dias (**a marca desce 28 mm a cada semana** → dá para achar a semana pela borda) · verde = review & lab.
4. **Ordem cronológica**: cada semana começa com o spread semanal e é seguida pelos seus dias. Route Review está fisicamente depois do dia 18; Monthly/Body Review + Next Month depois do dia 25. O dia 18, 25 e 27 tem um banner "HOJE · …" na página.

## Estrutura (106 páginas)

| Bloco | Páginas | Conteúdo |
|---|---|---|
| Início | 1–5 | Capa · Mapa · Chaos Mode · Capture It (2) |
| Mês | 6–18 | Overview (calendário + campos) · Compromissos do mês (1 linha/dia, 2 pág.) · RMM · Prioridades · KPIs · Backlog (2) · Guindastes · Accountability · Glow Up (2) · Content Backlog |
| Semanas 1–5 | 19–95 | Spread semanal (2 pág.) + 2 páginas por dia. Dia esquerdo: TOP 3 · AGORA · 6 checkpoints · BODY · LIFE. Dia direito: CAPTURE IT + NOTAS (pontilhado). |
| Reviews inline | 61–62 (após D18) · 79–81 (após D25) | Route Review (2) · Monthly Review + Next Month (2) · Body Review |
| Lab | 96–101 | Debug my life (3) · System Lab (2) · November RMM |

Ciclo: **27/09 RMM (definiu outubro) → 18/10 Route Review → 25/10 Monthly Review → 27/10 RMM de novembro.**

## Visual Design System v0.2 — girassol clean

Amarelo-girassol e azul da identidade, usados com parcimônia: o amarelo só em detalhes (borda da capa, girassol em linha, bordas da seção Mês, números de prioridade); o azul-tinta faz o trabalho pesado do texto para não cansar no dia a dia. Fundo branco, muito ar.

| Token | Valor | Uso |
|---|---|---|
| `--ink` | `#1F2B3C` azul-tinta | texto, bordas, tabs de início |
| `--ink-2` | `#6B7480` | legendas, dicas |
| `--rule` | `#CDD2D8` | linhas de escrita (claras, não competem com a caneta) |
| `--accent` | `#D9A63A` amarelo-girassol | seção Mês, números de prioridade, domingos, capa |
| `--week` | `#A3ACB6` | bordas das semanas/dias |
| `--review` | `#2E5C8A` azul | Review & Lab, banners, códigos de página no mapa |
| Display | Cormorant Garamond 400–600 | títulos, números grandes |
| Texto | Inter 400–600, caixa alta com tracking .12–.16em | rótulos |

Tudo é variável CSS em `print.css` / `<style>` do digital — ajustar tons pelos prints do Instagram não mexe no layout.

## v0.3 — Guia de uso + Feito Hoje

- 4 páginas **GUIA** logo após o Mapa: ritual do dia (abrir · executar · fechar), rituais de semana/mês (domingo, R1, R2/R3, N), regras "o que vai onde" e um dia de exemplo preenchido.
- Página direita de cada dia reorganizada: **FEITO HOJE** (12 quadradinhos de rotina: leitura, treino, estudo, trabalho focado, casa, cachorros, conteúdo, água, sono, alimentação, administrativo + 1 livre), **REGISTRO DO DIA** (7 linhas de 10 mm para o log detalhado), Capture It e Notas menores.
- Digital: view "Guia de uso", bloco Feito hoje + Registro do dia em Hoje, KPI "rotinas feitas hoje" no Dashboard.
- Total: 106 páginas A5 / 53 folhas A4 2-up.

## Como imprimir

- **Gráfica**: enviar `A5.pdf`, "A5, frente e verso, sem escala (100%), sem marcas, encadernação wire-o preto, capa PP fosco". Pedir folha de papel 90–120 g (caneta não atravessa).
- **Casa**: `A4-2up.pdf`, A4 paisagem, duplex **virar na borda curta**, 100%, cortar ao meio.

## November-ready

- Para gerar novembro: em `build_print.py` mudar `MONTH=11`, `MONTH_NAME="NOVEMBER"`, `SPRINT="Expansion Sprint 02"`. Domingos de review, semanas e dias são calculados.
- Antes de gerar: ler o **System Lab** (páginas L / seção L do digital) e o **Monthly Review**. Mudanças entram no código só aí.
- No digital, a página **November RMM** já lista automaticamente tudo que foi registrado no System Lab.

## Regra final

USE O SISTEMA. NÃO OTIMIZE O SISTEMA. Vontade de mudar → System Lab → 25/10 → v2.
