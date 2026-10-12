# Construi um pipeline de dados pessoal para gerenciar rotina e habitos

Testei agendas, apps de habito, planners. Nenhum funcionou. O padrao era sempre o mesmo: usava por 3 dias, abandonava, tentava outro.

Quando parei pra analisar por que nenhum sistema funcionava, percebi que o problema nao era de produtividade. Era de **dados**. Nenhum desses apps me permitia responder perguntas basicas:

- Em que horario eu realmente sou produtiva?
- Qual habito eu mantenho e qual eu abandono?
- O que acontece nos dias em que eu travo?
- Treinar de manha muda meu dia ou nao?

Sao perguntas de analytics. E eu sou engenheira de dados. Entao construi o meu proprio sistema.

---

## O que e o Expansao

Um pipeline de dados pessoal com um app na ponta. Nao e um planner. E um sistema de ingestao, classificacao e consulta que usa um app como interface.

O principio de design: **o dado entra por onde o usuario ja esta**. Se estou no WhatsApp e lembro de algo, mando mensagem pro bot. Se estou lavando louca, falo pra Alexa. Se abro o app, e uma lista de checkboxes -- nao um formulario. O pipeline classifica e armazena. O app so exibe.

```
  App · Voz · Alexa · WhatsApp · Google Agenda · Wellhub
                          |
                    Classificacao
                    (regras + LLM)
                          |
                  Supabase / Postgres
                     + pgvector
                          |
              ┌───────────┼───────────┐
           Consultas    RAG/LLM    MCP Server
           SQL          (texto)    (tools)
              └───────────┼───────────┘
                          |
                    App Expansao
```

---

## A primeira decisao: definir o grao

No MVP, os dados estavam em localStorage como chaves flat:

```json
{
  "d5.r3": true,
  "d5.top0": "fechar relatorio X",
  "w2.prio.1": "entregar projeto Y"
}
```

Nao da pra fazer JOIN, nao da pra agregar, nao da pra versionar. A primeira decisao de engenharia foi definir o grao como `dia x tipo` e separar em tabelas:

- **daily_routine** -- um registro por dia por habito, com outcome modelado como enum (`done`, `blocked`, `skipped`, `partial`, `dont_want`) e reason opcional
- **checkpoint** -- 6 por dia, com nota
- **capture** -- inbox de ideias vindas de qualquer fonte, com categoria classificada por LLM
- **daily_log** -- texto livre do dia, indexado com pgvector
- **app_event** -- instrumentacao de uso

A separacao entre **dados estruturados** (rotinas, checkpoints) e **texto livre** (logs, capturas) e a decisao mais importante do projeto. Consultas analiticas usam SQL puro nos estruturados. Perguntas semanticas usam RAG sobre os embeddings. Misturar os dois e garantia de lixo semantico no indice vetorial.

---

## Outcome > done

A maioria dos apps de habito modela o resultado como boolean: fez ou nao fez. Mas "nao fiz" pode significar 5 coisas diferentes:

| Outcome | O que significa |
|---|---|
| `done` | Fiz |
| `blocked` | Queria fazer, algo impediu |
| `skipped` | Pulei conscientemente |
| `partial` | Comecei, nao terminei |
| `dont_want` | Nao quero mais fazer isso |

Com `reason` opcional, isso vira diagnostico. Depois de 30 dias, posso rodar:

```sql
SELECT habit_key, outcome, COUNT(*), 
       array_agg(DISTINCT reason) AS reasons
FROM daily_routine
WHERE outcome != 'done'
GROUP BY habit_key, outcome
ORDER BY count DESC;
```

E descobrir que "estudo" quase sempre e `blocked` por "trabalho ocupou o espaco" -- o que muda a intervencao de "tenha mais disciplina" para "mude o horario do estudo".

---

## RAG: quando SQL nao basta

Para "quantos treinos fiz esta semana?", SQL resolve. Mas para "o que eu escrevia nos dias que treinava vs. nos dias que nao treinava?", preciso cruzar dados estruturados com texto livre.

