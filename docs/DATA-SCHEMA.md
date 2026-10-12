# Expansao - Schema de Dados

## Estado atual (localStorage)

O app salva um unico objeto JSON com chaves flat. Este documento mapeia as chaves para um schema semantico, preparando a migracao para Supabase.

## Namespace das chaves

| Padrao de chave | Tipo | Descricao |
|---|---|---|
| `d{N}.top{0-2}` | string | Top 3 do dia N (texto da tarefa) |
| `d{N}.topdone{0-2}` | boolean | Top 3 do dia N concluido |
| `d{N}.now` | string | Microacao atual (bloco Agora) |
| `d{N}.cp{0-5}` | boolean | Checkpoint feito (0=Manha..5=Noite) |
| `d{N}.cpn{0-5}` | string | Nota do checkpoint |
| `d{N}.r{0-11}` | boolean | Feito hoje - rotinas (ver ROUT) |
| `d{N}.r11n` | string | Rotina livre (nome custom) |
| `d{N}.body{0-3}` | boolean | Body: agua, alimentacao, movimento, treino |
| `d{N}.life{0-3}` | boolean | Life: cachorros, casa, higiene, administrativo |
| `d{N}.log` | string | Registro do dia (texto livre) |
| `d{N}.cap` | string | Capture it do dia |
| `d{N}.notes` | string | Notas do dia |
| `d{N}.chaos{0-4}` | boolean | Chaos Mode checks |
| `d{N}.chaosmain` | string | Compromisso principal (Chaos) |
| `d{N}.chaosnext` | string | Proxima coisa (Chaos) |
| `d{N}.alc` | boolean | Alcool no dia |
| `ov.{N}` | string | Overview - compromisso do dia N |
| `ovf.{0-6}` | string | Overview - campos fixos (eventos, viagens...) |
| `rmm.{0-3}` | string | RMM - 4 perguntas |
| `prio.{0-4}` | string | Prioridades do mes (3-5) |
| `kpi.{R}.{C}` | string | KPIs - area R, coluna C |
| `bl.fazer` | string[] | Backlog - Fazer |
| `bl.viver` | string[] | Backlog - Viver |
| `bl.ideias` | string[] | Backlog - Ideias |
| `bl.resolver` | string[] | Backlog - Resolver |
| `cr.{N}.obj/cr/dt/p/ok/res` | mixed | Guindastes (6 slots) |
| `acc.*` | string | Accountability table |
| `gu.*` | string | Glow Up medidas |
| `gu.photos` | string | Glow Up fotos |
| `gu.feel` | string | Glow Up sentimento |
| `ct.{N}.t/f/i/s{0-4}` | mixed | Content backlog (8 slots) |
| `w{W}.prio.{0-2}` | string | Prioridades da semana W |
| `w{W}.tr` | string | Treinos da semana |
| `w{W}.acc.*` | string | Accountability semanal |
| `w{W}.notes` | string | Notas da semana |
| `db.{N}.want/what/f{0-7}/exp` | mixed | Debug entries |
| `debug.count` | number | Quantidade de debug entries |
| `capture` | string[] | Inbox global (Capture It) |
| `lab` | string[] | System Lab entries |
| `rr.*` | string | Route Review campos |
| `mr.{N}.r/n` | string | Monthly Review areas |
| `mr.learn` | string | Monthly Review aprendizado |
| `nm.{0-5}` | string | Next Month campos |
| `br.{0-7}` | string | Body Review campos |
| `nov.rmm.{0-3}` | string | November RMM perguntas |
| `nov.prio.{0-4}` | string | November prioridades |

## Rotinas (ROUT) - indice para d{N}.r{i}

| i | Rotina |
|---|---|
| 0 | leitura (pomodoro) |
| 1 | treino |
| 2 | estudo / idioma |
| 3 | trabalho focado |
| 4 | casa |
| 5 | cachorros passeio |
| 6 | conteudo |
| 7 | agua |
| 8 | sono 7h+ |
| 9 | alimentacao ok |
| 10 | administrativo |
| 11 | livre (custom) |

## Checkpoints (CP) - indice para d{N}.cp{i}

| i | Checkpoint |
|---|---|
| 0 | Manha |
| 1 | 2 Pomodoros |
| 2 | Almoco |
| 3 | Tarde |
| 4 | Fim do trabalho |
| 5 | Noite |

## Schema futuro (Supabase)

### Tabelas estruturadas

```sql
-- Rotinas diarias (booleanos)
CREATE TABLE day_routines (
  day       DATE NOT NULL,
  routine   TEXT NOT NULL,  -- 'leitura', 'treino', etc.
  done      BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (day, routine)
);

-- Checkpoints
CREATE TABLE day_checkpoints (
  day       DATE NOT NULL,
  slot      SMALLINT NOT NULL,  -- 0-5
  done      BOOLEAN DEFAULT FALSE,
  note      TEXT,
  PRIMARY KEY (day, slot)
);

-- Top 3
CREATE TABLE day_top3 (
  day       DATE NOT NULL,
  position  SMALLINT NOT NULL,  -- 0-2
  task      TEXT,
  done      BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (day, position)
);

-- Body & Life checks
CREATE TABLE day_checks (
  day       DATE NOT NULL,
  category  TEXT NOT NULL,  -- 'body' ou 'life'
  item      TEXT NOT NULL,  -- 'agua', 'cachorros', etc.
  done      BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (day, category, item)
);
```

### Texto livre (indice vetorial)

```sql
-- Registros de texto (chunks para RAG)
CREATE TABLE day_texts (
  id        SERIAL PRIMARY KEY,
  day       DATE NOT NULL,
  type      TEXT NOT NULL,  -- 'log', 'capture', 'notes', 'now'
  content   TEXT,
  week      SMALLINT,
  embedding VECTOR(1536)    -- pgvector
);
```

### Eventos de uso (instrumentacao)

```sql
CREATE TABLE app_events (
  id        SERIAL PRIMARY KEY,
  ts        TIMESTAMPTZ DEFAULT NOW(),
  view      TEXT NOT NULL,  -- 'dash', 'today', 'chaos', etc.
  action    TEXT NOT NULL,  -- 'open', 'edit', 'check', 'export'
  meta      JSONB           -- dados extras
);
```

## Decisoes de design

1. **Grao: dia x tipo** - nao mes. Cada chunk cabe em centenas de tokens.
2. **Estruturado vs. texto**: rotinas/checkpoints sao filtro SQL; registro/captura sao RAG.
3. **Contrato antes de backend**: o schema do JSON e o produto de dados.
4. **Metrica alvo**: tokens por pergunta respondida, com e sem filtro estruturado.
