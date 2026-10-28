"""Apply or check static share metadata without changing page bodies or styling.
Usage: python3 scripts/link-previews.py [--check]
Configuration and PNG/icon assets are versioned in this repository.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit
import argparse,json,re,struct,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];DIST=ROOT/'dist';CONFIG=json.loads((ROOT/'preview-config.json').read_text());BASE=CONFIG['base_url'];START='<!-- link-preview:start -->';END='<!-- link-preview:end -->'
def metadata(path,page):
 url=BASE+('' if path=='index.html' else path.removesuffix('index.html') if path.endswith('/index.html') else path);image=BASE+page['image'];alt=CONFIG['name']+': '+' '.join(page['headline'])+' '+page['subtitle'];e=lambda s:escape(str(s),quote=True)
 tags=[f'<title>{e(page["title"])}</title>',f'<meta name="description" content="{e(page["description"])}">',f'<link rel="canonical" href="{url}">']
 values={'og:type':'website','og:site_name':CONFIG['name'],'og:locale':'en_US','og:title':page['title'],'og:description':page['description'],'og:url':url,'og:image':image,'og:image:secure_url':image,'og:image:type':'image/png','og:image:width':'1200','og:image:height':'630','og:image:alt':alt}
 tags += [f'<meta property="{k}" content="{e(v)}">' for k,v in values.items()]
 tags += [f'<meta name="{k}" content="{e(v)}">' for k,v in {'twitter:card':'summary_large_image','twitter:title':page['title'],'twitter:description':page['description'],'twitter:image':image,'twitter:image:alt':alt}.items()]
 tags += [f'<link rel="icon" href="{BASE}assets/previews/favicon.svg" type="image/svg+xml">',f'<link rel="icon" href="{BASE}assets/previews/icon-48.png" type="image/png" sizes="48x48">',f'<link rel="apple-touch-icon" href="{BASE}assets/previews/icon-180.png">']
 return START+'\n'+'\n'.join(tags)+'\n'+END
class Meta(HTMLParser):
 def __init__(self,html):super().__init__();self.values={};self.canonical=[];self.titles=0;self.feed(html)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta':self.values.setdefault(a.get('property',a.get('name')),[]).append(a.get('content'))
  if t=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if t=='title':self.titles+=1
def apply():
 for path,page in CONFIG['pages'].items():
  p=DIST/path;html=p.read_text();before,body=html.split('</head>',1)
  before=re.sub(re.escape(START)+r'[\s\S]*?'+re.escape(END),'',before)
  before=re.sub(r'<title\b[^>]*>[\s\S]*?</title>','',before,flags=re.I)
  before=re.sub(r'<meta\b(?=[^>]*(?:name\s*=\s*[\"\'](?:description|twitter:[^\"\']+)|property\s*=\s*[\"\']og:))[^>]*>','',before,flags=re.I)
  before=re.sub(r'<link\b(?=[^>]*rel\s*=\s*[\"\'](?:canonical|icon|shortcut icon|apple-touch-icon)[\"\'])[^>]*>','',before,flags=re.I)
  # Keep the head stable on repeat runs; never touch the body.
  before=before.rstrip()+'\n'+metadata(path,page)+'\n';p.write_text(before+'</head>'+body)
 urls=[]
 for path,p in CONFIG['pages'].items():
  url=BASE+('' if path=='index.html' else path.removesuffix('index.html') if path.endswith('/index.html') else path)
  urls.append(f'<url><loc>{url}</loc><image:image><image:loc>{BASE+p["image"]}</image:loc></image:image></url>')
 (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+'\n'.join(urls)+'\n</urlset>\n')
def check():
 actual={str(p.relative_to(DIST)) for p in DIST.rglob('*.html')};assert actual==set(CONFIG['pages']),f'Update preview-config.json for changed pages: {actual ^ set(CONFIG["pages"])}'
 for path,page in CONFIG['pages'].items():
  html=(DIST/path).read_text();m=Meta(html);assert html.count(START)==1 and html.count(END)==1
  assert m.titles==1 and len(m.canonical)==1,f'{path}: duplicate identity tags'
  expected=metadata(path,page);assert expected in html,f'{path}: stale generated metadata; run scripts/link-previews.py'
  for k in ['description','og:title','og:description','og:url','og:image','og:image:alt','twitter:card']:
   assert len(m.values[k])==1,f'{path}: duplicate {k}'
  assert m.values['og:url']==m.canonical,f'{path}: canonical mismatch'
  for k in ['og:image','og:url']:
   assert m.values[k][0].startswith(BASE),f'{path}: incorrect production origin/path'
  data=(DIST/page['image']).read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n';assert struct.unpack('>II',data[16:24])==(1200,630);assert len(data)<1000000
 for name in ['favicon.svg','icon-48.png','icon-180.png']:assert (DIST/'assets/previews'/name).stat().st_size>0
 ET.parse(DIST/'sitemap.xml')
 print(f'PASS: {len(CONFIG["pages"])} pages; unique static metadata; canonical/OG alignment; correct GitHub Pages paths; real 1200×630 PNG covers; icons; sitemap.')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
 if not args.check:apply()
 check()