O pipeline: texto do dia gera embedding (text-embedding-3-small, 1536 dims), armazenado no pgvector. Consulta: embedding da pergunta, cosine similarity, top-k logs, contexto pro LLM.

A decisao de **nao vetorizar tudo** e importante. Checkbox nao precisa de embedding. So texto livre vai pro indice vetorial. Menos ruido, mais relevancia, menos custo.

---

## MCP: o assistente que consulta seus dados

O Supabase e exposto via MCP (Model Context Protocol), permitindo que qualquer assistente consulte os dados com tools tipadas:

- `progresso_mensal(10, 2026)` retorna KPIs agregados
- `rotinas_da_semana("2026-10-07")` retorna o que fez e o que nao fez
- `buscar_capturas("treino")` busca no inbox

O ganho e mensuravel:

| Cenario | Tokens/pergunta | Custo |
|---|---|---|
| Sem pipeline (contexto inteiro) | ~50.000 | ~$0.15 |
| Com MCP (SQL pre-filtrado) | ~1.200 | ~$0.004 |
| Com RAG (top-3 logs) | ~3.500 | ~$0.01 |

Reducao de 50k para 1.2k tokens. Isso nao e otimizacao de software. E o resultado de ter um schema com grao correto. Engenharia de dados.

---

## O que aprendi

**1. Data contract pessoal e data contract real.** A mesma disciplina de definir grao, tipagem e contrato que uso em pipelines corporativos se aplica a um projeto de 1 usuario. Se o schema esta errado, o dashboard esta errado.

**2. A ingestao multi-source e o diferencial.** Um dev faria um app. Uma engenheira de dados faz um hub que puxa de 6 fontes, classifica e unifica. O usuario nao precisa de disciplina para alimentar o sistema.

**3. Separar estruturado de texto livre define se o RAG funciona.** Vetorizar checkbox e ruido. Vetorizar diario e sinal.

**4. O outcome importa mais que o done.** Enum com reason transforma diagnostico de habito de achismo para evidencia.

---

## Stack

- **Frontend**: HTML/CSS/JS vanilla, PWA, Web Speech API
- **Backend**: Supabase (Postgres + pgvector + auth)
- **Classificacao**: Claude API com fallback para regex
- **MCP**: TypeScript MCP Server sobre Supabase
- **Ingestao**: Alexa Skill Kit, Twilio, Google Calendar API

---

## Isso e uma serie

Esse artigo e o primeiro. Ele cobre a arquitetura, o schema e as decisoes de engenharia. Os proximos vao cobrir o que nenhum artigo tecnico costuma mostrar: **os dados reais**.

Eu sou o caso de estudo do meu proprio pipeline. Vou usar o Expansao no dia a dia, coletar dados sobre minha rotina, e publicar o que o sistema me ensinou. Sem filtro.

O que esperar nos proximos artigos:

- **Os dados da primeira semana**: quantos checks marquei, onde abandonei, o que o outcome 'blocked' me mostrou sobre minha rotina
- **Classificacao por LLM em producao**: como o pipeline decide se "to exausta" e um log, uma captura ou um trigger de intervencao
- **O que funciona e o que nao funciona**: gamificacao resolveu? streak motivou ou virou pressao? a barra de tempo do dia mudou meu comportamento?
- **Deteccao de padroes**: quando os dados sao suficientes pra SQL + embeddings identificarem que eu vou travar -- e agirem antes
- **MCP em producao**: como um assistente pessoal consulta seus proprios dados gastando 97% menos tokens

A pergunta que essa serie tenta responder: **uma engenheira de dados consegue usar o que sabe de pipeline, schema e analytics pra resolver um problema pessoal real?**

Acompanha pra ver o resultado.

---

*Expansao e um projeto pessoal. Pipeline de dados para gestao de rotina e habitos. Esse e o artigo 1 de uma serie. Em desenvolvimento.*
