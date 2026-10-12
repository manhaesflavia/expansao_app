from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
petals = "".join(f'<ellipse cx="50" cy="18" rx="4.4" ry="14.5" transform="rotate({360*k/14:.3f} 50 50)"/>' for k in range(14))
def sf(stroke, center, sw=1.4):
    return (f'<svg viewBox="0 0 100 100" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round">{petals}'
            f'<circle cx="50" cy="50" r="15" stroke="{center}"/><circle cx="50" cy="50" r="9" stroke="{center}" stroke-dasharray="1.5 2"/></svg>')

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--ink:#1F2B3C;--ink2:#6B7480;--acc:#D9A63A;--yel:#F3D77B;--soft:#E4E7EB}
*{box-sizing:border-box}body{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:Inter,sans-serif;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
.st{position:relative;width:1080px;height:1920px;padding:150px 90px 130px;display:flex;flex-direction:column}
.k{font-size:26px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc);font-weight:600}
h1{font-family:"Cormorant Garamond",serif;font-weight:500;font-size:112px;line-height:1;margin:34px 0 40px;letter-spacing:-.01em}
h1 em{font-style:italic;color:var(--acc)}
p{font-size:36px;line-height:1.45;color:var(--ink2);margin:0}
.sf{position:absolute;width:520px;height:520px}
.brand{position:absolute;left:90px;bottom:120px;display:flex;align-items:center;gap:22px;font-family:"Cormorant Garamond",serif;font-size:54px}
.brand svg{width:70px;height:70px}
.url{position:absolute;right:90px;bottom:135px;font-size:26px;letter-spacing:.06em;color:var(--ink2)}
.dark{background:var(--ink);color:#fff}.dark p{color:#B8C0CC}.dark .url{color:#B8C0CC}.dark h1 em{color:var(--yel)}.dark .k{color:var(--yel)}
.yel{background:var(--yel)}.yel p{color:#4B5563}.yel .k{color:var(--ink)}.yel h1 em{color:#fff}
.li{display:flex;gap:26px;align-items:flex-start;padding:22px 0;border-bottom:1px solid rgba(255,255,255,.14);font-size:32px;line-height:1.35}
.li b{font-family:"Cormorant Garamond",serif;font-size:46px;color:var(--yel);font-weight:500;min-width:190px;line-height:1.1}
.li:last-child{border:0}
.phone{position:absolute;left:50%;transform:translateX(-50%);bottom:-380px;width:720px;border:22px solid var(--ink);border-radius:80px;overflow:hidden;background:#fff;box-shadow:0 60px 120px rgba(31,43,60,.25)}
.phone img{display:block;width:100%}
.tag{display:inline-block;padding:14px 26px;border:2px solid var(--ink);border-radius:999px;font-size:26px;letter-spacing:.08em;margin-top:40px}
</style>"""

S1 = f"""{CSS}<div class="st yel">
<div class="sf" style="right:-140px;top:-120px;opacity:.9">{sf('#1F2B3C','#1F2B3C',1.1)}</div>
<div class="k">Sistema operacional pessoal</div>
<h1>Um planner<br>para quem<br>funciona por<br><em>urgência.</em></h1>
<p>Interesse, novidade, prazo. Se é assim que você liga, a agenda comum não foi feita para você.</p>
<div class="phone" style="bottom:-480px"><img src="file://{ROOT}/app/shot-today.png"></div>
</div>"""

S2 = f"""{CSS}<div class="st dark">
<div class="sf" style="right:-160px;bottom:-160px;opacity:.35">{sf('#D9A63A','#fff',1)}</div>
<div class="k">Desenhado a partir do TDAH adulto</div>
<h1>Menos força<br>de vontade.<br><em>Mais estrutura.</em></h1>
<p style="margin-bottom:60px">A atenção costuma estar lá. O que falha é a autorregulação — e o planner externaliza cada parte dela:</p>
<div class="li"><b>Começar</b><span>uma microação só — o passo que não dá pra procrastinar</span></div>
<div class="li"><b>Manter</b><span>6 checkpoints no dia pra voltar ao trilho, sem culpa</span></div>
<div class="li"><b>Lembrar</b><span>Capture It em toda página — zero confiança na memória</span></div>
<div class="li"><b>Parar</b><span>hora de sair do hiperfoco — anota onde parou e fecha</span></div>
<div class="li"><b>Voltar</b><span>Chaos Mode: 3 perguntas, 1 ação mínima, reset</span></div>
<div class="li"><b>Ajustar</b><span>todo mês: usar → observar → registrar → melhorar</span></div>
<div class="brand">{sf('#D9A63A','#fff',2.2)}Expansão</div>
</div>"""

S3 = f"""{CSS}<div class="st">
<div class="sf" style="right:-220px;top:-170px;opacity:.5">{sf('#D9A63A','#1F2B3C',.9)}</div>
<div class="k">Memória externa + captura + organização + execução + feedback</div>
<h1>Abri.<br>Sei onde estou.<br>Sei onde escrever.<br><em>Sei o que fazer.</em></h1>
<p>Papel A5 para regular, app para estar sempre à mão. 2 páginas por dia, 6 checkpoints, captura em toda página, review mensal. Um método só.</p>
<div style="display:flex;gap:26px;margin-top:70px">
<img src="file://{ROOT}/app/pg-cover.png" style="width:270px;border:1px solid var(--soft);box-shadow:0 30px 60px rgba(31,43,60,.12)">
<img src="file://{ROOT}/app/pg-day.png" style="width:270px;border:1px solid var(--soft);box-shadow:0 30px 60px rgba(31,43,60,.12)">
<img src="file://{ROOT}/app/pg-day2.png" style="width:270px;border:1px solid var(--soft);box-shadow:0 30px 60px rgba(31,43,60,.12)">
</div>
<div class="brand">{sf('#D9A63A','#1F2B3C',2.2)}Expansão</div>
<div class="url">link na bio ↗</div>
</div>"""

OG = f"""{CSS}<style>body{{width:1200px;height:630px}}.st{{width:1200px;height:630px;padding:70px 80px}}h1{{font-size:78px;margin:20px 0 24px}}p{{font-size:28px}}</style>
<div class="st">
<div class="sf" style="right:-90px;top:-110px;width:460px;height:460px;opacity:.9">{sf('#D9A63A','#1F2B3C',1.1)}</div>
<div class="k">Sistema operacional pessoal</div>
<h1>Um planner para quem funciona<br>por <em>interesse, urgência e novidade</em>.</h1>
<p style="max-width:720px">Memória externa + captura + organização + execução + feedback.<br>Papel A5 + app. Desenhado a partir do TDAH adulto.</p>
<div class="brand" style="bottom:60px;font-size:44px">{sf('#D9A63A','#1F2B3C',2.2)}Expansão</div>
</div>"""

out = ROOT / "dist/stories"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, vp in (("story-1-capa", S1, (1080, 1920)), ("story-2-tdah", S2, (1080, 1920)),
                           ("story-3-sistema", S3, (1080, 1920)), ("og", OG, (1200, 630))):
        pg = b.new_page(viewport={"width": vp[0], "height": vp[1]}, device_scale_factor=1 if name == "og" else 1)
        (ROOT/"prev/_st.html").write_text(html); pg.goto((ROOT/"prev/_st.html").as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        dest = ROOT / ("app/og.png" if name == "og" else f"dist/stories/{name}.png")
        pg.screenshot(path=str(dest)); print(dest); pg.close()
    b.close()
