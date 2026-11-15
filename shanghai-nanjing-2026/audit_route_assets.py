#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json,re,hashlib,datetime
root=Path(__file__).resolve().parent
assets=root/'assets'
spec=[
('TR01','2026-11-19','上海抵達／浦東入城'),
('SH01','2026-11-20','武康路／安福路'),
('SH02','2026-11-20','思南公館'),
('SH03','2026-11-20','新天地北里'),
('SH04','2026-11-20','上生新所'),
('SH05','2026-11-20','愚園路／靜安寺'),
('SH06','2026-11-20','上海植物園'),
('SH07','2026-11-20','豫園／九曲橋／城隍廟'),
('NJ01','2026-11-21','朝天宮／老門東'),
('NJ02','2026-11-22','玄武湖／雞鳴寺／明城牆'),
('NJ03','2026-11-23','頤和路／清涼山'),
('NJ04','2026-11-24','陵園路／美齡宮／明孝陵'),
('NJ05','2026-11-25','中山陵／音樂台／靈谷寺'),
('NJ06','2026-11-26','棲霞山'),
('NJ07','2026-11-27','南京博物院／總統府／秦淮'),
('NJ08','2026-11-28','南京彈性行程'),
('TR02','2026-11-29','南京返回上海龍陽路'),
('TR03','2026-11-30','龍陽路至浦東機場')]
mapping={
'SH01':['assets/routes/2026-11-20/SH01_wukang_approved_original.jpg'],
'SH05':['assets/routes/2026-11-20/SH05_yuyuan_jingan_v03.svg'],
'SH06':['assets/routes/2026-11-20/option-06-botanical-garden-entrances.svg'],
'NJ02':['assets/NJ02-01_20261122_jiming_jiefang_xuanwumen_geo.svg'],
'NJ03':['assets/routes/2026-11-23/NJ03_20261123_yihe_qingliang_v01.svg'],
'NJ04':['assets/routes/2026-11-24/NJ04_20261124_lingyuan_meiling_mingxiaoling_v02.svg'],
'NJ05':['assets/routes/2026-11-25/NJ05_20261125_zhongshan_music_linggu_v01.svg'],
'NJ06':['assets/routes/2026-11-26/NJ06_20261126_qixiashan_official_A_v01.svg'],
'NJ07':['assets/routes/2026-11-27/NJ07_20261127_museum_presidential_qinhuai_v01.svg']}
records=[]
for code,date,name in spec:
    paths=mapping.get(code,[])
    files=[]
    for p in paths:
        f=root/p
        files.append(dict(path=p,exists=f.is_file(),bytes=f.stat().st_size if f.exists() else None,sha256=hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None))
    status='核准原圖已入庫，仍需路線與手機驗收' if code=='SH01' else ('有示意 SVG，未通過實景與完整手繪驗收' if paths else '正式獨立路線圖缺失')
    records.append(dict(id=code,date=date,title=name,assets=files,status=status,route_verified=False,mobile_verified=False))
out={'generated':'2026-11-15','scope':'MD 基準：上海 7 選項、南京 8 日、交通 3 張','note':'這是實際檔案存在性檢查；未校核的 SVG 或 Library 合集不得算完成。SH05 檔名含 yuyuan 但其編號屬愚園路，須確認圖面後才採用。','routes':records}
(root/'ROUTE_ASSET_MANIFEST_20261115.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# 上海南京路線圖｜實際檔案與驗收清單','', '基準：上海 SH01–SH07（7選項）、南京 NJ01–NJ08（8日）、交通 TR01–TR03（3張）。此表只反映實際檔案，不代表地理正確或可交付。','','| 編號 | 日期 | 路線 | 實體檔案 | 狀態 |','|---|---|---|---|---|']
for r in records:
    paths=[a['path'].split('/')[-1] for a in r['assets'] if a['exists']]
    lines.append('| '+ ' | '.join([r['id'],r['date'][5:],r['title'],'、'.join(paths) or '無',r['status']])+' |')
lines+=['','## Library 已找回但尚未進入 iMac 的五份素材','- SH02 思南公館獨立水彩；SH02–SH03 雙圖；NJ01 水彩；上海南京總覽 A、B。已另行命名並打包，但不能列為本機已入庫。','- 兩份總覽的標註與路線版本有差異；不得自動拆圖後宣稱地理正確。','- 11/20 既有 preview 是 SH01–SH07 七個選項；早期補缺文件提到 9 個候選入口，需對照最新 MD 決定是否增加其他方案。','- TR01/TR02/TR03 無正式圖。','- SH05 現有 SVG 檔名混入 yuyuan，需防止愚園路與豫園誤配。','','## 驗收原則','每條圖需查核起終點、景點順序、實際位置、地鐵出口、營業資訊、餐飲位置、導航可點擊及 375/390px 手機顯示。未通過一律 route_verified=false。']
(root/'ROUTE_ASSET_AUDIT_20261115.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('AUDITED',len(records),'route IDs, with local assets',sum(bool(r['assets']) for r in records),'missing',sum(not r['assets'] for r in records))

[executed on device: iMac.local (54c486af-ddc6-40a8-bc75-9a00c8d92c8d)]