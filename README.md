# Expansao

Planner mensal para TDAH adulto, em papel A5 e app (PWA).

Metodo: **memoria externa + captura + organizacao + execucao + feedback**.

## Estrutura

```
expansao/
  app/app/          PWA (HTML + CSS + JS, offline, localStorage)
  landing/          Landing page publica (metodo, sem dados pessoais)
  print/            Gerador do PDF A5 (Python + Playwright)
  fonts/            Cormorant Garamond + Inter (CSS)
  dist/             Documentacao e artefatos gerados
  docs/             Schema de dados e decisoes tecnicas
```

## App (PWA)

Abre `app/app/index.html` no navegador. Instala como app pelo menu do navegador (Add to Home Screen).

- Dados salvos em `localStorage` (por aparelho)
- Exportar/Importar JSON pelo menu lateral
- Funciona offline via Service Worker

## Landing

Abre `landing/index.html`. Pagina publica que explica o metodo sem expor dados pessoais.

## Gerar PDF (papel A5)

Requer Python 3 + Playwright:

```bash
pip install playwright
playwright install chromium
cd print
python build_print.py
python pdf.py dist/october-2026-planner-A5.html dist/october-2026-planner-A5.pdf
```

## Identidade visual

| Token      | Valor     | Uso                          |
|------------|-----------|------------------------------|
| `--ink`    | `#1F2B3C` | texto, bordas (azul-tinta)   |
| `--ink2`   | `#6B7480` | legendas                     |
| `--accent` | `#D9A63A` | amarelo-girassol, detalhes   |
| `--review` | `#2E5C8A` | reviews, banners             |
| `--week`   | `#A3ACB6` | semanas/dias                 |
| `--rule`   | `#CDD2D8` | linhas de escrita            |

Tipografia: **Cormorant Garamond** em titulos; **Inter** em texto corrido.

## Ciclo mensal

1. RMM (Reuniao Mensal de Metas) no dia 27 do mes anterior
2. Uso diario: Top 3, Agora, checkpoints, Feito hoje, Registro
3. Domingo: planejamento da semana
4. Penultimo domingo: Route Review
5. Ultimo domingo: Monthly Review + Body Review
6. Dia 27: RMM do proximo mes

## Backlog

Ver `dist/BRIEF-expansao.md` para o backlog completo e instrucoes de continuidade.
