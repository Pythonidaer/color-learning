"""Optional development tool: requires Pillow and the open DejaVu fonts.
Run from any directory. PNGs are committed; CI checks them without Pillow.
"""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];CONFIG=json.loads((ROOT/'preview-config.json').read_text());DIST=ROOT/'dist'
FONT=Path('/usr/share/fonts/truetype/dejavu')
def font(size,bold=False,serif=False):return ImageFont.truetype(str(FONT/('DejaVuSerif.ttf' if serif else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),size)
for path,page in CONFIG['pages'].items():
 image=Image.new('RGB',(1200,630),'white');draw=ImageDraw.Draw(image);ink='#202124';muted='#5c6066';accent=page.get('accent',CONFIG['accent'])
 draw.rectangle((0,0,1200,12),fill=accent)
 draw.text((65,48),CONFIG['name'],font=font(27,True),fill=ink)
 draw.text((65,100),page['kind'],font=font(17),fill=muted)
 draw.line((65,145,1135,145),fill='#d8dadd',width=2)
 for i,line in enumerate(page['headline']):
  size=76
  while draw.textbbox((0,0),line,font=font(size,True))[2]>790:size-=1
  draw.text((60,185+i*97),line,font=font(size,True),fill=ink)
 if CONFIG['mark']=='Aa':
  draw.text((910,212),'Aa',font=font(130,serif=True),fill=accent)
  draw.line((900,370,1128,370),fill=accent,width=3)
 else:
  for y,c in [(195,'#a52e47'),(260,'#e7b64c'),(325,'#458a91')]:draw.rounded_rectangle((947,y,1107,y+48),radius=24,fill=c)
 draw.text((65,432),page['subtitle'],font=font(25),fill=muted)
 draw.line((65,510,1135,510),fill='#d8dadd',width=2)
 draw.text((65,546),CONFIG['base_url'].replace('https://',''),font=font(20),fill=muted)
 dest=DIST/page['image'];dest.parent.mkdir(parents=True,exist_ok=True);image.save(dest,optimize=True)
icons=DIST/'assets/previews';icons.mkdir(parents=True,exist_ok=True)
for size in [48,180]:
 image=Image.new('RGB',(size,size),'white');d=ImageDraw.Draw(image);f=font(int(size*.60),serif=CONFIG['mark']=='Aa',bold=CONFIG['mark']=='C');box=d.textbbox((0,0),CONFIG['mark'],font=f);w=box[2]-box[0];h=box[3]-box[1];d.text(((size-w)/2-box[0],(size-h)/2-box[1]),CONFIG['mark'],font=f,fill=CONFIG['accent']);image.save(icons/f'icon-{size}.png')
(icons/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="8" fill="white"/><text x="32" y="44" text-anchor="middle" font-size="38" font-family="'+('Georgia,serif' if CONFIG['mark']=='Aa' else 'Arial,sans-serif')+'" fill="'+CONFIG['accent']+'">'+CONFIG['mark']+'</text></svg>')
print('Rendered',len(CONFIG['pages']),'covers and three icon files.')
