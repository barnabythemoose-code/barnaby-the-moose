# Inceleyici listeleri (4 fps + 24 fps) + manuel gozlem -> kutuphane eslemesi -> ek_efektler.json
import json, re, sys, glob
Y='/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu/yeni'
def load_results(paths):
    ev=[]
    for p in paths:
        try: raw=open(p).read(); d=json.loads(raw[raw.find('{'):])
        except Exception as e: print('okunamadi',p,e); continue
        res=d.get('result',d)
        for k,v in res.items():
            if isinstance(v,dict) and 'events' in v:
                for e in v['events']: e['kaynak']=k; ev.append(e)
    return ev
paths=sys.argv[1:]
ev=load_results(paths)
# manuel gozlem (0-24 sn, kendi incelemem)
MAN=[(1.72,1.72,'Hazel omuzdan beliriyor','sparkle ping','cartoon','soft','sure'),
     (10.45,10.45,'kosu baslangici','whoosh','cartoon','medium','sure'),(10.5,13.95,'kosu','running gallop','foley','medium','sure'),
     (10.8,10.8,'yapraklar ucusuyor','leaf flurry','foley','medium','sure'),(11.6,11.6,'yapraklar ucusuyor','leaf flurry','foley','medium','sure'),(12.05,12.05,'genis plan yapraklar havada','leaf flurry','foley','soft','sure'),
     (14.0,14.5,'kazlarin onunde fren','skid stop','cartoon','strong','sure'),(14.15,14.15,'yaprak savrulmasi','leaf flurry','foley','medium','sure'),
     (22.45,22.45,'yaprak yiginina dalis','jump take-off','cartoon','medium','sure'),(22.7,22.7,'yigina dusus','dive into leaf pile thud','cartoon','strong','sure'),(23.05,23.05,'kafa yapraklardan cikiyor','leaf rustle','foley','soft','sure')]
for m in []: ev.append(dict(t=m[0],t_end=m[1],action=m[2],sfx=m[3],style=m[4],intensity=m[5],confidence=m[6],kaynak='manuel'))
# esleme kurallari: (regex, kutuphane adi, ham tepe dBFS, tur)
RULES=[
 (r'foot pat|waddle|webbed|creak|cricket|owl|ambience|bed ', None, 0, 'yok'),
 (r'slide whistle', None, 0, 'yok'),
 (r'leaf (fall|flutter|drift|float)|leaves (fall|flutter|drift|float|tumble|settl)|falling leaf|falling leaves|fluttering leaves', 'yaprak-dususu', -27, 'tek'),
 (r'skid|brake|screech|slid', 'fren', -18, 'tek'),
 (r'doink|boing', 'doink', -21, 'tek'),
 (r'dive|leaf pile|body thud|whump|bump|falls (down|over|onto|into)|tumble|plop|flop|collaps|thud', 'govde-pat', -19, 'tek'),
 (r'land', 'inis', -20, 'tek'),
 (r'take-?off|sproing|jump|leap|hop', 'ziplama', -23, 'tek'),
 (r'gallop|running|run ', 'dortnala', -26, 'dongu'),
 (r'flurr|kicked|scatter|swirl|leaves fly|flying leaves|leaves burst', 'yaprak-ucusmasi', -25, 'tek'),
 (r'whoosh|swish|head turn|double[- ]take|spin|whirl', 'whoosh', -26, 'tek'),
 (r'stomp', 'tepik-hafif', -20, 'tek'),
 (r'hoof|footstep|step|walk|trot|prance|skip', 'adim', -28, 'adim'),
 (r'long sniff|deep sniff|inhale', 'uzun-koklama', -27, 'tek'),
 (r'sniff|nostril|smell', 'burun-cekme', -27, 'tek'),
 (r'ping|sparkle|eyes pop|eyes open|eyes widen|realiz|idea|\bting\b|sting|perk', 'ping', -30, 'tek'),
 (r'antler|branch|twig', 'boynuz-dal', -27, 'tek'),
 (r'rustle|cloth|hug|wool|shawl|sweater|fabric|wipe|nuzzle|fur', 'yun', -29, 'tek'),
 (r'bell', 'el-cani', -22, 'tek'),
 (r'honk|goose|geese', 'kaz', -24, 'kaz'),
 (r'sit|stool|settle', 'govde-pat', -27, 'tek'),
 (r'wind|breeze|gust', 'ruzgar', -30, 'tek'),
 (r'ribbon|scent|magic|shimmer|glow', 'koku', -28, 'tek'),
 (r'drip|syrup|drop', 'surup', -24, 'tek'),
 (r'tap|tick|touch|poke', 'yapiskan', -28, 'tek'),
 (r'crunch|leaf', 'yaprak-citirti', -29, 'tek'),
 (r'breath|exhale|puff|sigh|gasp', None, 0, 'yok'),
]
INT={'soft':-4,'medium':0,'strong':+3}; CONF={'sure':0,'likely':-1,'guess':-5}
out=[]
for e in ev:
    hit=None
    for i,txt in enumerate((e.get('sfx','').lower(), e.get('action','').lower())):
        for rx,name,peak,tur in RULES:
            if re.search(rx,txt):
                if name in ('inis','govde-pat','fren','doink','ziplama') and i==1: continue
                hit=(name,peak,tur); break
        if hit: break
    if hit and hit[0] in ('fren','doink','ziplama','inis') and e.get('confidence')=='guess': continue
    if hit and hit[0] in ('whoosh','yun') and (e.get('confidence')=='guess' or (hit[0]=='whoosh' and e.get('intensity')=='soft')): continue
    if not hit or hit[0] is None: continue
    name,peak,tur=hit; g=peak+INT.get(e.get('intensity','medium'),0)+CONF.get(e.get('confidence','likely'),-1)
    out.append(dict(t=round(float(e['t']),3),t_end=round(float(e.get('t_end',e['t'])),3),ad=name,tepe=g,tur=tur,aciklama=e.get('action','')[:80],kaynak=e.get('kaynak',''),guven=e.get('confidence','')))
