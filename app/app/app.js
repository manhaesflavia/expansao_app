// ------------------------------------------------------------------ data

const Y = 2026, M = 10;
const DAYS = [...Array(31)].map((_, i) => new Date(Y, M - 1, i + 1));
const WD = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
      WS = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"];
const SUN = DAYS.filter(d => d.getDay() === 0).map(d => d.getDate());
const ROUTE = SUN[SUN.length - 2], MREV = SUN[SUN.length - 1], RMM = 27;

const WEEKS = [];
{
  let cur = [];
  for (const d of DAYS) {
    cur.push(d.getDate());
    if (d.getDay() === 0) {
      WEEKS.push(cur);
      cur = [];
    }
  }
  if (cur.length) WEEKS.push(cur);
}

const weekOf = day => WEEKS.findIndex(w => w.includes(day)) + 1;
const KEY = "planner-oct-2026";
let S = JSON.parse(localStorage.getItem(KEY) || "{}");
const save = () => localStorage.setItem(KEY, JSON.stringify(S));
const get = (k, def = "") => k in S ? S[k] : def;
const set = (k, v) => { S[k] = v; save(); };
const pad = n => String(n).padStart(2, "0");
const now = new Date();
let today = (now.getFullYear() === Y && now.getMonth() === M - 1) ? now.getDate() : 1;
let curDay = today,
    curWeek = weekOf(today),
    view = location.hash.slice(1) || "dash";

const CP = ["Manhã", "2 Pomodoros", "Almoço", "Tarde", "Fim do trabalho", "Noite"];
const ROUT = ["leitura (pomodoro)", "treino", "estudo / idioma", "trabalho focado", "casa", "cachorros passeio", "conteúdo", "água", "sono 7h+", "alimentação ok", "administrativo"];
const BODY = ["água", "alimentação", "movimento", "treino"],
      LIFE = ["cachorros", "casa", "higiene", "administrativo"];

// ------------------------------------------------------------------ widgets

const ed = (k, ph = "", cls = "") =>
  `<div class="ed ${cls}" contenteditable data-k="${k}" data-ph="${ph}">${esc(get(k))}</div>`;

const cb = (k, label, big = false) =>
  `<li class="${big ? "big" : ""}"><input type="checkbox" data-k="${k}" ${get(k, false) ? "checked" : ""}><span>${label}</span></li>`;

