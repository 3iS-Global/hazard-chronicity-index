"""Re-style a dashboard HTML (Leaflet + Chart.js, embedded DATA) with the UN visual identity.

Applies the UN colour ramp to every class palette, Roboto typography, logos in the header, the
"Elaborado por 3iS" credit line, rewrites the index names to HCI, fixes the distribution chart bars
(visible outline + value labels) and the main-map fit so the whole mainland (including Pastaza,
Orellana and Sucumbios) is visible.

Usage: python scripts/products/apply_un_branding_dashboard.py <source.html> <output.html>
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # repository root
import re,json,base64,sys
# Input and output HTML paths
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf-8-sig').read()
# Embed an image as a base64 data URI
def b64(p): return 'data:image/png;base64,'+base64.b64encode(open(str(ROOT/'assets'/'branding'/p),'rb').read()).decode()
UN,IS,EU=b64('un_emblem_blue.png'),b64('3is_logo_color.png'),b64('eu_funded_ha_es_1200.png')
# fonts
# Switch the typeface to Roboto
t=t.replace('family=Montserrat:wght@400;500;600;700;800','family=Roboto:wght@400;500;700')
t=t.replace("'Montserrat', sans-serif","'Roboto', Arial, sans-serif").replace("'Montserrat',Arial,sans-serif","'Roboto',Arial,sans-serif")
# palette vars
# Replace the colour variables with the UN palette
a=t.index(':root {'); b=t.index('}',a)
t=t[:a]+""":root {
    --navy: #002E6E; --teal-deep: #004987; --cyan: #0074B7; --aqua: #009EDB; --teal: #009EDB;
    --gray: #D9D9D9; --aqua-tint: #E3EDF6; --peach: #C5DFEF; --coral: #F58220; --mustard: #FFC800;
    --radius: 4px; --bg: #F4F6F8; --card: #ffffff; --border: #D0D7DE; --text: #000000; --muted: #4D5560;
    --font: 'Roboto', Arial, sans-serif;
  """+t[b:]
# header
# Replace the header with the UN / EU logo header
ha=t.index('<header>'); hb=t.index('</header>')+9
hdr=f'''<header>
  <div class="header-row">
    <div class="logos"><img class="un" src="{UN}" alt="Naciones Unidas"></div>
    <div class="titles">
      <h1>Índices de cronicidad de amenazas asociadas a El Niño — Ecuador, 2015–2025</h1>
      <p>Índice de Cronicidad de Amenazas (HCI): inundación, aluvión, deslizamiento, socavamiento y combinado</p>
    </div>
    <div class="header-right"><button id="btnInfo" onclick="document.getElementById('modalOverlay').classList.add('open')" title="Metodología">ⓘ Acerca de</button>
    <img class="eu" src="{EU}" alt="Financiado por la Unión Europea — Ayuda Humanitaria"></div>
  </div>
</header>'''
t=t[:ha]+hdr+t[hb:]
css_h=re.search(r'  header \{.*?\.brand-divider \{[^\n]*\n',t,re.S).group(0)
newcss='''  header { background:#fff; padding:.8rem 1.75rem; border-bottom:4px solid #009EDB; }
  header .header-row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px; }
  header .logos { display:flex; align-items:center; gap:18px; }
  header img.un { height:54px; } header img.is { height:34px; } header img.eu { height:44px; }
  header .titles { flex:1; min-width:280px; text-align:left; }
  header .titles h1 { margin:0; font-size:19px; font-weight:700; color:#000; }
  header .titles p { margin:4px 0 0; font-size:12.5px; color:#4D5560; }
  header .header-right { display:flex; align-items:center; gap:16px; }
  .brand-divider { display:none; }
'''
t=t.replace(css_h,newcss)
t=re.sub(r'#btnInfo \{.*?\}\n  #btnInfo:hover \{[^}]*\}',
 "#btnInfo { background:#009EDB; border:0; color:#000; border-radius:4px; padding:8px 16px; font-size:12.5px; font-weight:700; cursor:pointer; font-family:var(--font); white-space:nowrap; }\n  #btnInfo:hover { background:#64BDEA; }",t,flags=re.S)
# remove shadows/rounded pills
t=t.replace('border-radius: 999px','border-radius: 4px')
t=t.replace('box-shadow: 0 1px 3px rgba(0,0,0,0.06)','box-shadow:none').replace('box-shadow: 0 2px 6px rgba(0,0,0,0.18)','box-shadow:none').replace('box-shadow: 0 2px 6px rgba(0,0,0,0.25)','box-shadow:none')
t=t.replace('.pill { ','.pill { color:#004987;').replace('.pill.active-alt { background: var(--teal); border-color: var(--teal); color: var(--navy)','.pill.active-alt { background: #009EDB; border-color: #009EDB; color: #000')
t=t.replace('.pill:hover { background: var(--aqua-tint); }','.pill:hover { background: var(--aqua-tint); }\n  .control-label{color:#002E6E;text-transform:none;letter-spacing:0;font-size:12px}')
# aviso
t=t.replace('background:#FFF6E5;\n border-bottom:3px solid #F4B942','background:#E3EDF6;\n border-bottom:3px solid #009EDB')
t=t.replace('#aviso-metodologico th{background:#063B6D','#aviso-metodologico th{background:#002E6E').replace('color:#063B6D;font-size:13px','color:#002E6E;font-size:13px').replace('border-bottom:1px solid #e0d6c0','border-bottom:1px solid #C5DFEF').replace('.am-nota{font-size:11px;color:#667580','.am-nota{font-size:11px;color:#4D5560')
# footnote + modal footer
# Credit line: Elaborado por 3iS
t=t.replace('<p class="footnote">3iS · 2026</p>',f'<p class="footnote">Fuente: reportes SNGRE/ECU911, 2015–2025. Elaborado por 3iS · © 2026</p>')
fa=t.index('<div class="modal-footer">'); fb=t.index('</div>\n  </div>\n</div>',fa)
t=t[:fa]+f'<div class="modal-footer"><img src="{EU}" alt="UE" style="height:40px;margin-bottom:6px"><div class="name" style="font-style:normal">Elaborado por 3iS · © 2026</div>\n    '+t[fb:]
# naming EFCI -> HCI
# Rename the index to HCI (Hazard Chronicity Index)
t=t.replace('<b>EFCI (ENSO Flood/Hazard Chronicity Index)</b>','<b>HCI (Índice de Cronicidad de Amenazas)</b>')
t=t.replace('<b>EFCI</b> (Inundación),\n    <b>EACI</b> (Aluvión), <b>ELCI</b> (Deslizamiento), <b>ESCI</b> (Socavamiento) y <b>EHCI</b>','<b>HCI de inundación</b>,\n    <b>HCI de aluvión</b>, <b>HCI de deslizamiento</b>, <b>HCI de socavamiento</b> y <b>HCI combinado</b>')
t=t.replace('EFCI =','HCI =').replace('Cronicidad (EFCI)','Cronicidad (HCI)').replace('del EFCI','del HCI').replace('En el EFCI','En el HCI').replace('cronicidad EFCI','cronicidad HCI').replace('fuera del EFCI','fuera del HCI')
t=t.replace('{ TODOS: "EHCI", flood: "EFCI", debris_flow: "EACI", landslide: "ELCI", scour: "ESCI" }','{ TODOS: "HCI", flood: "HCI", debris_flow: "HCI", landslide: "HCI", scour: "HCI" }')
t=re.sub(r' — ver <i>docs/[^<]*</i>','',t); t=re.sub(r'\(<i>docs/[^<]*</i>\)|<i>docs/[^<]*</i>','',t)
t=t.replace('docs/methodology/13_sensitivity_validation.md','')
# colours JS
# Map old hex colours to UN-brand colours
rep={'#063B6D':'#002E6E','#135879':'#0074B7','#F4B942':'#FFC800','#207685':'#009EDB','#FD956F':'#F58220','#4CDBB0':'#72BF44','#eef1f3':'#E3EDF6','rgba(32,118,133,0.55)':'rgba(0,158,219,0.55)','rgba(6,59,109,0.12)':'rgba(0,46,110,0.12)','#667580':'#4D5560','#26343d':'#000000','#33424f':'#4D5560','#eaf2f6':'#FFFFFF'}
for k,v in rep.items(): t=t.replace(k,v)
t=t.replace('weight: 0.6, color: "#ffffff", fillOpacity: 0.88','weight: 0.6, color: "#7F93A6", fillOpacity: 1')
t=t.replace('if (!cell) return "#cccccc"','if (!cell) return "#F2F2F2"')
# dist chart: visible bars w/ outline + labels
# Distribution chart: visible outline on every bar so the lightest class never disappears
t=t.replace('backgroundColor: meta.colors.slice(0, nClasses), borderRadius: 3, maxBarThickness: 34 }]','backgroundColor: meta.colors.slice(0, nClasses), borderColor: "#002E6E", borderWidth: 1.5, borderSkipped: false, maxBarThickness: 34 }]')
t=t.replace('''  chartDist = new Chart(ctx, {
    type: "bar",''','''  chartDist = new Chart(ctx, {
    type: "bar",
    plugins: [{ id: "valLbl", afterDatasetsDraw(ch) { const c = ch.ctx; c.save(); c.fillStyle = "#000"; c.font = "500 11px Roboto, Arial"; c.textAlign = "center"; ch.getDatasetMeta(0).data.forEach((b, i) => { c.fillText(String(ch.data.datasets[0].data[i]), b.x, b.y - 4); }); c.restore(); } }],''')
t=t.replace('y: { ticks: { font: { size: 10 }, precision: 0 }, grid: { color: "#E3EDF6" } }\n      }\n    }\n  });\n  captionEl','y: { beginAtZero: true, grace: "12%", ticks: { font: { size: 10 }, precision: 0 }, grid: { color: "#E3EDF6" } }\n      }\n    }\n  });\n  captionEl')
t=t.replace('"Distribución por Clase — "','"Distribución de cantones por clase — "')
# map fit
# Fit the mainland map without panning so the east is not cropped
a=t.index('function fitMainMap()'); b=t.index('mapGala.invalidateSize();',a)
t=t[:a]+'''function fitMainMap() {
  mapMain.invalidateSize();
  mapMain.fitBounds(layerMain.getBounds(), { paddingTopLeft: [150, 4], paddingBottomRight: [4, 4] });
}

'''+t[b:]
t=t.replace('const mapMain = L.map("mapMain", { zoomControl: false,','const mapMain = L.map("mapMain", { zoomSnap: 0.1, zoomControl: false,')
t=t.replace('position: absolute; top: 12px; left: 12px; z-index: 480;','position: absolute; top: 12px; left: 12px; z-index: 480;')
t=t.replace('.map-shell { position: relative; max-width: 860px; }','.map-shell { position: relative; max-width: 960px; }')
# palettes in DATA
m=re.search(r'const DATA = (\{.*\});\n',t); d=json.loads(m.group(1))
# Sequential UN ramp
RAMP=['#E3EDF6','#99CCEA','#009EDB','#0067A3','#002E6E']
# Diverging hotspot palette
HOT=['#9B1235','#ED1847','#F59AAE','#EDEFF2','#99CCEA','#0074B7','#002E6E']
# Apply the palettes to every indicator
for k,v in d['indicadores_meta'].items():
    for h,mm in v.items():
        mm['colors']=HOT if k=='hotspots' else RAMP[:len(mm['colors'])]
t=t[:m.start(1)]+json.dumps(d,ensure_ascii=False)+t[m.end(1):]
t=t.replace('Hotspots (Getis-Ord Gi*)','Hotspots (Getis-Ord Gi*)')
# Write the restyled dashboard
open(dst,'w',encoding='utf-8').write(t)
for pat in ['Jerson','jachicanoy','EFCI','EACI','ELCI','ESCI','EHCI','Montserrat','docs/','#063B6D','#ffffff1c']: print(pat,t.count(pat))
