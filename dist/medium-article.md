# Recebi meu laudo de TDAH em julho. Em outubro, comecei a construir um pipeline de dados pessoal pra lidar com isso.

Em julho de 2026 recebi o laudo de TDAH adulto. Nao foi surpresa -- foi mais uma confirmacao para muita coisa que nunca fez sentido: os planners abandonados no terceiro dia, as listas feitas com empolgacao que nunca mais abri, a sensacao constante de saber exatamente o que precisa ser feito e nao conseguir comecar.

Fiz o que todo mundo faz. Testei apps. Routinery, Habitica, Todoist, Google Agenda, planners em papel, Notion. Funcionavam por uns dias. Depois viravam mais uma aba fechada.

Em outubro, parei de procurar o app certo e olhei para o problema com os olhos de quem trabalha com dados. Nenhuma dessas ferramentas me permitia responder perguntas basicas: em que horario eu realmente sou produtiva? Qual habito eu mantenho e qual eu abandono -- e por que? O que acontece nos dias em que eu travo? Treinar de manha muda meu dia ou nao?

Sao perguntas de analytics. E eu sou engenheira de dados. Entao comecei a construir o meu proprio sistema.

O projeto se chama Expansao. E eu sou o caso de estudo.

Em 2026, a stack para esse tipo de projeto existe e esta madura. O Model Context Protocol (MCP) permite que um assistente consulte dados estruturados via tools tipadas, sem receber um dump de texto como contexto. O pgvector permite busca semantica sobre texto livre sem sair do Postgres. LLMs classificam entradas de voz ou texto com prompts de 100 tokens. Nada disso era acessivel dessa forma dois anos atras. Hoje, uma pessoa sozinha monta um pipeline pessoal com a mesma arquitetura que times inteiros usam em producao.

Este artigo cobre a primeira camada: schema, contrato e as decisoes de engenharia de dados por tras do projeto. Nos proximos, vou publicar os dados reais.

---

## Arquitetura geral

O Expansao e um pipeline de dados pessoal com um app na ponta. Nao e um planner. E um sistema de ingestao, classificacao e consulta que usa uma PWA como interface.

O principio de design: o dado entra por onde o usuario ja esta. Se estou no WhatsApp e lembro de algo, mando mensagem para o bot. Se estou lavando louca, falo para a Alexa. Se abro o app, e uma lista de checkboxes -- nao um formulario. O pipeline classifica e armazena. O app exibe.

```
  App (PWA) · Voz (Web Speech API) · Alexa · WhatsApp · Google Agenda · Wellhub
                                      |
                                Classificacao
                               (regras + LLM)
                                      |
                             Supabase / Postgres
                                + pgvector
                                      |
                        ┌─────────────┼─────────────┐
                     Consultas     RAG/LLM       MCP Server
                     SQL           (texto)       (tools)
                        └─────────────┼─────────────┘
                                      |
                                App Expansao
```

Cada fonte converge para o mesmo schema no Supabase. O app le de uma unica fonte de verdade.

---

## Definicao do grao

No MVP, os dados estavam em localStorage como chaves flat:

```json
{
  "d5.r3": true,
  "d5.top0": "fechar relatorio X",
  "w2.prio.1": "entregar projeto Y"
}
```

Nao e possivel fazer JOIN, agregar ou versionar. A primeira decisao de engenharia foi definir o grao como `dia x tipo` e separar em tabelas:

- **daily_routine** -- um registro por dia por habito, com outcome modelado como enum e reason opcional
- **checkpoint** -- 6 registros por dia, com nota
- **capture** -- inbox de ideias vindas de qualquer fonte, com categoria classificada por LLM
- **daily_log** -- texto livre do dia, indexado com pgvector (1536 dims)
- **app_event** -- instrumentacao de uso

A separacao entre dados estruturados (rotinas, checkpoints -- colunas tipadas) e texto livre (logs, capturas -- indexados com embedding) e intencional. Consultas analiticas usam SQL puro sobre os estruturados. Perguntas semanticas usam RAG sobre os embeddings. Misturar as duas camadas compromete a relevancia do indice vetorial: vetorizar um boolean nao produz sinal util.

---

## Outcome em vez de done

A maioria dos apps de habito modela o resultado como boolean: fez ou nao fez. Para quem tem TDAH, "nao fiz" pode significar coisas diferentes, e a intervencao muda conforme o motivo:

| Outcome | Significado |
|---|---|
| `done` | Feito |
| `blocked` | Queria fazer, algo impediu |
| `skipped` | Pulei conscientemente |
| `partial` | Comecei, nao terminei |
| `dont_want` | Nao quero mais fazer isso |

Com `reason` opcional, isso se torna diagnostico. Depois de 30 dias de coleta, e possivel rodar:

```sql
SELECT habit_key, outcome, COUNT(*),
       array_agg(DISTINCT reason) AS reasons
FROM daily_routine
WHERE outcome != 'done'
GROUP BY habit_key, outcome
ORDER BY count DESC;
```