const esc = s =>
  String(s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

const H = (t, sub = "") =>
  `<h1>${t}</h1><p class="sub">${sub}</p>`;

const box = (t, k, cls = "mid", ph = "", hint = "") =>
  `<div class="card"><h3>${t}${hint ? `<span class="hint">${hint}</span>` : ""}</h3>${ed(k, ph, cls)}</div>`;

const numbered = (k, n, ph = "") =>
  [...Array(n)].map((_, i) =>
    `<div class="row"><span class="n">${i + 1}</span>${ed(`${k}.${i}`, ph, "one")}</div>`
  ).join("");

const list = (k, ph) => {
  const items = get(k, []);
  return `<div class="list" data-list="${k}">${items.map((v, i) =>
    `<div class="item"><div class="ed one" contenteditable data-list-k="${k}" data-i="${i}" data-ph="${ph}">${esc(v)}</div><button class="x" data-del="${k}" data-i="${i}" title="remover">×</button></div>`
  ).join("")}<button class="btn" data-add="${k}" style="margin-top:10px">+ adicionar</button></div>`;
};

const table = (k, cols, rows) =>
  `<table><tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr>${[...Array(rows)].map((_, r) =>
    `<tr>${cols.map((c, ci) =>
      `<td>${c === "✓"
        ? `<input type="checkbox" data-k="${k}.${r}.${ci}" ${get(`${k}.${r}.${ci}`, false) ? "checked" : ""}>`
        : ed(`${k}.${r}.${ci}`, "", "one")}</td>`
    ).join("")}</tr>`
  ).join("")}</table>`;

// ------------------------------------------------------------------ views

const V = {};

V.dash = () => {
  const d = curDay;
  const cpDone = CP.filter((_, i) => get(`d${d}.cp${i}`, false)).length;
  const top = [0, 1, 2].filter(i => get(`d${d}.topdone${i}`, false)).length;
  let treinos = 0;
  for (let x = 1; x <= 31; x++) if (get(`d${x}.body3`, false) || get(`d${x}.r1`, false)) treinos++;
  const rout = ROUT.filter((_, i) => get(`d${d}.r${i}`, false)).length;
  const lab = get("lab", []).length, cap = get("capture", []).length;
  const pri = [0, 1, 2, 3, 4].map(i => get(`prio.${i}`)).filter(Boolean);
  const dd = DAYS[d - 1];

  return H("Dashboard", `${pad(d)} de outubro · ${WD[dd.getDay()]} · semana ${weekOf(d)}`) +
    (d === ROUTE ? `<div class="banner">Hoje · Route Review → R1</div>` :
     d === MREV ? `<div class="banner">Hoje · Monthly Review → R2 · Body Review → R3</div>` :
     d === RMM ? `<div class="banner">Hoje · RMM — November → N</div>` : "") +
    `<div class="kpi">
      <div class="k"><b>${cpDone}/6</b><span>checkpoints hoje</span><div class="bar"><i style="width:${cpDone / 6 * 100}%"></i></div></div>
      <div class="k"><b>${top}/3</b><span>top 3 concluídos</span><div class="bar"><i style="width:${top / 3 * 100}%"></i></div></div>
      <div class="k"><b>${rout}/${ROUT.length}</b><span>rotinas feitas hoje</span><div class="bar"><i style="width:${rout / ROUT.length * 100}%"></i></div></div>
      <div class="k"><b>${treinos}</b><span>treinos no mês</span></div>
      <div class="k"><b>${cap}</b><span>itens no inbox · ${lab} no lab</span></div>
    </div>
    <div class="grid g2">
      <div class="card"><h3>O que importa <span class="hint">prioridades do mês</span></h3>${pri.length
        ? `<ol style="font-size:16px;margin:0;padding-left:24px">${pri.map(p => `<li>${esc(p)}</li>`).join("")}</ol>`
        : `<p class="rule">Defina em RMM → Prioridades.</p>`}</div>
      <div class="card"><h3>Agora <span class="hint">qual é a próxima microação?</span></h3>${ed(`d${d}.now`, "pegar roupa → vestir → tênis → sair…", "mid")}</div>
      <div class="card"><h3>Top 3 de hoje</h3>${[0, 1, 2].map(i =>
        `<div class="row"><input type="checkbox" data-k="d${d}.topdone${i}" ${get(`d${d}.topdone${i}`, false) ? "checked" : ""}>${ed(`d${d}.top${i}`, "", "one")}</div>`
      ).join("")}</div>
      <div class="card"><h3>Capture it <span class="hint">pipocou? escreva aqui</span></h3>${list("capture", "qualquer coisa que apareceu na cabeça")}</div>
    </div>
    <p class="rule">Regra do mês: <b>usar → observar → registrar.</b> Vontade de mudar o sistema? Vai para o System Lab.</p>`;
};

V.today = () => {
  const d = curDay, dd = DAYS[d - 1];
  const nav = `<div class="daynav">${DAYS.map(x =>
    `<button data-day="${x.getDate()}" class="${x.getDate() === d ? "on" : ""} ${x.getDate() === today ? "today" : ""}">${x.getDate()}</button>`
  ).join("")}</div>`;

  return H(`${pad(d)} · ${WD[dd.getDay()]}`, `Outubro 2026 · semana ${weekOf(d)} · D${pad(d)}`) + nav +
    (d === ROUTE ? `<div class="banner">Hoje · Route Review → R1</div>` :
     d === MREV ? `<div class="banner">Hoje · Monthly Review → R2 · Body Review → R3</div>` :
     d === RMM ? `<div class="banner">Hoje · RMM — November → N</div>` : "") +
    `<div class="grid g2">
     <div>
      <div class="card"><h3>Top 3</h3>${[0, 1, 2].map(i =>
        `<div class="row"><span class="n">${i + 1}</span><input type="checkbox" data-k="d${d}.topdone${i}" ${get(`d${d}.topdone${i}`, false) ? "checked" : ""}>${ed(`d${d}.top${i}`, "", "one")}</div>`
      ).join("")}</div>
      <div class="card"><h3>Agora <span class="hint">qual é a próxima microação?</span></h3>${ed(`d${d}.now`, "micro do micro: abrir material → fone → 10 min → registrar", "one")}</div>
      <div class="card"><h3>Checkpoints <span class="hint">onde estou · o que apareceu · próxima ação · mudar contexto?</span></h3>
        ${CP.map((c, i) =>
          `<div class="row" style="margin-bottom:6px"><input type="checkbox" data-k="d${d}.cp${i}" ${get(`d${d}.cp${i}`, false) ? "checked" : ""}><span style="width:130px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:600">${c}</span>${ed(`d${d}.cpn${i}`, "", "one")}</div>`
        ).join("")}</div>
      <div class="grid g2">
        <div class="card"><h3>Body</h3><ul class="chk">${BODY.map((b, i) => cb(`d${d}.body${i}`, b)).join("")}</ul></div>
        <div class="card"><h3>Life</h3><ul class="chk">${LIFE.map((b, i) => cb(`d${d}.life${i}`, b)).join("")}</ul></div>
      </div>
     </div>
     <div>
      <div class="card"><h3>Feito hoje <span class="hint">marque o que aconteceu</span></h3><ul class="chk c3">${ROUT.map((b, i) => cb(`d${d}.r${i}`, b)).join("")}<li><input type="checkbox" data-k="d${d}.r11" ${get(`d${d}.r11`, false) ? "checked" : ""}>${ed(`d${d}.r11n`, "outro…", "one")}</li></ul></div>
      <div class="card"><h3>Registro do dia <span class="hint">o quê · quanto tempo · como foi</span></h3>${ed(`d${d}.log`, "07:10 passeio cães 30 min · 08:30 2 blocos relatório · 13:00 leitura cap. 4 · 18:00 treino pernas 45 min…", "big")}</div>
      <div class="card"><h3>Capture it <span class="hint">tudo que pipocar — organizar depois</span></h3>${ed(`d${d}.cap`, "", "mid")}</div>
      <div class="card"><h3>Notas</h3>${ed(`d${d}.notes`, "", "mid")}</div>
     </div>
    </div>`;
};

V.guide = () =>
  H("Guia de uso", "passo a passo · detalhe é o que reduz a fricção") +
  `<div class="guide">
  <h3>1 · Abrir (manhã · 5 min · café)</h3><ol>
  <li>Abra <b>Hoje (D)</b>. Olhe a <b>Semana (W)</b>: quais compromissos e prioridades tocam hoje?</li>
  <li>Escreva o <b>Top 3</b>: três coisas que, feitas, fazem o dia valer — as que puxam as prioridades do mês (M).</li>
  <li>Preencha o <b>Agora</b> com a primeira microação, pequena a ponto de ser quase ridícula. <i>Ex.: "abrir o Anki" em vez de "estudar inglês".</i></li>
  <li>Dia já começou torto? Pule tudo e vá para o <b>Chaos Mode (X)</b>.</li></ol>

  <h3>2 · Executar (ao longo do dia)</h3><ol>
  <li>Trabalhe em blocos (pomodoro 25/5 ou 50/10). Um bloco = uma linha no <b>Registro do dia</b>.</li>
  <li>Terminou algo do Top 3? Marque. Não terminou? Escreva o próximo passo no Agora.</li>
  <li>Pipocou pensamento, ideia, compra, mensagem? <b>Capture it</b>. Não resolva agora; só anote.</li>
  <li>Em cada <b>Checkpoint</b> (manhã · 2 pomodoros · almoço · tarde · fim do trabalho · noite) marque e responda em uma linha: <i>onde estou · o que apareceu · próxima ação · mudo de contexto?</i></li></ol>

  <h3>3 · Fechar (noite · 10 min)</h3><ol>
  <li>Marque o <b>Feito hoje</b>: leitura, treino, estudo, trabalho focado, casa, cachorros, conteúdo, água, sono… Cada quadradinho é um dado para a review.</li>
  <li>Complete o <b>Registro do dia</b> com detalhe: <i>"pomodoro leitura cap. 4 · treino pernas 45 min · passeio cães 30 min · 3 blocos de foco no relatório"</i>. Quanto mais específico, menos você depende de memória.</li>
  <li>Marque Body e Life. Uma frase em <b>Notas</b>: sentimento ou aprendizado do dia.</li>
  <li>Processe o Capture it: vira Top 3 de amanhã, vai para a Semana, para o Backlog (B) — ou apaga.</li>
  <li>Se tiver energia, escreva o Top 3 de amanhã antes de dormir.</li></ol>

  <h3>Domingo · planejar a semana (20 min)</h3><ol>
  <li>Abra <b>Semana (W)</b>. Copie compromissos do Overview (O) e da agenda do celular.</li>
  <li>Escolha 3 prioridades que avançam as prioridades do mês. Se não avança nada do RMM, não é prioridade.</li>
  <li>Preencha Treinos e <b>Accountability</b>: quem espera por você esta semana.</li>
  <li>Processe o Inbox (C). Conte os Feito hoje dos 7 dias (treinos, pomodoros de leitura) e anote no Glow Up (GU).</li></ol>

  <h3>Dia 18 · Route Review (R1) · Dia 25 · Monthly + Body Review (R2, R3) · Dia 27 · RMM de novembro (N)</h3><ul>
  <li><b>R1</b>: Continue / Stop / Start / Change olhando os registros diários — não a memória. Até 2 experimentos até o dia 31.</li>
  <li><b>R2 + R3</b>: some Feito hoje, tracker e KPIs. Nota 1–5 por área. Esboce novembro.</li>
  <li><b>N</b>: leia System Lab (L) e Debug (DB) inteiros. Só agora o planner muda.</li></ul>

  <h3>O que vai onde</h3><ul>
  <li><b>Top 3</b> é intenção · <b>Feito hoje</b> é hábito (marca-se) · <b>Registro</b> é evidência (o quê · quanto tempo · como foi).</li>
  <li><b>Capture it</b> (dia) para o que pipoca · <b>Inbox (C)</b> para o que não pertence a um dia · <b>Notas</b> para reflexões.</li>
  <li>Tem data → <b>Overview</b> e <b>Semana</b> · sem data → <b>Backlog</b> · esta semana → <b>Semana</b>, no dia vira Top 3.</li>
  <li><b>Guindaste (G)</b> é estrutura externa que puxa por semanas · <b>Accountability (A)</b> é pessoa/grupo numa semana específica.</li>
  <li>Algo <i>na vida</i> não aconteceu → <b>Debug</b> · algo <i>no planner</i> não funciona → <b>System Lab</b>. Não altere, registre.</li></ul>

  <h3>Exemplo de um dia</h3>
  <p class="ex">Top 3: fechar relatório X (3 blocos) · treino pernas 18h com Ana · gravar 1 story sobre o livro.<br>Agora: abrir o arquivo e escrever o título da seção 2.<br>Feito hoje: ☑ leitura ☑ treino ☐ estudo ☑ trabalho focado ☑ cachorros ☑ casa ☑ conteúdo ☑ água ☐ sono 7h+<br>Registro: 07:10 passeio cães 30 min · 08:30–10:00 relatório, 2 blocos, seção 2 pronta · 18:00 treino pernas 45 min, agachamento 40 kg · 20:30 story em 1 take · louça · roupa.<br>Notas: blocos de manhã rendem mais; tarde para tarefas leves. Testar amanhã.</p>
  <p class="rule">Regra do mês: <b>usar → observar → registrar.</b> O redesenho é dia 27.</p>
  </div>`;

V.chaos = () =>
  H("Chaos Mode", "quando o dia já começou desorganizado · só isto") +
  `<div class="card"><ul class="chk">${["banheiro / higiene", "água", "cachorros", "alimentação"].map((c, i) => cb(`d${curDay}.chaos${i}`, c, true)).join("")}
   <li class="big"><input type="checkbox" data-k="d${curDay}.chaos4" ${get(`d${curDay}.chaos4`, false) ? "checked" : ""}><span>compromisso principal:</span>${ed(`d${curDay}.chaosmain`, "qual?", "one")}</li></ul></div>` +
  box("Qual é a próxima coisa que evita que o dia desande?", `d${curDay}.chaosnext`, "mid") +
  `<p class="rule">Depois disso, volte para Hoje. Não tente recuperar o dia inteiro — só a próxima coisa.</p>`;

V.capture = () =>
  H("Capture it", "inbox do mês · capturar não significa executar") +
  `<div class="card">${list("capture", "banho · dentes · boleto · ideia · mensagem…")}</div><p class="rule">Organize nos checkpoints: vira Top 3, Backlog, Content ou lixo.</p>`;

V.overview = () => {
  const rows = DAYS.map(d => {
    const n = d.getDate();
    const tag = n === ROUTE ? "Route Review" : n === MREV ? "Monthly Review" : n === RMM ? "RMM" : "";
    return `<tr class="${d.getDay() === 0 ? "sun" : ""}"><td class="d">${pad(n)}<small>${WS[d.getDay()]}</small></td><td>${tag ? `<span class="tag">${tag}</span>` : ""}${ed(`ov.${n}`, "", "one")}</td></tr>`;
  }).join("");

  return H("Monthly Overview", "October 2026 · visão do ciclo inteiro") +
    `<div class="grid g2"><div class="card"><h3>Compromissos do mês</h3><table>${rows}</table></div>
     <div>${["Grandes acontecimentos", "Viagens", "Eventos", "Consultas", "Treinos importantes", "Compromissos sociais", "Prazos"].map((t, i) => box(t, `ovf.${i}`, "one")).join("")}</div></div>`;
};

V.rmm = () =>
  H("October RMM", "reunião mensal · definida em 27 de setembro") +
  `<div class="grid g2">${["O que quero viver?", "O que quero construir?", "O que quero melhorar?", "O que quero experimentar?"].map((q, i) => box(q, `rmm.${i}`, "mid")).join("")}</div>
   <div class="card"><h3>Prioridades do mês <span class="hint">3 a 5, não mais</span></h3>${numbered("prio", 5)}</div>`;

V.kpis = () => {
  const areas = [
    ["Corpo", "treinos · movimento · álcool · peso · medidas · fotos"],
    ["Carreira", "entregas · estudos · networking · AI/Data"],
    ["Idiomas", "inglês · italiano"],
    ["Criação", "conteúdos · artigos · ideias"],
    ["Finanças", "gastos · economia · viagem"]
  ];

  return H("Monthly KPIs", "só os indicadores relevantes a este ciclo") +
    `<div class="card"><table><tr><th>Área</th><th>KPI</th><th>Início</th><th>Meta</th><th>Agora</th></tr>${areas.map((a, r) =>
      `<tr><td style="width:170px"><b style="font-size:11px;letter-spacing:.12em;text-transform:uppercase">${a[0]}</b><div class="mini">${a[1]}</div></td>${[0, 1, 2, 3].map(c =>
        `<td>${ed(`kpi.${r}.${c}`, "", "one")}</td>`
      ).join("")}</tr>`
    ).join("")}</table></div>`;
};

V.backlog = () =>
  H("Monthly Backlog", "quero fazer / viver / resolver · não precisa acontecer tudo este mês") +
  `<div class="grid g2">${[["Fazer", "bl.fazer"], ["Viver", "bl.viver"], ["Ideias", "bl.ideias"], ["Resolver", "bl.resolver"]].map(([t, k]) =>
    `<div class="card"><h3>${t}</h3>${list(k, "")}</div>`
  ).join("")}</div>`;

V.cranes = () =>
  H("Guindastes", "quem ou o quê está me puxando?") +
  `<div class="grid g2 cards">${[0, 1, 2, 3, 4, 5].map(i =>
    `<div class="card">
     <h3>Objetivo</h3>${ed(`cr.${i}.obj`, "", "one")}<h3 style="margin-top:10px">Guindaste</h3>${ed(`cr.${i}.cr`, "pessoa · grupo · competição · evento · aula · prazo · dinheiro", "one")}
     <div class="grid g2" style="margin-top:10px"><div><h3>Data</h3>${ed(`cr.${i}.dt`, "", "one")}</div><div><h3>Pessoa</h3>${ed(`cr.${i}.p`, "", "one")}</div></div>
     <div class="row" style="margin-top:10px"><label class="row" style="gap:6px"><input type="checkbox" data-k="cr.${i}.ok" ${get(`cr.${i}.ok`, false) ? "checked" : ""}> confirmado</label>${ed(`cr.${i}.res`, "resultado", "one")}</div></div>`
  ).join("")}</div>`;

V.acc = () =>
  H("Accountability", "treinos com amigos · videochamada · coworking · stories · GymRats · grupos") +
  `<div class="card"><h3>Treinos com amigos</h3>${table("acc", ["Dia", "Pessoa", "Atividade", "Horário", "✓"], 8)}</div>` +
  box("Outros compromissos de exposição", "acc.other", "mid");

V.glow = () =>
  H("Glow Up", "projeto do mês · tendências, não um número isolado") +
  `<div class="card"><h3>Medidas</h3>${table("gu", ["Quando", "Peso", "Cintura", "Quadril", "Braço", "Coxa", "Bioimp."], 6)}</div>
   <div class="card"><h3>Tracker <span class="hint">clique nos dias: treino / movimento / álcool / água / alimentação</span></h3>
   <table><tr><th></th>${DAYS.map(d => `<th style="padding:2px;text-align:center">${d.getDate()}</th>`).join("")}</tr>
   ${[["Treino", "body3"], ["Movimento", "body2"], ["Água", "body0"], ["Alimentação", "body1"], ["Álcool", "alc"]].map(([l, k]) =>
     `<tr><td style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;white-space:nowrap">${l}</td>${DAYS.map(d =>
       `<td style="padding:4px 2px;text-align:center"><input type="checkbox" style="width:14px;height:14px" data-k="d${d.getDate()}.${k}" ${get(`d${d.getDate()}.${k}`, false) ? "checked" : ""}></td>`
     ).join("")}</tr>`
   ).join("")}</table></div>
   <div class="grid g2">${box("Fotos · quando / onde", "gu.photos", "mid")}${box("Como estou me sentindo / tendência", "gu.feel", "mid")}</div>`;

