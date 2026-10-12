#!/usr/bin/env python3
"""Generate the A5 print planner (HTML -> PDF) for October 2026 — Expansion Sprint 01."""
import calendar
import datetime as dt
from pathlib import Path

OUT = Path(__file__).parent / "dist"
OUT.mkdir(exist_ok=True)

YEAR, MONTH = 2026, 10
MONTH_NAME = "OCTOBER"
SPRINT = "Expansion Sprint 01"
THEME = "EXPANSION"
SENTENCE = "Construir um sistema no qual eu consiga executar a vida que quero viver."

WD_PT = ["SEGUNDA", "TERÇA", "QUARTA", "QUINTA", "SEXTA", "SÁBADO", "DOMINGO"]
WD_SHORT = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]

days = [dt.date(YEAR, MONTH, d) for d in range(1, calendar.monthrange(YEAR, MONTH)[1] + 1)]
sundays = [d for d in days if d.weekday() == 6]
ROUTE_REVIEW = sundays[-2]  # penúltimo domingo
MONTH_REVIEW = sundays[-1]  # último domingo
RMM_DAY = dt.date(YEAR, MONTH, 27)

# weeks (Mon–Sun), partial first/last
weeks = []
cur = []
for d in days:
    cur.append(d)
    if d.weekday() == 6:
        weeks.append(cur)
        cur = []
if cur:
    weeks.append(cur)

# ---------------------------------------------------------------- helpers
pages = []  # list of (code, html, section)


def add(code, html, section, cls=""):
    pages.append({"code": code, "html": html, "section": section, "cls": cls})


def lines(n, h=10, cls=""):
    return "".join(f'<div class="line {cls}" style="height:{h}mm"></div>' for _ in range(n))


def dots(h):
    return f'<div class="dots" style="height:{h}mm"></div>'