Se "estudo" aparece consistentemente como `blocked` com reason "trabalho ocupou o espaco", a intervencao muda de "tenha mais disciplina" para "mude o horario do estudo". E uma diferenca que so aparece com dados estruturados.

---

## RAG: quando SQL nao resolve

Para perguntas como "quantos treinos fiz esta semana?", SQL basta. Para "o que eu escrevia nos dias em que treinava vs. nos dias em que nao treinava?", e necessario cruzar dados estruturados com texto livre.

O pipeline de RAG: o texto do dia (log + notas) gera um embedding via text-embedding-3-small (1536 dimensoes), armazenado no pgvector. Na consulta, o embedding da pergunta e comparado por cosine similarity, os top-k logs relevantes sao recuperados e enviados como contexto para o LLM.

A decisao de nao vetorizar tudo e importante. Checkboxes e rotinas sao dados estruturados -- gerar embeddings de TRUE/FALSE nao produz relevancia. Somente texto livre vai para o indice vetorial. Isso reduz custo de embedding e melhora a qualidade da recuperacao.

---

## MCP: tools tipadas em vez de contexto bruto

O Supabase e exposto via MCP, permitindo que qualquer assistente consulte os dados com tools tipadas em vez de receber o historico inteiro como texto:

- `progresso_mensal(10, 2026)` retorna KPIs agregados
- `rotinas_da_semana("2026-10-07")` retorna habitos feitos e nao feitos
- `buscar_capturas("treino")` busca no inbox por texto

O ganho e mensuravel:

| Cenario | Tokens por pergunta | Custo estimado (Claude Sonnet) |
|---|---|---|
| Sem pipeline (contexto inteiro) | ~50.000 | ~$0.15 |
| Com MCP (SQL pre-filtrado) | ~1.200 | ~$0.004 |
| Com RAG (top-3 logs relevantes) | ~3.500 | ~$0.01 |

A reducao de 50k para 1.2k tokens e resultado direto de ter um schema com grao correto e separacao entre estruturado e texto livre. Nao e otimizacao de software; e engenharia de dados.

---

## O que observei ate aqui

Quatro coisas que o processo de construcao ja evidenciou, antes mesmo de ter 30 dias de dados:

**Data contract pessoal e data contract real.** A mesma disciplina de definir grao, tipagem e contrato de dados que aplico em pipelines corporativos se aplica a um projeto de um usuario. Se o schema esta errado, qualquer dashboard construido sobre ele tambem esta.

**Ingestao multi-source e o diferencial de pensar como DE.** Um dev construiria um app. Uma engenheira de dados constroi um hub que puxa de 6 fontes, classifica e unifica. O usuario nao precisa ter disciplina para alimentar o sistema -- o sistema se alimenta de onde o usuario ja esta.

**Separar estruturado de texto livre define se o RAG funciona.** Essa nao e uma otimizacao prematura. E a decisao que determina se a busca semantica retorna sinal ou ruido.

**Outcome importa mais que done.** Modelar como enum com reason opcional transforma o diagnostico de habito de achismo em evidencia consultavel.

---

## Stack

- **Frontend**: HTML/CSS/JS vanilla, PWA, Web Speech API
- **Backend**: Supabase (Postgres + pgvector + auth)
- **Classificacao**: Claude API com fallback para regex
- **MCP**: TypeScript MCP Server sobre Supabase
- **Ingestao**: Alexa Skill Kit, Twilio, Google Calendar API

---

## Isso e uma serie. E eu sou o experimento.

Este artigo cobre a arquitetura e as decisoes de engenharia. A partir de agora, todo mes vou publicar os resultados reais do uso. Sem filtro.

Vou abrir os numeros: quantos checks marquei, quantos dias abandonei, quais habitos sobreviveram e quais deixei morrer. O `outcome` vai mostrar se foi por bloqueio, por escolha ou por esquecimento. Se a gamificacao funcionou ou virou mais uma coisa que eu ignorei. Se o pipeline realmente muda comportamento ou se e apenas um dashboard que eu nao abro.

Nos proximos artigos, alem dos dados:

- **Classificacao por LLM em producao**: como o pipeline decide se "to exausta" e um log, uma captura ou um trigger de intervencao
- **Deteccao de padroes comportamentais**: SQL + embeddings para identificar quando vou travar -- e agir antes
- **MCP em producao**: como um assistente pessoal consulta dados estruturados gastando 97% menos tokens

Spoiler do artigo 2: daqui a 10 dias embarco para uma eurotrip. Fuso novo, hostel, sem rotina fixa, sem academia. O pipeline vai coletar dados de uma rotina completamente fora do padrao. Vamos ver o que sobrevive.

A pergunta que essa serie tenta responder: uma engenheira de dados consegue usar o que sabe de pipeline, schema e analytics para mudar a propria rotina?

Eu nao sei a resposta. Mas vou publicar ela aqui, com dados.

---

*Expansao · artigo 1 de uma serie · pipeline de dados pessoal para gestao de rotina e habitos.*