V.content = () =>
  H("Content Backlog", "ideia → capturar → criar depois · se precisar gravar agora: câmera → grava → fecha → volta") +
  `<div class="grid g2 cards">${[0, 1, 2, 3, 4, 5, 6, 7].map(i =>
    `<div class="card"><div class="grid g2"><div><h3>Tema</h3>${ed(`ct.${i}.t`, "", "one")}</div><div><h3>Formato · Plataforma</h3>${ed(`ct.${i}.f`, "reels · story · carrossel · artigo", "one")}</div></div>
     <h3 style="margin-top:10px">Ideia</h3>${ed(`ct.${i}.i`, "", "one")}<ul class="chk c3" style="margin-top:10px">${["capturada", "roteiro", "gravar", "editar", "publicar"].map((s, j) => cb(`ct.${i}.s${j}`, s)).join("")}</ul></div>`
  ).join("")}</div>`;

V.week = () => {
  const w = curWeek, days = WEEKS[w - 1];
  const nav = `<div class="daynav">${WEEKS.map((_, i) =>
    `<button data-week="${i + 1}" class="${i + 1 === w ? "on" : ""}" style="width:auto;padding:0 12px">Semana ${i + 1}</button>`
  ).join("")}</div>`;

  return H(`Semana ${w}`, `${pad(days[0])}–${pad(days[days.length - 1])} out`) + nav +
    `<div class="grid g2"><div>
     <div class="card"><h3>Prioridades</h3>${numbered(`w${w}.prio`, 3)}</div>
     <div class="card"><h3>Compromissos</h3><table>${days.map(n =>
       `<tr class="${DAYS[n - 1].getDay() === 0 ? "sun" : ""}"><td class="d">${pad(n)}<small>${WS[DAYS[n - 1].getDay()]}</small></td><td>${ed(`ov.${n}`, "", "one")}</td></tr>`
     ).join("")}</table><p class="mini">Mesmo campo do Overview mensal.</p></div>
     ${box("Treinos", `w${w}.tr`, "mid")}</div>
     <div><div class="card"><h3>Accountability <span class="hint">quem espera por mim esta semana</span></h3>${table(`w${w}.acc`, ["Dia", "Pessoa", "O quê", "✓"], 4)}</div>
     ${box("Notas + Captura", `w${w}.notes`, "big")}</div></div>`;
};

