"""Assemble the 300 dpi atlas PDF: cover, index, one divider per hazard view and its 12 maps.

Usage: python scripts/products/make_atlas_pdf.py   (run make_static_maps.py first)
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # repository root
import glob,os
from PIL import Image,ImageDraw,ImageFont
R=str(ROOT)+'/'
F=lambda s,w='Regular': ImageFont.truetype(os.path.expanduser(f'~/.fonts/Roboto-{w}.ttf'),s*2)
K=2; W,H=1950*K,1140*K
UNI=Image.open(R+'assets/branding/un_emblem_blue.png').convert('RGBA'); EUI=Image.open(R+'assets/branding/eu_funded_ha_es_1200.png').convert('RGBA')
# Paste a logo scaled to a given width
def paste(im,i,x,y,w):
    i=i.resize((w,int(w*i.height/i.width))); im.paste(i,(x,y),i)
# Cover page: UN-blue band, title, credit and EU funding logo
def cover():
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    d.rectangle([0,0,W,1280],fill='#009EDB'); d.rectangle([140,120,500,480],fill='white'); paste(im,UNI,170,150,300)
    d.text((140,660),'Atlas de cronicidad de amenazas',font=F(70,'Bold'),fill='#000')
    d.text((140,860),'Índice de Cronicidad de Amenazas (HCI) asociado a El Niño',font=F(36),fill='#000')
    d.text((140,980),'Ecuador, 2015–2025',font=F(36),fill='#000')
    d.text((140,1520),'Inundaciones · aluviones · deslizamientos · socavamientos · amenazas combinadas',font=F(28),fill='#4D5560')
    d.text((140,H-240),'Elaborado por 3iS · © 2026',font=F(30,'Bold'),fill='#000'); paste(im,EUI,W-1180,H-380,1040)
    return im
# Section divider page
def divider(n,sub):
    im=Image.new('RGB',(W,H),'#009EDB'); d=ImageDraw.Draw(im)
    d.text((140,880),n,font=F(80,'Bold'),fill='#000'); d.text((140,1100),sub,font=F(34),fill='#000'); return im
# Hazard views in the order of the atlas
names=[('TODOS','Amenazas combinadas'),('flood','Inundaciones'),('debris_flow','Aluviones'),('landslide','Deslizamientos'),('scour','Socavamientos')]
# Pages 1 (cover) and 2 (index) are filled at the end
pages=[None,None]; toc=[]
# One divider plus the 12 maps of each hazard view
for hz,n in names:
    toc.append((n,len(pages)+1)); pages.append(divider(n,'12 mapas por indicador, cantones de Ecuador, 2015–2025'))
    for f in sorted(glob.glob(R+f'outputs/maps/*_{hz}.png')): pages.append(Image.open(f).convert('RGB').resize((W,H)))
pages[0]=cover()
# Index page with the first page of each section
idx=Image.new('RGB',(W,H),'#009EDB'); d=ImageDraw.Draw(idx)
d.text((140,140),'Índice',font=F(64,'Bold'),fill='#000'); y=460
for i,(n,p) in enumerate(toc):
    d.text((140,y),f'{i+1}',font=F(48,'Bold'),fill='#fff'); d.text((320,y),n,font=F(44),fill='#000'); d.text((W-500,y),str(p),font=F(44,'Bold'),fill='#000'); y+=240
d.text((140,H-240),'Elaborado por 3iS · © 2026',font=F(28),fill='#000'); pages[1]=idx
# Page-number pill at the bottom centre of map and divider pages
for k,pg in enumerate(pages):
    if k>=2:
        d=ImageDraw.Draw(pg); cx=W//2; d.rounded_rectangle([cx-90,H-124,cx+90,H-36],radius=44,fill='#009EDB'); d.text((cx,H-80),str(k+1),font=F(26,'Bold'),fill='#000',anchor='mm')
# Write the multi-page PDF at 300 dpi
pages[0].save(R+'outputs/reports/Atlas_HCI_Ecuador_completo.pdf',save_all=True,append_images=pages[1:],resolution=300)
pages[1].resize((975,570)).save('/tmp/atlas_index_preview.png'); print(len(pages))
