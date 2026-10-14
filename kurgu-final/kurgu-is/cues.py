# B090 cue sheet v2: timeline.json -> out/cues.json  (diyalog / ortam / sfx / muzik / hazirA / hazirB stemleri)
import json, sys, os, subprocess, re
IS=sys.argv[1]; tl=json.load(open(IS+'/out/timeline.json')); T={x['ad']:x for x in tl['timeline']}
def g(ad,t): return T[ad]['t0']+t
def L(ad): return T[ad]['kare']/24
VC=IS+'/el/vc/'; RT=IS+'/el/vc/retake/'; TTS=IS+'/el/tts/'; VT=IS+'/el/vc_tts/'; KR=IS+'/el/tts_kirp/'; SFX=IS+'/el/sfx/'; MZ=IS+'/el/muzik/'; ORT=IS+'/ortam/'; SES=IS+'/ses/'
# --- yardimcilar: LUFS ve sure (onbellek)
cache_p=IS+'/out/olcum-cache.json'; cache=json.load(open(cache_p)) if os.path.exists(cache_p) else {}
def lufs(p):
    if p in cache and 'I' in cache[p]: return cache[p]['I']
    o=subprocess.run(['ffmpeg','-i',p,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
    m=re.findall(r'I:\s+(-?[\d.]+) LUFS',o); v=float(m[-1]) if m else -23.0
    cache.setdefault(p,{})['I']=v; return v
def dur(p):
    if p in cache and 'd' in cache[p]: return cache[p]['d']
    assert os.path.exists(p), "YOK: "+p
    v=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
    cache.setdefault(p,{})['d']=v; return v
C=[]
def cue(stem,file,t,**k):
    k={a:b for a,b in k.items() if b is not None}; C.append(dict(stem=stem,file=file,t=round(t,3),**k))
def dlg(file,t,hedef=-17.0,tempo=1.0,**k):
    cue('diyalog',file,t,gain_db=round(hedef-lufs(file),1),tempo=tempo,fi=k.pop('fi',0.01),fo=k.pop('fo',0.03),**k)
# 1) S1-S4 blok (dokunulmaz, 0 dB)
cue('blok', SES+'TG-ARA-KURGU-S1-S4-mobil-v2.wav', 0.0, src_t1=T['S1-S4 blok']['t1'], fi=0, fo=0.04)
# 2) hazir miksler: S5 (7 parca) + D1 + E1 ; B=efektli, A=efektsiz
HZ=[('S5-1a','TG-S5-1a-B-efektli-r3.wav','TG-S5-1a-A-efektsiz-r3.wav'),('S5-1b','TG-S5-1b-B-efektli-r2.wav','TG-S5-1b-A-efektsiz-r2.wav'),('S5-2a','TG-S5-2a_B-efektli.wav','TG-S5-2a_A-efektsiz.wav'),('S5-2b','TG-S5-2b_B-efektli.wav','TG-S5-2b_A-efektsiz.wav'),('S5-2c','TG-S5-2c_B-efektli.wav','TG-S5-2c_A-efektsiz.wav'),('S5-3a','TG-S5-3a_B-efektli.wav','TG-S5-3a_A-efektsiz.wav'),('S5-3b','TG-S5-3b_B-efektli.wav','TG-S5-3b_A-efektsiz.wav'),('S6-2-D1','TG-S6-2-D1-B-efektli-v3.wav','TG-S6-2-D1-A-efektsiz-v3.wav'),('S6-3-E1','TG-S6-3-E1-B-efektli-v2-dinleme.wav','TG-S6-3-E1-A-efektsiz-v2-dinleme.wav')]
HZ_GAIN=1.5   # hazir miksler bloktan ~3 dB alcak olculdu; yarisini kapat
for ad,b,a in HZ:
    n=L(ad); 
    # S5-1a EDL 24. kareden basliyor -> kaynak ofseti
    s0=(T[ad].get('src_in',0))/24
    ek={'S5-3b':dict(env=[[0,-5],[2.5,0]]),'S5-3a':dict(gain_db=HZ_GAIN+1.0),'S6-2-D1':dict(gain_db=0.0),'S6-3-E1':dict(gain_db=0.0)}.get(ad,{})
    kw=dict(src_t0=s0, src_t1=s0+n+0.02, fi=0.02, fo=0.04, gain_db=HZ_GAIN); kw.update(ek)
    SRCD=(IS+'/ses_dn/') if ad in ('S5-2c','S5-3a','S5-3b') else SES   # gurultu azaltilmis hazir miksler (Owner notu 2:00-2:19)
    cue('hazirB', SRCD+b, T[ad]['t0'], **kw)
    cue('hazirA', SRCD+a, T[ad]['t0'], **kw)
# 3) Seedance sesli klipler: ortam (konusmasiz) + VC replikler
for ad in ['S6-1','S6-2-D2','S6-3-E2','S6-4','S6-5','S7-1-B']:
    cue('ortam', ORT+ad+'_ortam.wav', T[ad]['t0'], src_t1=L(ad)+0.02, fi=0.02, fo=0.04, gain_db=(3 if ad in ('S6-2-D2','S6-3-E2') else 0))
n=L('S8-1-B2 genis')+L('S8-1-B2 Anne punch-in'); s0=17/24
cue('ortam', ORT+'S8-1-B2_ortam.wav', T['S8-1-B2 genis']['t0'], src_t0=s0, src_t1=s0+n+0.02, fi=0.02, fo=0.04)
# E2 can kuyrugu S6-4 basina L-cut (E2 ortaminin son 0,6 sn'si)
# (E2 kuyruk can L-cut'i kaldirildi: E2 110 kareye kisaltildi, can S6-4 acilisinda EL SFX)
# S6-4 kapali agiz 'Hmm' (ham Seedance; VC yok) -4 dB
cue('diyalog', SES+'B090-TG-S6-4_d01.wav', g('S6-4',1.78), gain_db=-4, src_t0=1.78, src_t1=2.10, fi=0.02, fo=0.03, id='S6-4_Hmm')
rep=json.load(open(IS+'/vc_girdi/replikler.json'))
RETAKE={}
TTS2={'S7-1_H2','S7-1_H3','S6-5_B2'}   # VC ters testi gecemedi -> kilitli sesle TTS (asagida DUB)
KLIP={'S6-1':'S6-1','S6-2-D2':'S6-2-D2','S6-3-E2':'S6-3-E2','S6-4':'S6-4','S6-5':'S6-5','S7-1-B':'S7-1-B','S8-1-B2':'S8-1-B2 genis'}
for r in rep:
    if r['id'] in TTS2: continue
    f=RETAKE.get(r['id'], VC+r['id']+'.mp3'); loc=max(0,r['t0']-0.08)
    if r['klip']=='S8-1-B2': loc-=17/24
    hedef=-17.0 if r['kim'] in ('barnaby','hazel') else -17.5
    if r['klip'] in ('S6-2-D2','S6-3-E2'): hedef=-16.0
    if r['id'] in ('S6-5_H2','S6-5_H1'): hedef=-18.5   # kisa fisilti/soru
    dlg(f, g(KLIP[r['klip']],loc), hedef=hedef, id=r['id'])
# 4) Sessiz klipler: ruzgar yatagi + TTS/TTS->VC dublaj
breeze=SFX+'breeze_sakin_lp.wav'
t0=T['S8-2']['t0']; t1=T['Son kart']['t1']
cue('ortam', breeze, t0-0.4, loop_to=t1-t0+0.4, gain_db=round(-38-lufs(breeze),1), fi=0.4, fo=2.0)
# (dosya, klip, konusma baslangic hedefi (klip ici), onset, hedef LUFS, tempo)
T2=IS+'/el/tts2/'
DUB=[('S7-1_H2',T2+'S7-1_H2_v2_iCYXuH.mp3','S7-1-B',6.95,0.12,-17.0,1.05),
     ('S7-1_H3',T2+'S7-1_H3_v1_TQN10N.mp3','S7-1-B',10.85,0.32,-17.0,1.0),
     ('S6-5_B2',T2+'S6-5_B2_v2_xcKGmI.mp3','S6-5',6.15,0.14,-17.0,1.05),
     ('S8-2_A68',TTS+'who-s-there_v1_vrl0xM.mp3','S8-2',1.55,0.20,-17.5,1.0),
     ('S8-2_H69',TTS+'they-kept-the-bell-for-you_v3_1s7eI1.mp3','S8-2',2.85,0.12,-17.5,1.0),
     ('S8-2_B70',TTS+'they-waited_v1_Ztspxu.mp3','S8-2',4.65,0.14,-18.0,1.0),
     ('S8-3_A71',TTS+'barnaby_v2_xNZJzx.mp3','S8-3',1.75,0.16,-17.5,1.0),
     ('S8-3_B72',VT+'mama_v3_ULpeZl.mp3','S8-3',4.70,0.10,-17.0,1.0),
     ('S8-4_A73',KR+'anne73.wav','S8-4',0.45,0.06,-20.0,1.05),
     ('S8-4_B74',VT+'ifollowed_v2_NtsFQk.mp3','S8-4',3.45,0.18,-17.0,1.05),
     ('S8-4_A75',TTS+'papa-s-pie-has-a-tree-in-it_v1_Ntrjo9.mp3','S8-4',6.80,0.16,-17.5,1.05),
     ('S8-4_P76',KR+'baba76.wav','S8-4',9.45,0.14,-17.5,1.0),
     ('S9-1_A77',TTS+'now-we-can-ring-it-papa_v1_w5EF7A.mp3','S9-1',0.30,0.06,-17.5,1.0),
     ('S9-1_P78',TTS+'hm_v2_FBgUJb.mp3','S9-1',2.45,0.12,-18.0,1.0),
     ('S9-2a_A79',TTS+'thank-you-hazel_v3_UfEuZr.mp3','S9-2a',1.76,0.10,-17.5,1.08),
     ('S9-2b_B81',VT+'soten_v4_anPTjy.mp3','S9-2b',1.35,0.02,-17.0,1.0),
     ('S9-2b_H82',VT+'tenoutof_v3_fk2qvo.mp3','S9-2b',4.62,0.22,-17.0,1.0)]
for id_,f,ad,hedef_t,on,hedef,tempo in DUB:
    dlg(f, g(ad, hedef_t-on/tempo), hedef=hedef, tempo=tempo, id=id_)
# 5) SFX (klip ici saniye, dosya, dB)
SF=[('S6-4',0.05,'v2_a-hand-pulled-small-brass-bell-on-a-wood_LcY6IM.mp3',-16),
    ('S7-1-B',6.2,'one-single-distant-canada-goose-honk-hig_v1_2Wv0AU.mp3',-10),('S7-1-B',6.7,'one-single-distant-canada-goose-honk-hig_v1_2Wv0AU.mp3',-13),('S7-1-B',7.1,'one-single-distant-canada-goose-honk-hig_v1_2Wv0AU.mp3',-15),
    ('S8-2',0.3,'v2_two-soft-slow-hoof-steps-on-dry-autumn-l_1byJJW.mp3',-12),('S8-2',0.95,'one-single-crisp-dry-leaf-crunching-unde_v1_mb30Fo.mp3',-20),
    ('S8-3',3.3,'two-quick-deep-sniffs-through-a-big-soft_v1_9F8l2L.mp3',-14),('S8-3',6.55,'a-tiny-soft-touch-of-two-furry-noses-a-v_v1_7QywER.mp3',-16),
    ('S8-4',2.9,'a-tiny-sticky-tap-a-hoof-tip-touching-st_v1_eczWyI.mp3',-26),
    ('S9-1',3.15,'v2_a-hand-pulled-small-brass-bell-on-a-wood_LcY6IM.mp3',-8),
    ('S9-2a',1.60,'v2_a-small-hazelnut-set-down-gently-on-a-wo_sYd1oY.mp3',-20),
    ('S9-2b',5.45,'v2_three-gentle-soft-thumps-of-large-furry-_v3Vd38.mp3',-18)]
for ad,t,f,db in SF:
    cue('sfx', SFX+f, g(ad,t), gain_db=round(db-13-lufs(SFX+f),1), fi=0.01, fo=0.08)   # referans: -13 LUFS'lik can = db
# 5b) Cizgi film tepik (S9-1): Baba 2 agir, Barnaby 7 hafif; tepe hedefi Baba -9 dBFS, Barnaby -14 dBFS
SF2=IS+'/el/sfx2/'
for t,kim in [(4.42,'baba'),(5.06,'baba'),(5.95,'b'),(6.36,'b2'),(6.70,'b'),(6.95,'b2'),(7.07,'b3'),(7.24,'b2'),(7.53,'b')]:
    f,gdb={'baba':('tepik_v1_Hq3Izf.mp3',3.0),'b':('tepik_v1_hafif.wav',7.0),'b2':('tepik_v1_hafif.wav',6.0),'b3':('tepik_v1_hafif.wav',3.0)}[kim]
    cue('sfx', SF2+f, g('S9-1',t-0.03), gain_db=gdb, fi=0.0, fo=0.05, id='tepik')
# 6) Muzik: ducking zarfi diyalog cue'larindan
def dlg_windows():
    w=[]
    for c in C:
        if c['stem']!='diyalog': continue
        d=(c['src_t1']-c.get('src_t0',0)) if c.get('src_t1') else dur(c['file'])/c.get('tempo',1.0)
        w.append((c['t'],c['t']+d))
    return sorted(w)
def env_for(t_start,t_end,base,duck,extra=()):
    pts=[(0.0,base)]; last=base
    wins=[(a,b,duck) for a,b in dlg_windows() if b>t_start and a<t_end]+[(a,b,d) for a,b,d in extra]
    for a,b,d in sorted(wins):
        a=max(a-0.25,t_start); b=min(b+0.35,t_end)
        pts+= [(a-t_start-0.3,base),(a-t_start,base+d),(b-t_start,base+d),(b-t_start+0.6,base)]
    pts=[(round(max(0,x),3),y) for x,y in pts]
    # monoton zaman: ayni/geri giden noktalari minimum al
    out=[]
    for x,y in sorted(pts):
        if out and x<=out[-1][0]+0.02: out[-1]=(out[-1][0],min(out[-1][1],y))
        else: out.append((x,y))
    return [[x,y] for x,y in out]
m1=MZ+'M1_S6-S7_64s.mp3'; m2=MZ+'M2_S8-S9_58s.mp3'
m1t=T['S6-1']['t0']-1.5; m1end=T['S7-1-B']['t1']+0.3
m1base=round(-26.0-lufs(m1),1)
hz_extra=[(T['S6-2-D1']['t0'],T['S6-2-D1']['t1'],-5),(T['S6-3-E1']['t0'],T['S6-3-E1']['t1'],-5)]
cue('muzik', m1, m1t, src_t1=m1end-m1t, fi=1.5, fo=1.2, gain_db=m1base, env=env_for(m1t,m1end,0,-9,hz_extra))
m2t=T['S8-1-B2 genis']['t0']-1.0; m2end=T['Son kart']['t1']
m2base=round(-26.0-lufs(m2),1)
e=env_for(m2t,m2end,0,-8,[(T['S9-1']['t0']+4.2,T['S9-1']['t0']+7.9,-7)])   # tepik serisi altinda muzik -7 dB; 
# final yukselisi: son replikten sonra +5 dB, kartta cozulme
# S8-3 kuyrugunda kucuk muzik kabarmasi (+3 dB) -> S8-4 girisindeki seviye sicramasini yumusatir
tb=T['S8-4']['t0']; e+= [[round(tb-0.75-m2t,3),0],[round(tb-0.40-m2t,3),3.0],[round(tb-0.15-m2t,3),3.0]]
e=sorted(e); e=[[x,y] for i,(x,y) in enumerate(e) if i==0 or x>e[i-1][0]]
lastd=max(b for a,b in dlg_windows()); e+= [[round(lastd+0.6-m2t,3),0],[round(lastd+2.0-m2t,3),5],[round(T['Son kart']['t0']+1.5-m2t,3),5],[round(m2end-m2t,3),-6]]
cue('muzik', m2, m2t, src_t1=m2end-m2t, fi=1.0, fo=2.5, gain_db=m2base, env=e)
json.dump(cache,open(cache_p,'w')); json.dump(C,open(IS+'/out/cues.json','w'),ensure_ascii=False,indent=1)
print(len(C),'cue; M1',m1t,m1end,'M2',m2t,m2end)