V.debug = () => {
  const n = get("debug.count", 3);

  return H("Debug my life", "quando algo não acontecer · sem culpa, só diagnóstico") +
    [...Array(n)].map((_, i) =>
      `<div class="card"><div class="grid g2">${box("O que eu queria fazer?", `db.${i}.want`, "one")}${box("O que aconteceu? Onde quebrou?", `db.${i}.what`, "one")}</div>
       <h3>Qual foi a fricção?</h3><ul class="chk c2" style="margin-bottom:14px">${["faltou clareza", "tarefa grande demais", "faltou guindaste", "ambiente atrapalhou", "Instagram capturou", "cansada / faminta", "trabalho ocupou o espaço", "outra demanda venceu"].map((f, j) => cb(`db.${i}.f${j}`, f)).join("")}</ul>
       ${box("Qual experimento vou testar?", `db.${i}.exp`, "one")}</div>`
    ).join("") +
    `<button class="btn" id="moredebug">+ novo debug</button>`;
};

V.lab = () =>
  H("System Lab", "October feedback → November v2 · registre, não implemente") +
  `<div class="card"><p class="rule" style="margin-top:0">Não funcionou · faltou · sobrou · página inútil · página apertada · difícil de achar · nova métrica · mudança de fluxo.</p>${list("lab", "\u201Cseria melhor se\u2026\u201D")}</div>`;

