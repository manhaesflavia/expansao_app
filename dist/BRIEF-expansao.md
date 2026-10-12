# Expansão — brief para recriar/continuar o projeto no Devin

> Cole este documento como primeira mensagem de uma sessão nova e anexe `expansao-source.zip`.
> O zip tem todo o código; este arquivo explica o que é, por que é assim e o que falta.

---

## 1. O que é

**Expansão** é um planner mensal (um mês por vez) para TDAH adulto, em dois formatos que seguem o mesmo método:

- **Papel A5** — PDF de 106 páginas, 2 páginas por dia, wire-o, letra grande.
- **App (PWA)** — HTML único, instalável no celular, offline, dados em `localStorage`.
- **Landing pública** — explica o método sem expor nenhum dado pessoal.

Método em uma linha: **memória externa + captura + organização + execução + feedback**.
Experiência desejada: *"Abri. Sei onde estou. Sei onde escrever. Sei o que fazer."*

Mês atual: **Outubro 2026 — Expansion Sprint 01**. Novembro = Sprint 02.
Ciclo: 27/09 RMM → 18/10 Route Review → 25/10 Monthly Review → 27/10 RMM de novembro.

Regra do mês: **usar o sistema, não otimizar o sistema**. Vontade de mudar → System Lab → v2 em novembro.

---

## 2. Estrutura do código (zip)

```
planner/
├─ build_print.py        # gera o HTML A5 (todas as 106 páginas) a partir de listas/loops
├─ print.css             # design system de impressão (tokens, grid A5, margens, thumb index)
├─ pdf.py                # Playwright → PDF A5 + A4 2-up
├─ sunflower.svg         # girassol em linha (capa, ícone, landing)
├─ fonts/                # Cormorant Garamond + Inter
├─ stories.py            # gera stories 1080x1920 + og.png (Playwright)
├─ app/
│  ├─ index.html         # LANDING pública (estática, sem dados)
│  ├─ og.png, pg-*.png, shot-*.png   # imagens da landing (prints em branco)
│  └─ app/
│     ├─ index.html      # O APP (PWA) — tudo em um arquivo: CSS + JS + views
│     ├─ manifest.json   # start_url ./index.html#dash, scope ./
│     ├─ sw.js           # cache "expansao-v3", network-first, fallback offline
│     └─ icon-192/512/512-maskable.png  # ícone amarelo (fundo #F3D77B, girassol azul)
└─ dist/
   ├─ october-2026-planner-A5.pdf / -A4-2up.pdf
   ├─ README-october-2026.md     # decisões de formato, impressão, navegação
   ├─ lacunas-perfil.md          # análise de lacunas + backlog (INTERNO, não publicar)
   └─ artigo-medium.md           # rascunho de artigo (engenharia de dados)
```

Deploy: `app/` inteiro como site estático (landing na raiz, app em `/app/`).
URL atual: https://app-yprqllyd.devinapps.com (landing) · https://app-yprqllyd.devinapps.com/app/ (app).

Gerar PDF: `python3 build_print.py && python3 pdf.py`. Novembro: em `build_print.py` mudar `MONTH=11`, `MONTH_NAME="NOVEMBER"`, `SPRINT="Expansion Sprint 02"`.

---

## 3. Identidade visual

| Token | Valor | Uso |
|---|---|---|
| `--ink` | `#1F2B3C` | texto, bordas (azul-tinta) |
| `--ink2` | `#6B7480` | legendas |
| `--accent` | `#D9A63A` | amarelo-girassol, só detalhes |
| fundo claro | `#F3D77B` | ícone, hero da landing |
| `--review` | `#2E5C8A` | reviews, banners |
| `--week` | `#A3ACB6` | semanas/dias |
| `--rule` | `#CDD2D8` | linhas de escrita |

Tipografia: **Cormorant Garamond** só em títulos e números grandes; **Inter** em todo texto corrido, rótulos (caixa alta, tracking .12–.16em) e em tudo que é pequeno no app — a serifa fina lia mal em tela.
Estética: branco, muito ar, maduro, nada infantil, nenhuma ilustração pesada; girassol só em linha fina.

---

## 4. Páginas / views

**Papel (106 p.)**: Capa · Mapa ("onde escrevo isso?") · Guia de uso (4 p.) · Chaos Mode · Capture It · Overview do mês · Compromissos · RMM · Prioridades · KPIs · Backlog · Guindastes · Accountability · Glow Up · Content Backlog · 5 semanas (spread semanal + 2 p./dia) · Route Review (após D18) · Monthly Review + Body Review (após D25) · Debug my life · System Lab · November RMM.

**Dia, página esquerda**: TOP 3 · AGORA (próxima microação) · 6 checkpoints (Manhã, 2 Pomodoros, Almoço, Tarde, Fim do trabalho, Noite) · BODY · LIFE.
**Dia, página direita**: FEITO HOJE (leitura, treino, estudo, trabalho focado, casa, cachorros, conteúdo, água, sono, alimentação, administrativo, livre) · REGISTRO DO DIA (7 linhas) · Capture It · Notas.