out.sort(key=lambda x:(0 if x['kaynak'].startswith('R') else 1, x['t'], x['ad']))
# tekillestirme: ayni ad 0.2 sn icinde -> en yuksek tepeyi tut; adimlar 0.17 sn
ded=[]
for x in out:
    win=0.17 if x['tur']=='adim' else 0.25
    same=[d for d in ded if d['ad']==x['ad'] and (abs(d['t']-x['t'])<win or (d['kaynak'][:1]!=x['kaynak'][:1] and abs(d['t']-x['t'])<0.5))]
    if same: same[0]['tepe']=max(same[0]['tepe'],x['tepe']); same[0]['t_end']=max(same[0]['t_end'],x['t_end']); continue
    ded.append(x)
# kosu donguleri: araliklari birlestir, icindeki tekil adimlari at
runs=[]
for x in [d for d in ded if d['tur']=='dongu']:
    a,b=x['t'],max(x['t_end'],x['t']+0.8)
    if runs and a<=runs[-1][1]+0.3: runs[-1][1]=max(runs[-1][1],b); runs[-1][2]=max(runs[-1][2],x['tepe'])
    else: runs.append([a,b,x['tepe']])
final=[d for d in ded if d['tur']!='dongu' and not (d['ad']=='fren' and any(abs(a-d['t'])<0.3 for a,b,_ in runs)) and not (d['tur']=='adim' and any(a-0.1<=d['t']<=b+0.1 for a,b,_ in runs))]
for a,b,g in runs: final.append(dict(t=a,t_end=b,ad='dortnala',tepe=g,tur='dongu',aciklama='kosu',kaynak='birlesik',guven='sure'))
final.sort(key=lambda x:x['t'])
final.sort(key=lambda x:x['t'])
# --- son filtreler
def ok(x):
    a=x['aciklama'].lower()
    if x['ad']=='fren' and not re.search(r'skid|brake|stop|halt|dead|screech',a): return False
    if x['ad']=='doink' and re.search(r'cut to|hard cut',a): return False
    if x['ad']=='ping' and x['guven']!='sure': return False
    return True
final=[x for x in final if ok(x)]
for x in final:
    if x['ad']=='doink' and re.search(r'eyes|eye ',x['aciklama'].lower()): x['ad']='ping'; x['tepe']=min(x['tepe'],-28)
    if x['ad']=='govde-pat' and x['guven']!='sure': x['tepe']=min(x['tepe'],-24)
# ziplama'dan hemen once gelen doink'i at; 0.7 sn icindeki ikinci fren'i at
keep=[]
for i,x in enumerate(final):
    if x['ad']=='doink' and any(y['ad']=='ziplama' and 0<=y['t']-x['t']<0.25 for y in final): continue
    if x['ad']=='fren' and any(y['ad']=='fren' and 0<x['t']-y['t']<0.7 for y in keep): continue
    keep.append(x)
final=keep
json.dump(final,open(Y+'/ek_efektler.json','w'),ensure_ascii=False,indent=1)
import collections; print(len(ev),'olay ->',len(final),'efekt;',dict(collections.Counter(x['ad'] for x in final)))