V.route = () =>
  H("Route Review", `${pad(ROUTE)} out · penúltimo domingo · reflexão + reorganização de rota`) +
  `<div class="grid g2">${[["Continue · o que funcionou?", "rr.c"], ["Stop · o que não funcionou?", "rr.s"], ["Start · o que quero começar?", "rr.st"], ["Change · o que precisa mudar?", "rr.ch"], ["Biggest bottleneck", "rr.bb"], ["Biggest win", "rr.bw"], ["O que está consumindo minha atenção?", "rr.att"], ["O que está me dando energia?", "rr.en"]].map(([t, k]) => box(t, k, "mid")).join("")}</div>${box("Quais experimentos testo até o dia 31?", "rr.exp", "mid")}`;

V.monthly = () =>
  H("Monthly Review", `${pad(MREV)} out · último domingo · resultados do ciclo`) +
  `<div class="card"><table><tr><th>Área</th><th>Resultado / métrica</th><th>Nota 1–5</th></tr>${["Corpo / treinos", "Carreira", "Idiomas", "Conteúdo", "Finanças", "Experiências", "Relações", "Hábitos"].map((a, i) =>
    `<tr><td style="width:180px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;padding-top:12px">${a}</td><td>${ed(`mr.${i}.r`, "", "one")}</td><td style="width:90px">${ed(`mr.${i}.n`, "", "one")}</td></tr>`
  ).join("")}</table></div>` +
  box("O que este mês me ensinou?", "mr.learn", "mid") +
  `<h1 style="font-size:28px;margin-top:30px">Next month</h1><p class="sub">November — Expansion Sprint 02 · esboço</p><div class="grid g3">${["Prioridades", "KPIs", "Guindastes", "Compromissos", "Experimentos", "Sprints"].map((t, i) => box(t, `nm.${i}`, "mid")).join("")}</div>`;