**App**: as mesmas views (dash, today, week, guide, chaos, capture, overview, rmm, kpis, backlog, guindastes, accountability, glowup, content, debug, lab, route, monthly, body, nov) via `location.hash`; menu lateral no mobile; Exportar/Importar JSON.

Códigos de página: X Chaos · C Capture · O Overview · M1/M2 RMM · K KPIs · B Backlog · G Guindastes · A Accountability · GU Glow Up · CT Content · W1–W5 · D01–D31 · R1/R2/R3 reviews · DB Debug · L Lab · N November.

---

## 5. Decisões já tomadas (não reabrir sem motivo)

- A5 vertical, wire-o, margem de lombada 17 mm; linhas de 10–12 mm; "se não cabe letra grande, a caixa não existe".
- Uma página = uma pergunta; no máximo 2 blocos densos.
- Landing **abstrata**: fala do método e do TDAH adulto em geral; não é sobre a autora. Rodapé: "Feito por uma engenheira de dados com TDAH, para uso próprio · Sobre a autora (em breve)". Nenhum dado real, nenhum detalhe de laudo.
- Texto público direto, sem frase de efeito, sem "não é X, é Y", sem tom de IA.
- Stories do Instagram: a autora faz com foto da tela ("em desenvolvimento"); não gerar artes prontas.
- Ícone: variante amarela (fundo `#F3D77B`, girassol azul em linha).
- O app é PWA, não está na Play Store. Widget nativo só com app nativo (TWA/Capacitor) — futuro.
- Dados: hoje `localStorage` por aparelho. **Exportar manualmente é fricção; o alvo é sync automático**.

---

## 6. Perfil (uso interno — resumo sem dados clínicos)

Pontos que o sistema precisa cobrir, por ordem: rende com estímulo externo/urgência/prazo; dificuldade de iniciar, manter, parar (hiperfoco) e lembrar do futuro (memória prospectiva); prejuízo em **dinheiro** e **casa**; vulnerabilidade a culpa/autocrítica; autocuidado some quando o trabalho engole.

Pergunta que o app ainda não faz (vinda do psicólogo): **"travei ou não quero?"** — nem toda tarefa não feita é falha de mecânica; às vezes falta propósito. Ver `lacunas-perfil.md`.

---

## 7. Backlog (prioridade)

**App, pequenos (podem entrar ainda em outubro)**
1. Bloco "Agora" fixo no topo + lembretes nos checkpoints (notificações) — substituto do widget.
2. Botão Chaos Mode fixo.

**Sprint 02 (novembro), com backend**
3. Sync automático: `localStorage` → Supabase (Postgres + pgvector + auth, plano free). Exportar vira só backup.
4. Hora de parar (time-boxing) + estimado × real por tarefa.
5. Dinheiro: página mensal + lista de espera de 48h para compras.
6. Gatilhos "quando X → Y" (memória prospectiva).
7. Mínimos antes do trabalho (água, comida, remédio) visíveis no topo do dia.
8. "Travei ou não quero?" no checkpoint; prioridade da RMM com "por que importa agora"; Monthly Review com duas colunas (sistema falhou × eu não quis).
9. Três vitórias do dia + regra "metade conta".
10. **Versão flexível**: rotinas, checkpoints e KPIs configuráveis pelo usuário (tela "Configurar meu mês"; defaults = conjunto atual; config vive no mesmo JSON; PDF gerado a partir da config).

**Papel**: rotação de zonas da casa, acompanhamento clínico, progresso visível de projetos longos.

**Dados / estudo (o projeto de carreira)**
- Schema: grão = dia × tipo (`day_routine`, `checkpoint`, `capture`, `daily_log`, `review`); estruturado em tabelas, texto livre em índice vetorial com data/semana/tipo como metadado.
- RAG sobre registros; MCP expondo tools (`rotinas_da_semana`, `registro_do_dia`).
- Métrica: **tokens por pergunta respondida**, com e sem filtro estruturado.
- Artigo Medium em rascunho (`artigo-medium.md`); feedback pendente: "pouco voltado para dados" → reescrever com DDL, modelo de eventos vs. snapshot, chunking com metadados e números de tokens.

---

## 8. Como pedir para o Devin continuar

Exemplos de primeira mensagem:
- *"Anexo o zip e o brief. Implemente o item 1 do backlog (bloco Agora fixo + notificações nos checkpoints) no `app/app/index.html`, sem mudar o visual, e publique."*
- *"Monte o backend Supabase do item 3 com o schema do item 7 e troque o localStorage por sync automático."*
- *"Gere o planner de novembro (Sprint 02) aplicando os itens 4, 5 e 7 nas páginas de papel."*
