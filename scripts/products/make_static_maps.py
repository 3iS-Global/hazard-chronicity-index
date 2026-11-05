"""Render the 60 static choropleth maps (12 indicators x 5 hazard views) at 300 dpi.

The canton classes, breaks and labels are read from the dashboard data embedded in index.html, so
static maps and dashboard always agree. Layout: Galapagos inset on the left, mainland on the right,
legend below the inset, source note and logos in the footer.

Usage: python scripts/products/make_static_maps.py [indicator_hazard ...]
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # repository root
import re,json,sys
import geopandas as gpd, matplotlib
# Headless backend: no display needed
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from PIL import Image
import numpy as np
R=str(ROOT)+'/'
for f in fm.findSystemFonts(fontpaths=['/sessions/brave-dreamy-fermat/.fonts']): fm.fontManager.addfont(f)
# Use Roboto, the UN typeface
plt.rcParams['font.family']='Roboto'
# Read the dashboard HTML, which embeds the canton data
t=open(R+'index.html',encoding='utf-8-sig').read()
# Parse the JSON value assigned to a JavaScript constant
def jv(n):
    i=t.index('const '+n+' = ')+len('const '+n+' = ')
    return json.JSONDecoder().raw_decode(t[i:])[0]
# Class values, breaks and labels per indicator and hazard; plus canton and province geometries
D=jv('DATA'); cant=gpd.GeoDataFrame.from_features(jv('CANTONES')['features'],crs=4326)
prov=gpd.GeoDataFrame.from_features(jv('PROVINCIAS')['features'],crs=4326)
# Galapagos cantons are drawn in the inset
GAL={"San Cristóbal","Isabela","Santa Cruz"}
# Split mainland and Galapagos cantons
isg=cant.canton_name_official.isin(GAL); main=cant[~isg]; gal=cant[isg]
pg=prov.province_name_official=='Galápagos'; pmain=prov[~pg]; pgal=prov[pg]
# UN blue sequential ramp (light to dark), 5 classes
RAMP=['#E3EDF6','#99CCEA','#009EDB','#0067A3','#002E6E']
# Diverging palette for Gi* hotspots: UN red = hot, UN blue = cold
HOT=['#9B1235','#ED1847','#F59AAE','#EDEFF2','#99CCEA','#0074B7','#002E6E']
# Hazard views: key -> (slug, label)
HAZ={'TODOS':('combinado','amenazas combinadas'),'flood':('inundaciones','inundaciones'),'debris_flow':('aluviones','aluviones'),'landslide':('deslizamientos','deslizamientos'),'scour':('socavamientos','socavamientos')}
# Indicators: key -> (number, slug, title, unit)
IND={ # key:(num, slug, title, unit)
'frecuencia':('01','frecuencia_eventos','Frecuencia de eventos','Número de eventos, 2015–2025'),
'severidad':('02','severidad','Índice de severidad','Índice normalizado (0–1)'),
'frecuencia_enso':('03','frecuencia_enso','Frecuencia de eventos en meses El Niño','Meses con al menos un evento durante El Niño'),
'poblacion':('04','poblacion_afectada','Población afectada','Máximo histórico, personas afectadas directa e indirectamente'),
'agricultura':('05','perdidas_agricolas','Pérdidas agrícolas','Máximo histórico, hectáreas afectadas y destruidas'),
'vivienda':('06','perdidas_vivienda','Pérdidas de vivienda','Máximo histórico, viviendas afectadas y destruidas'),
'efci':('07','hci_cronicidad','Cronicidad (HCI)','Clases del Índice de Cronicidad de Amenazas'),
'hotspots':('08','hotspots_gi_star','Hotspots de cronicidad (Getis-Ord Gi*)','Significancia estadística del clúster espacial'),
'educacion':('09','educacion_afectada','Establecimientos educativos afectados','Máximo histórico, afectados y destruidos'),
'salud':('10','salud_afectada','Centros de salud afectados','Máximo histórico, afectados y destruidos'),
'vias':('11','vias_afectadas','Vías afectadas','Máximo histórico, metros lineales'),
'puentes':('12','puentes_afectados','Puentes afectados','Máximo histórico, afectados y destruidos')}
# Format a class break with the number format of the indicator
def fv(v,f):
    return f"{v:,.0f}" if f=='0,0' else (f"{v:.3f}" if f=='.3f' else (f"{v:.2f}" if f=='.2f' else f"{v:,.0f}"))
# Logos used in the header and footer
UN=Image.open(R+'assets/branding/un_emblem_blue.png').convert('RGBA'); EU=Image.open(R+'assets/branding/eu_funded_ha_es_1200.png').convert('RGBA'); IS=Image.open(R+'assets/branding/3is_logo_color.png').convert('RGBA')
# Draw one map and save it as PNG
def draw(ind,hz,out):
    num,slug,title,unit=IND[ind]; meta=D['indicadores_meta'][ind][hz]; layer=D['hazards'][hz][ind]
    cols=HOT if ind=='hotspots' else RAMP[:len(meta['colors'])]
    if meta.get('categorical'): labels=meta['labels']
    else:
        br=meta['breaks']; labels=[ (fv(0 if i==0 else br[i-1],meta['fmt'])+' – '+fv(b,meta['fmt'])) for i,b in enumerate(br)]
    # Figure size in inches (landscape)
    W,H=13.0,7.6
    fig=plt.figure(figsize=(W,H),dpi=150,facecolor='white')
    fig.text(0.03,0.965,f"{title}: {HAZ[hz][1]}",fontsize=17,fontweight='bold',color='#000',ha='left',va='top')
    fig.text(0.03,0.915,f"{unit}. Cantones de Ecuador, 2015–2025",fontsize=11,color='#4D5560',ha='left',va='top')
    # Mainland axes
    ax=fig.add_axes([0.30,0.125,0.52,0.76]); ax.set_aspect('equal'); ax.axis('off')
    cl=main.canton_code.map(lambda c: layer.get(c,{}).get('c'))
    # Fill colour of each canton from its class (light grey when there is no data)
    fc=[('#F2F2F2' if c is None or c!=c else cols[min(int(c),len(cols)-1)]) for c in cl]
    main.plot(ax=ax,color=fc,edgecolor='#7F93A6',linewidth=0.25)
    # Province outlines on top
    pmain.boundary.plot(ax=ax,color='#1A1A1A',linewidth=0.6)
    # Extent that includes the whole Amazon region (Pastaza, Orellana, Sucumbios)
    ax.set_xlim(-81.3,-74.9); ax.set_ylim(-5.2,1.6)
    # Galapagos inset on the left
    ia=fig.add_axes([0.03,0.52,0.20,0.34]); ia.set_aspect('equal'); ia.set_xticks([]); ia.set_yticks([]); ia.set_facecolor('white'); [sp.set_edgecolor('#999999') for sp in ia.spines.values()]; ia.set_title('Galápagos',fontsize=10,fontweight='bold',loc='left',pad=4)
    cg=gal.canton_code.map(lambda c: layer.get(c,{}).get('c'))
    gal.plot(ax=ia,color=[('#F2F2F2' if c is None or c!=c else cols[min(int(c),len(cols)-1)]) for c in cg],edgecolor='#1A1A1A',linewidth=0.5)
    # Legend below the inset
    ly=0.40; lx=0.03
    fig.text(lx,ly+0.012,'Clases',fontsize=10,fontweight='bold',ha='left',va='bottom')
    for i,(c,l) in enumerate(zip(cols,labels)):
        y=ly-0.036*i
        fig.patches.append(Rectangle((lx,y-0.027),0.016,0.028,transform=fig.transFigure,facecolor=c,edgecolor='#4D5560',linewidth=0.6))
        fig.text(lx+0.022,y-0.013,l,fontsize=9.5,ha='left',va='center')
    fig.text(lx,ly-0.036*len(cols)-0.005,'Sin dato: gris claro',fontsize=8,color='#4D5560',ha='left',va='top')
    # UN-blue rule above the footer
    fig.patches.append(Rectangle((0,0.105),1,0.002,transform=fig.transFigure,facecolor='#009EDB',edgecolor='none'))
    fig.text(0.03,0.092,'Fuente: reportes SNGRE/ECU911 (2015–2025); límites administrativos. '+('' if meta.get('categorical') else 'Clases por rupturas naturales (Jenks). ')+'Elaborado por 3iS · © 2026',fontsize=8,color='#4D5560',ha='left',va='top')
    fig.text(0.03,0.068,'Las denominaciones y los límites no implican reconocimiento ni aceptación oficial por parte de las Naciones Unidas.',fontsize=7.5,color='#4D5560',ha='left',va='top')
    h=0.075; h=0.115; a_=fig.add_axes([0.97-h*UN.width/UN.height*H/W,0.86,h*UN.width/UN.height*H/W,h]); 
    a_.imshow(UN); a_.axis('off')
    h=0.06; a=fig.add_axes([0.97-h*EU.width/EU.height*H/W,0.012,h*EU.width/EU.height*H/W,h]); a.imshow(EU); a.axis('off')
    # Save at 300 dpi
    fig.savefig(out,dpi=300); plt.close(fig)
# Render every indicator for every hazard view (or only those passed on the command line)
if __name__=='__main__':
    import os
    os.makedirs(R+'outputs/maps',exist_ok=True)
    sel=sys.argv[1:]
    for hz in HAZ:
        for ind in IND:
            if sel and f"{ind}_{hz}" not in sel: continue
            draw(ind,hz,R+f"outputs/maps/{IND[ind][0]}_{IND[ind][1]}_{hz}.png")
    print('done')