def box(label, h, kind="dots", hint=""):
    inner = dots(h) if kind == "dots" else lines(int(h // 10), 10) if kind == "lines" else f'<div style="height:{h}mm"></div>'
    hint_html = f'<span class="hint">{hint}</span>' if hint else ""
    return f'<section class="box"><h3>{label}{hint_html}</h3>{inner}</section>'


def checks(items, cols=2):
    lis = "".join(f'<li><span class="cb"></span>{i}</li>' for i in items)
    return f'<ul class="checks cols{cols}">{lis}</ul>'


def h1(t, sub=""):
    s = f'<p class="sub">{sub}</p>' if sub else ""
    return f'<header class="ph"><h1>{t}</h1>{s}</header>'


def q(t):
    return f'<p class="q">{t}</p>'


def fmt(d):
    return f"{d.day:02d} OUT · {WD_SHORT[d.weekday()]}"


# ---------------------------------------------------------------- 01 COVER
add("", f"""
<div class="cv">
  <div class="bar"></div>
  <svg viewBox="0 0 100 100" fill="none" stroke="#D9A63A" stroke-width="1.4"><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(0.0 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(25.714285714285715 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(51.42857142857143 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(77.14285714285714 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(102.85714285714286 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(128.57142857142858 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(154.28571428571428 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(180.0 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(205.71428571428572 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(231.42857142857142 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(257.14285714285717 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(282.85714285714283 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(308.57142857142856 50 50)"/><ellipse cx="50" cy="20" rx="5" ry="15" transform="rotate(334.2857142857143 50 50)"/><circle cx="50" cy="50" r="15" stroke="#1F2B3C"/><circle cx="50" cy="50" r="9" stroke="#1F2B3C" stroke-dasharray="1.5 2"/></svg>
  <p class="eyebrow">Personal Operating System</p>
  <h1>{MONTH_NAME}<br>2026</h1>
  <p class="theme">{THEME}</p>
  <p class="sprint">{SPRINT}</p>
  <p class="sentence">“{SENTENCE}”</p>
  <p class="owner">Flávia</p>
</div>
""", "start", "cover")

# ---------------------------------------------------------------- 02 COMO USAR / ÍNDICE
add("MAPA", h1("Onde eu escrevo isso?", "Mapa do planner — a resposta deve ser óbvia") + """
<table class="map">
<tr><td class="k">Como uso isso tudo?</td><td>GUIA DE USO <b>GUIA</b> — dia · semana · mês · exemplo</td></tr>
<tr><td class="k">Pipocou um pensamento</td><td>CAPTURE IT (hoje, pág. direita) ou INBOX <b>C</b></td></tr>
<tr><td class="k">O dia já começou caótico</td><td>CHAOS MODE <b>X</b> — só 5 coisas</td></tr>
<tr><td class="k">O que importa este mês</td><td>RMM <b>M1</b> · Prioridades <b>M2</b></td></tr>
<tr><td class="k">Compromisso / data</td><td>OVERVIEW <b>O</b> · Semana <b>W</b> · Dia <b>D</b></td></tr>
<tr><td class="k">Qual é a próxima ação</td><td>Dia <b>D</b> → AGORA</td></tr>
<tr><td class="k">Hora de parar e olhar</td><td>Dia <b>D</b> → CHECKPOINTS</td></tr>
<tr><td class="k">Quero fazer / viver algum dia</td><td>BACKLOG <b>B</b></td></tr>
<tr><td class="k">Preciso de alguém me puxando</td><td>GUINDASTES <b>G</b> · ACCOUNTABILITY <b>A</b></td></tr>
<tr><td class="k">Corpo, peso, treino, fotos</td><td>GLOW UP <b>GU</b></td></tr>
<tr><td class="k">Ideia de conteúdo</td><td>CONTENT <b>CT</b></td></tr>
<tr><td class="k">Algo não aconteceu</td><td>DEBUG <b>DB</b></td></tr>
<tr><td class="k">“Seria melhor se o planner…”</td><td>SYSTEM LAB <b>L</b> — não altere, registre</td></tr>
<tr><td class="k">Dia 18 · penúltimo domingo</td><td>ROUTE REVIEW <b>R1</b></td></tr>
<tr><td class="k">Dia 25 · último domingo</td><td>MONTHLY REVIEW <b>R2</b> · BODY REVIEW <b>R3</b></td></tr>
<tr><td class="k">Dia 27 · RMM</td><td>NOVEMBER RMM <b>N</b></td></tr>
</table>
<p class="rule">Regra do mês: <b>USAR → OBSERVAR → REGISTRAR.</b> Não redesenhar. Ideias de melhoria vão para o SYSTEM LAB.</p>
<p class="rule small">Códigos ficam no rodapé de cada página. As bordas coloridas marcam a seção: azul-escuro = início · amarelo = mês · cinza = semanas/dias (a marca desce a cada semana) · azul = review & lab.</p>
""", "start")

# ---------------------------------------------------------------- 02b GUIA DE USO (4 pages)
def guide(title, sub, blocks):
    html = h1(title, sub) + '<div class="guide">'
    for head, body in blocks:
        html += f'<section class="g"><h3>{head}</h3>{body}</section>'
    return html + '</div>'


def ol(items):
    return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'


def ul(items):
    return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


add("GUIA", guide("GUIA DE USO · O DIA", "passo a passo · detalhe é o que reduz a fricção", [
    ("1 · ABRIR (manhã · 5 min · café)", ol([
        "Abra na página de hoje (<b>D</b>). A borda cinza da semana ajuda a achar.",
        "Olhe a SEMANA (<b>W</b>) ao lado: quais compromissos e prioridades da semana tocam hoje?",
        "Escreva o <b>TOP 3</b>: três coisas que, feitas, fazem o dia valer. Não são tarefas soltas — são as que puxam o mês (M2).",
        "Preencha o <b>AGORA</b> com a primeira microação, pequena a ponto de ser quase ridícula. <i>Ex.: “abrir o Anki” em vez de “estudar inglês”.</i>",
        "Se o dia já começou torto: pule tudo e vá para o <b>CHAOS MODE (X)</b>."])),
    ("2 · EXECUTAR (ao longo do dia)", ol([
        "Trabalhe em blocos (pomodoro 25/5 ou 50/10). Um bloco = uma linha no <b>REGISTRO DO DIA</b> (pág. direita).",
        "Terminou algo do TOP 3? Risque. Não terminou? Tudo bem — escreva o próximo passo no AGORA.",
        "Pipocou pensamento, ideia, coisa pra comprar, mensagem pra responder? <b>CAPTURE IT</b>. Não resolva agora; só anote.",
        "Em cada <b>CHECKPOINT</b> (manhã · 2 pomodoros · almoço · tarde · fim do trabalho · noite) marque o quadrado e responda em uma linha: <i>onde estou · o que apareceu · próxima ação · mudo de contexto?</i>"])),
    ("3 · FECHAR (noite · 10 min)", ol([
        "Marque o <b>FEITO HOJE</b>: leitura, treino, estudo, trabalho focado, casa, cachorros, conteúdo, água, sono… Cada quadradinho é um dado para a review.",
        "Complete o <b>REGISTRO DO DIA</b> com detalhe: <i>“pomodoro leitura cap. 4 · treino pernas 45 min · passeio cães 30 min · 3 blocos de foco no relatório”</i>. Quanto mais específico, menos você depende de memória.",
        "Marque BODY e LIFE. Anote em <b>NOTAS</b> um sentimento ou aprendizado do dia (uma frase basta).",
        "Passe os olhos no CAPTURE IT: o que vira tarefa vai para o TOP 3 de amanhã, para a semana (W) ou para o BACKLOG (B). O resto, risque.",
        "Escreva o TOP 3 de amanhã antes de dormir, se tiver energia. Se não, fica para o café."])),
]), "start")

add("GUIA", guide("GUIA DE USO · SEMANA E MÊS", "rituais fixos · sempre no mesmo dia, sempre do mesmo jeito", [
    ("DOMINGO · PLANEJAR A SEMANA (20 min)", ol([
        "Abra a página da SEMANA (<b>W</b>). Copie compromissos do OVERVIEW (<b>O</b>) e da agenda do celular para a lista de dias.",
        "Escolha 3 <b>PRIORIDADES</b> que avançam as prioridades do mês (M2). Se não avança nada do M2, não é prioridade.",
        "Preencha <b>TREINOS</b> (dia, tipo, horário) e <b>ACCOUNTABILITY</b>: quem espera por você esta semana (amiga do treino, coworking, grupo, post prometido).",
        "Olhe o INBOX (<b>C</b>) e o CAPTURE IT da semana passada: processe — tarefa, backlog ou lixo.",
        "Conte os FEITO HOJE dos 7 dias: quantos treinos? quantos pomodoros de leitura? Anote em NOTAS da semana e no tracker do GLOW UP (GU)."])),
    ("DIA 18 · ROUTE REVIEW (<b>R1</b>)", ol([
        "Penúltimo domingo. Vá até R1 e responda CONTINUE / STOP / START / CHANGE olhando os registros diários — não a memória.",
        "Escolha até 2 experimentos para testar até o dia 31. Escreva-os também no SYSTEM LAB (L)."])),
    ("DIA 25 · MONTHLY REVIEW (<b>R2</b>) + BODY REVIEW (<b>R3</b>)", ol([
        "Some os dados: FEITO HOJE, tracker do GLOW UP (GU), KPIs (K). Dê nota 1–5 por área.",
        "Responda “o que este mês me ensinou?” e esboce novembro na página NEXT MONTH."])),
    ("DIA 27 · RMM DE NOVEMBRO (<b>N</b>)", ol([
        "Leia SYSTEM LAB (L) e DEBUG (DB) inteiros. Decida o que muda no planner de novembro — só agora.",
        "Defina tema, 3–5 prioridades, KPIs e guindastes de novembro. Gere a versão 02."])),
    ("REGRA DO MÊS", '<p>USAR → OBSERVAR → REGISTRAR. Se algo no planner incomoda, anote no <b>SYSTEM LAB (L)</b> e siga usando. O redesenho é dia 27.</p>'),
]), "start")

add("GUIA", guide("GUIA DE USO · O QUE VAI ONDE", "regras de decisão para não travar na hora de escrever", [
    ("TOP 3 vs. FEITO HOJE vs. REGISTRO", ul([
        "<b>TOP 3</b> é intenção: escrito de manhã, 3 itens, no máximo.",
        "<b>FEITO HOJE</b> é hábito: quadradinhos de rotinas repetidas (leitura, treino, cães…). Marca-se, não se escreve.",
        "<b>REGISTRO DO DIA</b> é evidência: o que de fato aconteceu, com detalhe (o quê · quanto tempo · como foi)."])),
    ("CAPTURE IT vs. INBOX (C) vs. NOTAS", ul([
        "<b>CAPTURE IT</b> (página do dia): tudo que pipoca durante o dia. Rápido, feio, sem filtro.",
        "<b>INBOX (C)</b>: quando a página do dia não está à mão, ou coisas que não pertencem a nenhum dia.",
        "<b>NOTAS</b>: reflexões, frases, sentimentos, coisas que quer lembrar na review."])),
    ("BACKLOG (B) vs. OVERVIEW (O) vs. SEMANA (W)", ul([
        "Tem data? → <b>OVERVIEW</b> e depois <b>SEMANA</b>.",
        "Não tem data mas quero fazer/viver/resolver? → <b>BACKLOG</b>.",
        "Vai acontecer esta semana? → <b>SEMANA</b>, e no dia certo vira TOP 3."])),
    ("GUINDASTES (G) vs. ACCOUNTABILITY (A)", ul([
        "<b>Guindaste</b> é estrutura externa que puxa por semanas: competição, curso, evento, dinheiro investido, compromisso público.",
        "<b>Accountability</b> é pessoa/grupo específico numa semana específica: treino com a Ana, coworking terça."])),
    ("DEBUG (DB) vs. SYSTEM LAB (L)", ul([
        "Algo <i>na minha vida</i> não aconteceu como queria? → <b>DEBUG</b> (causa · condição · próximo teste).",
        "Algo <i>no planner</i> não funciona? → <b>SYSTEM LAB</b>. Não altere agora, registre."])),
    ("GLOW UP (GU) vs. BODY (dia)", ul([
        "<b>BODY</b> no dia: 4 quadrados, marcar e seguir.",
        "<b>GLOW UP</b>: o projeto do mês — tracker, medidas, fotos, tendência. Preencher 1× por semana, no domingo."])),
]), "start")

add("GUIA", guide("EXEMPLO · UM DIA PREENCHIDO", "como fica na prática · uma quinta-feira comum", [
    ("TOP 3", ol(["Fechar relatório X (3 blocos de foco)", "Treino pernas 18h com Ana", "Gravar 1 story sobre o livro"])),
    ("AGORA", '<p class="ex">→ abrir o arquivo do relatório e escrever o título da seção 2</p>'),
    ("CHECKPOINTS", ul([
        "<b>MANHÃ</b> ☑ estou na mesa · cães passeados · próxima: bloco 1 relatório",
        "<b>2 POMODOROS</b> ☑ seção 2 pronta · pipocou: renovar CNH (→ capture) · próxima: bloco 2",
        "<b>ALMOÇO</b> ☑ comi bem · cansada · próxima: 15 min leitura, depois bloco 3",
        "<b>FIM DO TRABALHO</b> ☑ relatório 80% · amanhã: revisar tabela · próxima: trocar de roupa p/ treino",
        "<b>NOITE</b> ☑ treino feito · story gravado · próxima: registro do dia + TOP 3 de amanhã"])),
    ("FEITO HOJE", '<p class="ex">☑ leitura (1 pomodoro) · ☑ treino · ☐ estudo/idioma · ☑ trabalho focado (3 blocos) · ☑ cachorros passeio · ☑ casa · ☑ conteúdo · ☑ água · ☐ sono 7h+</p>'),
    ("REGISTRO DO DIA", ul([
        "07:10 passeio cães 30 min, sol · 07:45 café + planner",
        "08:30–10:00 relatório X: 2 blocos, seção 2 pronta",
        "18:00 treino pernas 45 min c/ Ana — agachamento 40 kg, melhor que semana passada",
        "20:30 story gravado em 1 take · louça · roupa na máquina"])),
    ("CAPTURE IT", '<p class="ex">renovar CNH · ideia post “planner ADHD” · comprar ração · perguntar à Ju sobre o curso · hotel em Paraty</p>'),
    ("NOTAS", '<p class="ex">Dia bom. Blocos de manhã rendem mais; tarde é para tarefas leves. Testar isso amanhã.</p>'),
]), "start")

# ---------------------------------------------------------------- 03 CHAOS MODE
add("X", h1("CHAOS MODE", "Quando o dia já começou desorganizado. Só isto.") + """
<ul class="checks big">
<li><span class="cb"></span>banheiro / higiene</li>
<li><span class="cb"></span>água</li>
<li><span class="cb"></span>cachorros</li>
<li><span class="cb"></span>alimentação</li>
<li><span class="cb"></span>compromisso principal: <span class="fill"></span></li>
</ul>
""" + box("Qual é a próxima coisa que evita que o dia desande?", 48, "lines") +
    '<p class="rule small">Depois disso, volte para a página de hoje (D). Não tente recuperar o dia inteiro — só a próxima coisa.</p>', "start")

# ---------------------------------------------------------------- 04 CAPTURE INBOX (2 pages)
for i in (1, 2):
    add("C", h1("CAPTURE IT", "Inbox do mês · capturar não significa executar") +
        '<p class="rule small">Banho · dentes · cachorro · boleto · mensagem · tarefa · ideia · conteúdo · estudo · viagem · casa. Organize depois, no checkpoint.</p>' +
        lines(14, 10), "start")

# ---------------------------------------------------------------- 05 OVERVIEW (3 pages)
cal_rows = ""
for wk in calendar.Calendar(0).monthdayscalendar(YEAR, MONTH):
    cells = ""
    for d in wk:
        if d == 0:
            cells += "<td></td>"
        else:
            mark = ""
            if d == ROUTE_REVIEW.day: mark = '<span class="mk">R1</span>'
            if d == MONTH_REVIEW.day: mark = '<span class="mk">R2</span>'
            if d == RMM_DAY.day: mark = '<span class="mk">RMM</span>'
            cells += f"<td><span class='dn'>{d}</span>{mark}</td>"
    cal_rows += f"<tr>{cells}</tr>"
add("O", h1("MONTHLY OVERVIEW", f"{MONTH_NAME} 2026 · visão do ciclo inteiro") + f"""
<table class="cal">
<tr>{''.join(f'<th>{w}</th>' for w in WD_SHORT)}</tr>{cal_rows}
</table>
<div class="grid2">
{box("Grandes acontecimentos", 30, "lines")}
{box("Viagens", 30, "lines")}
{box("Eventos", 30, "lines")}
{box("Consultas", 30, "lines")}
</div>
""", "month")

half = (len(days) + 1) // 2
for part, chunk in enumerate((days[:half], days[half:])):
    rows = "".join(
        f'<tr class="{"sun" if d.weekday()==6 else ""}"><td class="d">{d.day:02d}</td><td class="w">{WD_SHORT[d.weekday()]}</td><td class="ln">'
        + ('<span class="tag">Route Review</span>' if d == ROUTE_REVIEW else '<span class="tag">Monthly Review</span>' if d == MONTH_REVIEW else '<span class="tag">RMM</span>' if d == RMM_DAY else '')
        + '</td></tr>' for d in chunk)
    add("O", h1("COMPROMISSOS DO MÊS", "Um dia por linha · compromissos, prazos, treinos importantes, social") +
        f'<table class="daylist">{rows}</table>', "month")

# ---------------------------------------------------------------- 06 RMM (2 pages)
add("M1", h1("OCTOBER RMM", "Reunião Mensal · definida no dia 27 de setembro") +
    box("O que quero viver?", 36, "lines") + box("O que quero construir?", 36, "lines") +
    box("O que quero melhorar?", 36, "lines") + box("O que quero experimentar?", 36, "lines"), "month")
add("M2", h1("PRIORIDADES DO MÊS", "3 a 5. Não mais do que isso.") +
    "".join(f'<div class="prio"><span class="n">{i}</span><div class="pl">{lines(2, 11)}</div></div>' for i in range(1, 6)) +
    '<p class="rule small">Se tudo é prioridade, nada é. Ao ler esta página, a resposta para “o que importa?” deve levar 5 segundos.</p>', "month")

# ---------------------------------------------------------------- 07 KPIs
kpi_rows = ""
for area, ex in [("CORPO", "treinos · movimento · álcool · peso · medidas · fotos"),
                 ("CARREIRA", "entregas · estudos · networking · AI/Data"),
                 ("IDIOMAS", "inglês · italiano"),
                 ("CRIAÇÃO", "conteúdos · artigos · ideias desenvolvidas"),
                 ("FINANÇAS", "gastos · economia · viagem")]:
    kpi_rows += f'<tr><td class="area">{area}<small>{ex}</small></td><td></td><td></td><td></td><td></td></tr>'
add("K", h1("MONTHLY KPIs", "Escolha só os indicadores relevantes a este ciclo. Deixe áreas em branco se não importarem agora.") +
    f'<table class="kpi"><tr><th>Área</th><th>KPI</th><th>Início</th><th>Meta</th><th>Fim</th></tr>{kpi_rows}</table>', "month")

# ---------------------------------------------------------------- 08 BACKLOG (2 pages)
add("B", h1("MONTHLY BACKLOG", "Quero fazer / viver / resolver · não precisa acontecer tudo este mês") +
    box("FAZER", 72, "lines") + box("VIVER", 72, "lines"), "month")
add("B", h1("MONTHLY BACKLOG", "continuação") + box("IDEIAS", 72, "lines") + box("RESOLVER (administrativo, casa, contas)", 72, "lines"), "month")

# ---------------------------------------------------------------- 09 GUINDASTES
card = """<div class="gcard">
<div class="gr"><b>Objetivo</b><span class="fill"></span></div>
<div class="gr"><b>Guindaste</b><span class="fill"></span></div>
<div class="gr half"><b>Data</b><span class="fill"></span><b>Pessoa</b><span class="fill"></span></div>
<div class="gr half"><b>Confirmado?</b><span class="cb"></span> sim <span class="cb"></span> não <b>Resultado</b><span class="fill"></span></div>
</div>"""
add("G", h1("GUINDASTES", "Quem ou o quê está me puxando? Pessoa · compromisso · grupo · competição · evento · publicação · aula · prazo · dinheiro investido") + card * 4, "month")

# ---------------------------------------------------------------- 10 ACCOUNTABILITY
acc_rows = "".join('<tr><td></td><td></td><td></td><td></td><td class="c"><span class="cb"></span></td></tr>' for _ in range(6))
add("A", h1("ACCOUNTABILITY", "Treinos com amigos · videochamada · coworking · stories · GymRats · grupos") +
    f'<table class="acc"><tr><th>Dia</th><th>Pessoa</th><th>Atividade</th><th>Hora</th><th>✓</th></tr>{acc_rows}</table>' +
    box("Outros compromissos de exposição (stories, grupos, chamadas)", 70, "lines"), "month")

# ---------------------------------------------------------------- 11 GLOW UP (2 pages)
gu_rows = "".join(f'<tr><td class="area">{w}</td><td></td><td></td><td></td><td></td><td></td></tr>' for w in ["Início", "Sem 1", "Sem 2", "Sem 3", "Sem 4", "Fim"])
add("GU", h1("GLOW UP", "Projeto do mês · tendências, não um número isolado") +
    f'<table class="gu"><tr><th></th><th>Peso</th><th>Cintura</th><th>Quadril</th><th>Braço</th><th>Coxa</th></tr>{gu_rows}</table>' +
    '<div style="margin:3mm 0 6mm">' + checks(["fotos início", "fotos fim", "bioimpedância"], 3) + '</div>' +
    box("Como estou me sentindo / tendência", 60, "lines"), "month")
wk_cells = "".join(f'<td class="area">Sem {i}</td>' + "<td></td>" * 7 for i in range(1, 6))
tracker = "<table class='trk'><tr><th></th>" + "".join(f"<th>{w}</th>" for w in WD_SHORT) + "</tr>" + \
    "".join(f"<tr><td class='area'>Sem {i}</td>" + "<td></td>" * 7 + "</tr>" for i in range(1, 6)) + "</table>"
add("GU", h1("GLOW UP · TRACKER", "Marque o dia: T treino · M movimento · A álcool · H água ok · ✓ alimentação") + tracker +
    box("Notas (alimentação, energia, sono, ciclo)", 80, "lines"), "month")

# ---------------------------------------------------------------- 12 CONTENT BACKLOG
ccard = """<div class="gcard">
<div class="gr"><b>Tema</b><span class="fill"></span><b>Formato</b><span class="fill short"></span></div>
<div class="gr"><b>Ideia</b><span class="fill"></span></div>
<div class="gr"><b>Plataforma</b><span class="fill"></span></div>
<div class="gr status"><b>Status</b>
<span class="cb"></span>capturada <span class="cb"></span>roteiro <span class="cb"></span>gravar <span class="cb"></span>editar <span class="cb"></span>publicar</div>
</div>"""
add("CT", h1("CONTENT BACKLOG", "Ideia de conteúdo → capturar → criar depois. Se precisar gravar agora: câmera → grava → fecha → volta.") + ccard * 4, "month")

# ---------------------------------------------------------------- 13 WEEKS + DAYS
ROUTINES = ["leitura (pomodoro)", "treino", "estudo / idioma", "trabalho focado", "casa", "cachorros passeio",
            "conteúdo", "água", "sono 7h+", "alimentação ok", "administrativo", '<span class="fill"></span>']
CHECKPOINTS = [("MANHÃ", "morning"), ("2 POMODOROS", "2-pomodoro"), ("ALMOÇO", "lunch"),
               ("TARDE", "afternoon"), ("FIM DO TRABALHO", "work shutdown"), ("NOITE", "night")]


def week_pages(i, wk):
    rng = f"{wk[0].day:02d}–{wk[-1].day:02d} OUT"
    comp = "".join(f'<tr class="{"sun" if d.weekday()==6 else ""}"><td class="d">{d.day:02d}</td><td class="w">{WD_SHORT[d.weekday()]}</td><td class="ln"></td></tr>' for d in wk)
    left = h1(f"SEMANA {i}", rng) + \
        '<section class="box"><h3>PRIORIDADES</h3>' + "".join(f'<div class="prio"><span class="n">{n}</span><div class="pl">{lines(1, 11)}</div></div>' for n in (1, 2, 3)) + '</section>' + \
        f'<section class="box"><h3>COMPROMISSOS</h3><table class="daylist wk">{comp}</table></section>' + \
        box("TREINOS", 40, "lines")
    acc = "".join('<tr><td></td><td></td><td></td><td class="c"><span class="cb"></span></td></tr>' for _ in range(3))
    right = h1(f"SEMANA {i}", "accountability · notas · captura") + \
        f'<section class="box"><h3>ACCOUNTABILITY <span class="hint">quem espera por mim esta semana</span></h3><table class="acc"><tr><th>Dia</th><th>Pessoa</th><th>O quê</th><th>✓</th></tr>{acc}</table></section>' + \
        box("NOTAS + CAPTURA", 108, "dots")
    add(f"W{i}", left, f"week{i}")
    add(f"W{i}", right, f"week{i}")


def day_pages(d, wi):
    banner = ""
    if d == ROUTE_REVIEW:
        banner = '<p class="banner">HOJE · ROUTE REVIEW → R1</p>'
    elif d == MONTH_REVIEW:
        banner = '<p class="banner">HOJE · MONTHLY REVIEW → R2 · BODY REVIEW → R3</p>'
    elif d == RMM_DAY:
        banner = '<p class="banner">HOJE · RMM — NOVEMBER → N</p>'
    cps = "".join(f'<tr><td class="c"><span class="cb"></span></td><td class="lbl">{a}</td><td class="ln"></td></tr>' for a, _ in CHECKPOINTS)
    left = f'<header class="ph day"><h1>{d.day:02d}</h1><div><p class="wd">{WD_PT[d.weekday()]}</p><p class="sub">OUT 2026 · SEMANA {wi}</p></div></header>' + banner + \
        '<section class="box"><h3>TOP 3</h3>' + "".join(f'<div class="prio"><span class="n">{n}</span><div class="pl">{lines(1, 12)}</div></div>' for n in (1, 2, 3)) + '</section>' + \
        box("AGORA", 20, "lines", "qual é a próxima microação?") + \
        f'<section class="box"><h3>CHECKPOINTS <span class="hint">onde estou · o que apareceu · próxima ação · mudar contexto?</span></h3><table class="cp">{cps}</table></section>' + \
        '<div class="grid2 tight"><section class="box"><h3>BODY</h3>' + checks(["água", "alimentação", "movimento", "treino"], 2) + '</section>' + \
        '<section class="box"><h3>LIFE</h3>' + checks(["cachorros", "casa", "higiene", "administrativo"], 2) + '</section></div>'
    right = f'<header class="ph day small"><h1>{d.day:02d}</h1><div><p class="wd">{WD_SHORT[d.weekday()]}</p></div></header>' + \
        '<section class="box"><h3>FEITO HOJE <span class="hint">marque o que aconteceu</span></h3>' + checks(ROUTINES, 3) + '</section>' + \
        box("REGISTRO DO DIA", 73, "lines", "o quê · quanto tempo · como foi") + \
        box("CAPTURE IT", 40, "dots", "tudo que pipocar — organizar depois") + \
        box("NOTAS", 14, "dots")
    add(f"D{d.day:02d}", left, f"week{wi}")
    add(f"D{d.day:02d}", right, f"week{wi}")


for i, wk in enumerate(weeks, 1):
    week_pages(i, wk)
    for d in wk:
        day_pages(d, i)
        if d == ROUTE_REVIEW:
            add("R1", h1("ROUTE REVIEW", f"{fmt(d)} · penúltimo domingo · reflexão + reorganização de rota") +
                '<div class="grid2">' + box("CONTINUE · o que funcionou?", 34, "lines") + box("STOP · o que não funcionou?", 34, "lines") +
                box("START · o que quero começar?", 34, "lines") + box("CHANGE · o que precisa mudar?", 34, "lines") + '</div>' +
                box("BIGGEST BOTTLENECK", 20, "lines") + box("BIGGEST WIN", 20, "lines"), "review")
            add("R1", h1("ROUTE REVIEW", "perguntas de rota") +
                box("O que está consumindo minha atenção?", 34, "lines") + box("O que está me dando energia?", 34, "lines") +
                box("Onde estou falhando? Qual é o gargalo?", 34, "lines") + box("Quais experimentos testo até o dia 31?", 34, "lines"), "review")
        if d == MONTH_REVIEW:
            mr_rows = "".join(f'<tr><td class="area">{a}</td><td></td><td></td></tr>' for a in
                              ["Corpo / treinos", "Carreira", "Idiomas", "Conteúdo", "Finanças", "Experiências", "Relações", "Hábitos"])
            add("R2", h1("MONTHLY REVIEW", f"{fmt(d)} · último domingo · resultados do ciclo") +
                f'<table class="kpi rev"><tr><th>Área</th><th>Resultado / métrica</th><th>Nota 1–5</th></tr>{mr_rows}</table>' +
                box("O que este mês me ensinou?", 36, "lines"), "review")
            add("R2", h1("NEXT MONTH", "November — Expansion Sprint 02 · esboço") +
                '<div class="grid2">' + box("Prioridades", 40, "lines") + box("KPIs", 40, "lines") +
                box("Guindastes", 40, "lines") + box("Compromissos", 40, "lines") + '</div>' +
                box("Experimentos / sprints", 40, "lines"), "review")
            add("R3", h1("BODY REVIEW", "final do mês · tendências") +
                '<div class="grid2">' + box("O que mudou?", 30, "lines") + box("Como estou me sentindo?", 30, "lines") +
                box("Como está minha força?", 30, "lines") + box("Como estão minhas roupas?", 30, "lines") +
                box("Medidas · fotos · métricas mostram…", 30, "lines") + box("O que testo no próximo ciclo?", 30, "lines") + '</div>', "review")

# ---------------------------------------------------------------- DEBUG (3 pages)
for _ in range(3):
    add("DB", h1("DEBUG MY LIFE", "Quando algo não acontecer. Sem culpa — só diagnóstico.") +
        box("O que eu queria fazer?", 18, "lines") + box("O que aconteceu? Onde quebrou?", 28, "lines") +
        '<section class="box"><h3>QUAL FOI A FRICÇÃO?</h3>' +
        checks(["faltou clareza", "tarefa grande demais", "faltou guindaste", "ambiente atrapalhou", "Instagram capturou",
                "cansada / faminta", "trabalho ocupou o espaço", "outra demanda venceu"], 2) + '</section>' +
        box("Qual experimento vou testar?", 28, "lines"), "review")

# ---------------------------------------------------------------- SYSTEM LAB (2 pages)
for i in (1, 2):
    add("L", h1("SYSTEM LAB", "October feedback → November v2 · registre, não implemente") +
        ('<p class="rule small">Não funcionou · faltou · sobrou · página inútil · página apertada · difícil de achar · nova métrica · mudança de fluxo.</p>' if i == 1 else '') +
        lines(15 if i == 1 else 16, 10), "review")

# ---------------------------------------------------------------- NOVEMBER RMM
add("N", h1("NOVEMBER RMM", "Expansion Sprint 02 · dia 27 de outubro · use o SYSTEM LAB e o MONTHLY REVIEW como entrada") +
    box("O que quero viver?", 30, "lines") + box("O que quero construir?", 30, "lines") +
    box("O que quero melhorar?", 30, "lines") + box("O que quero experimentar?", 30, "lines") +
    '<section class="box"><h3>3–5 PRIORIDADES</h3>' + lines(3, 10) + '</section>', "review")

# pad to even page count so it prints as spreads
if len(pages) % 2:
    add("", '<div class="cv back"><p class="eyebrow">Notas</p></div>' + dots(160), "review")

# ---------------------------------------------------------------- render
CSS = (Path(__file__).parent / "print.css").read_text()
week_count = len(weeks)
body = []
for i, p in enumerate(pages, 1):
    side = "recto" if i % 2 else "verso"
    sec = p["section"]
    tab_style = ""
    if sec.startswith("week"):
        w = int(sec[4:])
        tab_style = f'style="top:{40 + (w - 1) * 28}mm"'
        sec_cls = "week"
    else:
        sec_cls = sec
    tab = f'<div class="tab {sec_cls}" {tab_style}></div>' if p["cls"] != "cover" else ""
    footer = f'<footer><span class="code">{p["code"]}</span><span class="pn">{i}</span></footer>' if p["cls"] != "cover" else ""
    body.append(f'<div class="page {side} {sec_cls} {p["cls"]}">{tab}<div class="content">{p["html"]}</div>{footer}</div>')

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>October 2026 — Expansion Sprint 01 · Planner A5</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(body)}</body></html>"""
(OUT / "october-2026-planner-A5.html").write_text(html)
print(f"pages: {len(pages)}")