V.body = () =>
  H("Body Review", "final do mês · tendências") +
  `<div class="grid g2">${["O que mudou?", "Como estou me sentindo?", "Como está minha força?", "Como estão minhas roupas?", "O que mostram as medidas?", "O que mostram as fotos?", "O que mostram as métricas?", "O que quero testar no próximo ciclo?"].map((q, i) => box(q, `br.${i}`, "mid")).join("")}</div>`;

V.nov = () =>
  H("November RMM", "Expansion Sprint 02 · dia 27 de outubro · entrada: System Lab + Monthly Review") +
  `<div class="grid g2">${["O que quero viver?", "O que quero construir?", "O que quero melhorar?", "O que quero experimentar?"].map((q, i) => box(q, `nov.rmm.${i}`, "mid")).join("")}</div><div class="card"><h3>3–5 prioridades</h3>${numbered("nov.prio", 5)}</div>
   <div class="card"><h3>Lab → v2 <span class="hint">itens registrados no System Lab</span></h3>${get("lab", []).length
     ? `<ul>${get("lab", []).map(x => `<li>${esc(x)}</li>`).join("")}</ul>`
     : `<p class="rule">Nada registrado ainda.</p>`}</div>`;

// ------------------------------------------------------------------ render & events

const main = document.getElementById("main");

