#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate route asset identity and local HTML image references without claiming geography verification."""
from pathlib import Path
import json,re,sys,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
data=json.loads((root/'ROUTE_ASSET_MANIFEST_20261115.json').read_text(encoding='utf8'))
errors=[];warnings=[]
for route in data['routes']:
 code=route['id']
 for a in route['assets']:
  p=root/a['path']
  if not p.is_file():errors.append(f'{code}: missing {a["path"]}');continue
  if p.suffix=='.svg':
   try:
    doc=ET.parse(p).getroot()
    title=' '.join(''.join(e.itertext()) for e in doc.iter() if e.tag.endswith('title'))
    text=' '.join(''.join(e.itertext()) for e in doc.iter() if e.tag.endswith('text'))
    if not title: warnings.append(f'{code}: SVG missing title')
    if code=='SH05' and ('愚園' not in title or '豫園' in title):errors.append('SH05: mistaken 愚園/豫園 identity')
    if code=='SH06' and '植物園' not in title+text:errors.append('SH06: incorrect identity')
    if code=='NJ04' and '美齡' not in title+text:errors.append('NJ04: incorrect identity')
   except ET.ParseError as e:errors.append(f'{code}: malformed SVG: {e}')
for page in root.glob('*.html'):
 s=page.read_text(encoding='utf8')
 for m in re.finditer(r"<img\b[^>]*?src=[\"\']([^\"\']+)[\"\']",s,re.I|re.S):
  src=m.group(1)
  if src.startswith(('data:','http:','https:')):continue
  if not (page.parent/src.split('#')[0].split('?')[0]).exists():errors.append(f'{page.name}: missing image {src}')
print('Route identity checks:',len(data['routes']),'routes;',len(errors),'errors;',len(warnings),'warnings')
for x in errors:print('ERROR',x)
for x in warnings:print('WARN',x)
sys.exit(bool(errors))

[executed on device: iMac.local (54c486af-ddc6-40a8-bc75-9a00c8d92c8d)]