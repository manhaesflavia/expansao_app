# Expansao - Backlog

## Visao

O Expansao nao e um app de planner. E um **assistente pessoal adaptativo** que trapaceia a favor do cerebro TDAH. Ele puxa dados de onde voce ja esta, preve quando voce vai falhar, age quando voce esquece, e mostra que voce esta progredindo.

Regra: **se o usuario precisa de disciplina para usar o app, o app esta errado.**

---

## Sprint 01 - Outubro 2026 (ATUAL)

### Feito
- [x] App PWA funcionando (HTML self-contained, localStorage, offline)
- [x] Landing page publica
- [x] PDF A5 para impressao (106 paginas)
- [x] Repositorio Git organizado
- [x] Schema de dados documentado (DATA-SCHEMA.md)

### Em uso
- [ ] Usar o app por 10 dias antes da viagem
- [ ] Registrar no System Lab o que falta / nao funciona / tem friccao

---

## Sprint 02 - Novembro 2026

### Backend + Sync
- [ ] Supabase (Postgres + pgvector + auth)
- [ ] Trocar localStorage por sync automatico
- [ ] Schema DDL real (ver DATA-SCHEMA.md)
- [ ] Exportar vira so backup

### Modo Minimo Vital (porta de entrada)
- [ ] Tela unica ao abrir: microfone + "agora" + 5 checkboxes (agua, comida, remedio, cachorro, banho)
- [ ] Sem menu, sem navegacao. Voce abre e esta la
- [ ] Botao Chaos Mode fixo e visivel

### Comando por Voz
- [ ] Botao de microfone grande (Web Speech API no Chrome/Edge)
- [ ] Transcricao automatica
- [ ] Classificacao simples: captura / registro / debug / nota emocional
- [ ] Salva no lugar certo sem o usuario decidir
- [ ] "Surto mode": fala tudo, o app organiza depois

### Planos Flexiveis
- [ ] Criar plano novo a qualquer momento (viagem, curso, projeto)
- [ ] Cada plano com tarefas, datas, checklist proprios
- [ ] Dashboard mostra progresso de todos os planos ativos
- [ ] Plano concluido vira historico

---

## Sprint 03 - Dezembro 2026

### Integracoes (Hub)
- [ ] Google Agenda sync (compromissos entram sozinhos no Overview)
- [ ] Alexa Skill basica ("capturar" e "como foi meu dia")
- [ ] WhatsApp webhook (voce envia mensagem, vira Capture It)
- [ ] Wellhub/GymRats: check-in de treino detectado automaticamente
- [ ] Centralizar listas soltas do WhatsApp no app

### Inteligencia
- [ ] Classificacao por LLM (Claude API) do que entra por voz/texto
- [ ] RAG sobre registros (perguntar coisas sobre seus dados)
- [ ] MCP Server expondo tools (rotinas_da_semana, registro_do_dia)
- [ ] Metrica: tokens por pergunta respondida

### Comportamento Reativo (quando voce esquece)
- [ ] 3 dias sem abrir? Alexa/WhatsApp manda mini-resumo
- [ ] Nao e notificacao generica -- baseada nos seus dados reais
- [ ] Previsao de falha: "nas ultimas 3 semanas, quarta a tarde voce para"
- [ ] Sugestao de intervencao: "mover treino pra manha? marcar com alguem?"

---

## Sprint 04+ - 2027

### Gamificacao
- [ ] XP por acao (checkbox, registro, captura = pontos)
- [ ] Streaks flexiveis ("5 de 7 dias conta")
- [ ] Niveis por area (Corpo lv.3, Carreira lv.5, Casa lv.1)
- [ ] Badges ("10 treinos no mes", "usou Chaos Mode e voltou")
- [ ] Boss battles (meta do mes como chefao com barra de vida)
- [ ] Co-op mode (desafios com amigos, GymRats integrado)

### Progresso e Reforco Positivo
- [ ] Dashboard mostra O QUE VOCE JA FEZ, nao o que falta
- [ ] Frases baseadas em dados: "voce treinou 8 dias -- mais que setembro"
- [ ] Contagens e barras que so sobem
- [ ] Regra da metade: fazer metade conta como feito
- [ ] 3 vitorias do dia

### Deteccao de Triggers e Sugestoes
- [ ] Identificar padroes: "voce trava depois de reunioes longas"
- [ ] Identificar o que funciona: "treino de manha = dia 73% mais produtivo"
- [ ] Pareamento de tarefas: "serie + louca", "podcast + passeio caes"
- [ ] Sugestao de coisas para fazer em dupla
- [ ] "Da ultima vez que voce se sentiu assim, o treino ajudou"

### Adaptacao Continua
- [ ] Triagem inicial: perguntas sobre rotina, dificuldades, horarios
- [ ] App comeca com defaults e ajusta conforme uso real
- [ ] Rotinas, checkpoints e KPIs configuraveis pelo usuario
- [ ] "Travei ou nao quero?" no checkpoint (mecanica vs. proposito)

### Lacunas do Perfil (do laudo)
- [ ] Dinheiro: pagina mensal, lista de espera 48h para compras
- [ ] Casa: minimo diario 10 min, zona por dia da semana
- [ ] Tempo: "ate as __:__" no Agora, estimei vs. levou
- [ ] Memoria prospectiva: gatilhos "quando X -> faco Y"
- [ ] Minimos antes do trabalho (agua, comida, remedio) no topo do dia
- [ ] Saude: consultas, medicacao, efeitos observados

### Privacidade
- [ ] Seus dados, seu controle (tudo no seu Supabase)
- [ ] WhatsApp: voce envia para o bot, bot nao le suas conversas
- [ ] Wellhub: API publica de check-in, sem dados de saude
- [ ] Historico WPP: so importacao manual, sem acesso por API

---

## Portfolio (engenharia de dados)
- [ ] Artigo Medium reescrito com DDL, numeros de tokens, pipeline completo
- [ ] Schema: grao = dia x tipo (day_routine, checkpoint, capture, daily_log, review)
- [ ] Estruturado em tabelas, texto livre em indice vetorial
- [ ] Metrica: tokens por pergunta respondida, com e sem filtro estruturado
- [ ] Instrumentacao de uso: eventos {timestamp, view, action}

---

## Principios de design

1. **Zero friccao**: se precisa de disciplina para usar, esta errado
2. **Puxar, nao empurrar**: dados vem de onde voce ja esta
3. **Progresso visivel**: mostrar o feito, nunca o que falta
4. **Sem culpa**: linguagem positiva, regra da metade, Chaos Mode
5. **Adaptativo**: o app muda, nao o usuario
6. **Previsao > reacao**: prever falha e agir antes
7. **Voz primeiro**: quando o emocional transborda, digitar e impossivel