function render() {
  main.innerHTML = V[view]();
  document.querySelectorAll("nav button[data-v]").forEach(b =>
    b.classList.toggle("on", b.dataset.v === view)
  );
  location.hash = view;
  window.scrollTo(0, 0);
  const nb = document.querySelector(`nav button[data-v="${view}"]`);
  document.getElementById("tb-code").textContent = nb ? nb.textContent.trim() : "";
}

document.querySelectorAll("nav button[data-v]").forEach(b =>
  b.onclick = () => {
    view = b.dataset.v;
    document.body.classList.remove("menu");
    render();
  }
);

document.getElementById("ham").onclick = () =>
  document.body.classList.toggle("menu");

document.getElementById("scrim").onclick = () =>
  document.body.classList.remove("menu");

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js");

main.addEventListener("input", e => {
  const t = e.target;
  if (t.dataset.k !== undefined && t.classList.contains("ed"))
    set(t.dataset.k, t.innerText);
  if (t.dataset.listK) {
    const a = get(t.dataset.listK, []);
    a[+t.dataset.i] = t.innerText;
    set(t.dataset.listK, a);
  }
});

main.addEventListener("change", e => {
  const t = e.target;
  if (t.type === "checkbox" && t.dataset.k) {
    set(t.dataset.k, t.checked);
    if (view === "dash") render();
  }
});

main.addEventListener("click", e => {
  const t = e.target.closest("button");
  if (!t) return;
  if (t.dataset.day) { curDay = +t.dataset.day; render(); }
  if (t.dataset.week) { curWeek = +t.dataset.week; render(); }
  if (t.dataset.add) {
    const a = get(t.dataset.add, []);
    a.push("");
    set(t.dataset.add, a);
    render();
    const eds = main.querySelectorAll(`[data-list-k="${t.dataset.add}"]`);
    eds[eds.length - 1]?.focus();
  }
  if (t.dataset.del) {
    const a = get(t.dataset.del, []);
    a.splice(+t.dataset.i, 1);
    set(t.dataset.del, a);
    render();
  }
  if (t.id === "moredebug") {
    set("debug.count", get("debug.count", 3) + 1);
    render();
  }
});

document.getElementById("exp").onclick = () => {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(S, null, 1)], { type: "application/json" }));
  a.download = `planner-oct-2026-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
};

document.getElementById("imp").onchange = e => {
  const f = e.target.files[0];
  if (!f) return;
  f.text().then(t => {
    S = JSON.parse(t);
    save();
    render();
  });
};

render();
