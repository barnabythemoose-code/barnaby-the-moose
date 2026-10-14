# B090 sifirdan ses kurgusu: TTS diyalog + ElevenLabs efekt/ortam/muzik -> cues.json (render.py formati)
import json, subprocess, os, glob, numpy as np, soundfile as sf
SR=48000
W='/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu'; IS=W+'/is'; Y=W+'/yeni'
os.makedirs(Y+'/dia',exist_ok=True); os.makedirs(Y+'/sfxn',exist_ok=True); os.makedirs(Y+'/out',exist_ok=True)
tl=json.load(open(IS+'/out/timeline.json')); T={x['ad']:x for x in tl['timeline']}; TOTAL=tl['toplam_sn']
def dec(p,ac=1,af=None):
    cmd=['ffmpeg','-v','error','-i',p]+(['-af',af] if af else [])+['-f','f32le','-ac',str(ac),'-ar',str(SR),'-']
    a=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32); return a.reshape(-1,ac).copy() if ac>1 else a.copy()
def db(x): return 20*np.log10(np.sqrt((x**2).mean())+1e-12)
def span(x,thr=-40,w=0.02):
    n=int(w*SR); e=np.array([20*np.log10(np.sqrt((x[i:i+n]**2).mean())+1e-9) for i in range(0,len(x)-n,n)]); on=np.where(e>thr)[0]
    return (on[0]*w, min(len(x)/SR,(on[-1]+1)*w)) if len(on) else (0.0,len(x)/SR)
def atempo(x,tp):
    if abs(tp-1)<1e-3: return x
    sf.write(Y+'/_t.wav',x,SR,subtype='FLOAT'); subprocess.run(['ffmpeg','-v','error','-y','-i',Y+'/_t.wav','-af',f'atempo={tp}','-c:a','pcm_f32le',Y+'/_t2.wav'],check=True); return dec(Y+'/_t2.wav')
cues=[]
def cue(stem,file,t,**k): d=dict(stem=stem,file=file,t=round(float(t),3)); d.update(k); cues.append(d); return d
# ------------------------------------------------------------------ DIYALOG
DIA_RMS=-23.0  # ham (bus oncesi) konusma RMS hedefi, mono dBFS
L={r['id']:r for r in json.load(open(Y+'/replikler.json'))}
P={r['id']:r['pencere'] for r in json.load(open(Y+'/pencereler.json'))}
SEC=json.load(open(Y+'/retake_secim.json'))
# D1 / E1 ek replikleri (pencereler: A-efektsiz miksin enerji profili)
L['S6-2-D1_B1']=dict(id='S6-2-D1_B1',kim='Barnaby',metin="My antlers grew. Mama won't know me."); P['S6-2-D1_B1']=[144.64,147.34]
L['S6-2-D1_H1']=dict(id='S6-2-D1_H1',kim='Hazel',metin="Your nose found a pie three valleys away."); P['S6-2-D1_H1']=[147.94,149.75]
L['S6-3-E1_H1']=dict(id='S6-3-E1_H1',kim='Hazel',metin="Sound travels at night. Call."); P['S6-3-E1_H1']=[155.91,157.97]
L['S6-3-E1_B1']=dict(id='S6-3-E1_B1',kim='Barnaby',metin="Mama. Papa."); P['S6-3-E1_B1']=[158.37,161.0]
NIGHT=lambda t: t>=138.75
dia=[]  # (id, t, dur, path)
CAP={'S4-4_H25':1.2,'S6-5_B2':1.33,'S5-1_B29':1.0,'S4-4_B24':1.1}  # anlasilirlik > senkron: kisa unlemler dogal tempoda
def place_line(k, x, win, extra_db=0.0, split_pause=None):
    s0,s1=span(x); pre=int(0.03*SR); x=x[max(0,int(s0*SR)-pre):int(s1*SR)+int(0.08*SR)]
    sl=(len(x)/SR)-0.03-0.08; wl=win[1]-win[0]
    need=sl/wl if wl>0.2 else 1.0; cap=1.3 if sl<1.0 else 1.22
    cap=CAP.get(k,cap); tp=min(max(need,0.92),cap)
    x=atempo(x,tp)
    g=10**((DIA_RMS+extra_db-(db(x[int(0.03*SR):]) ))/20); x=x*g
    n=int(0.06*SR); x[-n:]*=np.linspace(1,0,n,dtype=np.float32)
    path=Y+f'/dia/{k}.wav'; sf.write(path,x,SR,subtype='FLOAT')
    t=win[0]+0.03-0.03  # konusma baslangici agiz acilisinda
    dia.append(dict(id=k,t=round(t,3),dur=round(len(x)/SR,3),tempo=round(tp,2),asim=round(len(x)/SR-0.11-wl,2),path=path))
for k,r in L.items():
    f=Y+f'/tts/{k}_r2.mp3' if SEC.get(k,{}).get('secim')=='r2' else Y+f'/tts/{k}.mp3'
    x=dec(f); win=P[k]; extra=(-1.5 if NIGHT(win[0]) else 0.0)+(-0.5 if r['kim']=='Hazel' else 0.0)
    if k=='S6-3-E1_B1':
        # 'Mama.' / 'Papa.' ic duraklamadan bol, iki agiz penceresine ayri yerlestir
        n=int(0.02*SR); e=np.array([20*np.log10(np.sqrt((x[i:i+n]**2).mean())+1e-9) for i in range(0,len(x)-n,n)]); s0,s1=span(x)
        i0=int(s0/0.02); i1=int(s1/0.02); q=np.where(e[i0:i1]<-38)[0]
        if len(q):
            # en uzun ic bosluk
            runs=np.split(q,np.where(np.diff(q)!=1)[0]+1); run=max(runs,key=len); cut=(i0+run[len(run)//2])*0.02
            place_line(k+'a',x[:int(cut*SR)],[158.37,159.45],extra); place_line(k+'b',x[int(cut*SR):],[159.91,161.0],extra); continue
    place_line(k,x,win,extra)
# 0-40 sn yeni dublaj (izol/dub40_lines, kirpilmis+tempo uygulanmis)
for Lj in json.load(open(IS+'/izol/dub40_lines/liste.json'))['replikler']:
    x=dec(IS+f"/izol/dub40_lines/{Lj['id']}.wav"); s0,s1=span(x); g=10**((DIA_RMS-0.5*(Lj['id'][0]=='H')-db(x[int(s0*SR):int(s1*SR)]))/20); x=x*g
    path=Y+f"/dia/D40_{Lj['id']}.wav"; sf.write(path,x,SR,subtype='FLOAT'); dia.append(dict(id='D40_'+Lj['id'],t=Lj['t'],dur=round(len(x)/SR,3),tempo=Lj['tempo'],asim=0,path=path))
# S8-2..S9-2b replikleri (onaylanmis yerlesim): eski cue'lardan dosya/t/tempo, seviye yeniden
old=json.load(open(IS+'/out/cues.json'))
for c in old:
    if c['stem']=='diyalog' and c['t']>=205:
        x=dec(c['file']); 
        if c.get('src_t1'): x=x[int(c.get('src_t0',0)*SR):int(c['src_t1']*SR)]
        x=atempo(x,c.get('tempo',1.0) or 1.0); s0,s1=span(x); kim=c['id'].split('_')[1][0]
        g=10**((DIA_RMS-1.5-(0.5 if kim=='H' else 0)-db(x[int(s0*SR):int(s1*SR)]))/20); x=x*g
        x=x[:min(len(x),int((s1+0.10)*SR))]; n=int(0.06*SR); x[-n:]*=np.linspace(1,0,n,dtype=np.float32)
        path=Y+f"/dia/{c['id']}.wav"; sf.write(path,x,SR,subtype='FLOAT'); dia.append(dict(id=c['id'],t=c['t'],dur=round(len(x)/SR,3),tempo=c.get('tempo',1.0),asim=0,path=path))
dia.sort(key=lambda d:d['t'])
# cakisma kontrolu: sonraki replikten en az 60 ms once bit
for i in range(len(dia)-1):
    a,b=dia[i],dia[i+1]; end=a['t']+a['dur']
    if end>b['t']-0.06:
        x=dec(a['path']); need=end-(b['t']-0.06); keep0=int((b['t']-0.06-a['t'])*SR); cut=x[keep0:max(keep0+1,len(x)-int(0.09*SR))]
        if a['t']<205 and need<=0.4 and len(cut)>int(0.03*SR) and db(cut)>-34:   # kesilecek kisim konusma: sonraki repligi geciktir
            b['t']=round(b['t']+need,3); print('GECIKTIRILDI',b['id'],'+%.2f sn (%s icin)'%(need,a['id'])); continue
        keep=int((b['t']-0.06-a['t'])*SR)
        if keep>int(0.2*SR):
            x=x[:keep]; n=int(0.08*SR); x[-n:]*=np.linspace(1,0,n,dtype=np.float32); sf.write(a['path'],x,SR,subtype='FLOAT'); print('KIRPILDI',a['id'],'->',b['id'],round(end-(b['t']-0.06),2),'sn')
            a['dur']=round(len(x)/SR,3)
        else: print('CAKISMA',a['id'],b['id'])
for d in dia: cue('diyalog',d['path'],d['t'],src_t0=0.0,src_t1=None,fi=0.005,fo=0.005,gain_db=0.0,id=d['id'])
json.dump(_py(dia) if '_py' in globals() else dia,open(Y+'/dia_yerlesim.json','w'),indent=1,default=float)
DWIN=[(d['t'],d['t']+d['dur']) for d in dia]
# ------------------------------------------------------------------ EFEKT KAYNAKLARI (tepe -1 dBFS normalize, varyantlar)
SRC={
 'el-cani':IS+'/el/sfx/v2_a-hand-pulled-small-brass-bell-on-a-wood_LcY6IM.mp3',
 'cift-can':IS+'/el/sfx/v2_a-small-brass-bell-rings-softly-twice-fa_sGGmYB.mp3',
 'toynak':IS+'/el/sfx/v2_two-soft-slow-hoof-steps-on-dry-autumn-l_1byJJW.mp3',
 'toynak3':IS+'/el/sfx/v2_three-slow-soft-hoof-taps-on-grassy-grou_G7rDTM.mp3',
 'yaprak-citirti':IS+'/el/sfx/one-single-crisp-dry-leaf-crunching-unde_v1_mb30Fo.mp3',
 'burun-cekme':IS+'/el/sfx/two-quick-deep-sniffs-through-a-big-soft_v1_9F8l2L.mp3',
 'yun':IS+'/el/sfx/a-soft-rustle-of-a-thick-knitted-wool-sh_v1_oOjrqs.mp3',
 'tepik-agir':IS+'/el/sfx2/tepik_v1_Hq3Izf.mp3','tepik-hafif':IS+'/el/sfx2/tepik_v1_hafif.wav',
 'uzak-cift-can':Y+'/sfx/uzak-cift-can.mp3','kosu':Y+'/sfx/kosu-adimlari-dongu.mp3','uzun-koklama':Y+'/sfx/uzun-koklama.mp3',
 'thwup':Y+'/sfx/thwup.mp3','pop':Y+'/sfx/pop.mp3','kaz-surusu':Y+'/sfx/kaz-surusu.mp3','yaprak-dususu':Y+'/sfx/yaprak-dususu.mp3',
 'surup':Y+'/sfx/surup-damlasi.mp3','koku':Y+'/sfx/koku-seridi.mp3','ruzgar':Y+'/sfx/ruzgar-esintisi.mp3',
 'fren':Y+'/sfx/fren-kayma.mp3','doink':Y+'/sfx/doink.mp3','yaprak-ucusmasi':Y+'/sfx/yaprak-ucusmasi.mp3','whoosh':Y+'/sfx/whoosh.mp3',
 'ziplama':Y+'/sfx/ziplama.mp3','inis':Y+'/sfx/inis.mp3','dortnala':Y+'/sfx/dortnala-dongu.mp3','ping':Y+'/sfx/ping.mp3',
 'govde-pat':Y+'/sfx/govde-pat.mp3','boynuz-dal':Y+'/sfx/boynuz-dal.mp3','yapiskan':IS+'/el/sfx/a-tiny-sticky-tap-a-hoof-tip-touching-st_v1_eczWyI.mp3',
 'kaz':IS+'/el/sfx/one-single-distant-canada-goose-honk-hig_v1_2Wv0AU.mp3',
}
def norm_sfx(name,af=None,src=None):
    x=dec(src or SRC[name],2,af)
    if len(x)==0: raise SystemExit('BOS KAYNAK: '+name+' '+str(src or SRC[name]))
    pk=np.abs(x).max(); x=x*(10**(-1/20)/max(pk,1e-6)); p=Y+f'/sfxn/{name}.wav'; sf.write(p,x,SR,subtype='FLOAT'); return p
SF={n:norm_sfx(n) for n in SRC}
SF['el-cani-uzak']=norm_sfx('el-cani-uzak','lowpass=f=2200,highpass=f=200',SRC['el-cani'])
SF['tepik-uzak']=norm_sfx('tepik-uzak','lowpass=f=1200',SRC['tepik-agir'])
SF['koku-ters']=norm_sfx('koku-ters','areverse',SRC['koku'])
SF['mmf']=norm_sfx('mmf','lowpass=f=900,asetrate=48000*0.92,aresample=48000',Y+'/tts/S6-4_Hmm.mp3')
SF['adim1']=norm_sfx('adim1','atrim=0:0.5,afade=t=out:st=0.4:d=0.1',SRC['toynak3']); SF['adim2']=norm_sfx('adim2','atrim=0:0.5,afade=t=out:st=0.4:d=0.1',SRC['toynak'])
SF['kaz-yakin']=norm_sfx('kaz-yakin','highpass=f=150',SRC['kaz'])
def sfx(name,t,peak,fi=0.005,fo=0.05,**k):
    st1=k.pop('src_t1',None); cue('sfx',SF[name],t,src_t0=0.0,src_t1=st1,fi=fi,fo=fo,gain_db=peak+1.0+5.0,**k)
# ------------------------------------------------------------------ EFEKT SPOT LISTESI (film sn, ham tepe dBFS)
sfx('el-cani-uzak',0.30,-24,fo=0.6)                       # ilk can (uzak)
sfx('kaz-yakin',15.7,-24); sfx('kaz-yakin',17.6,-26)      # S2-1 yerdeki kazlar (yakin tek otus)
sfx('toynak',26.4,-25); sfx('toynak',27.9,-26)            # S3-1 adimlar
sfx('tepik-uzak',30.15,-21,fo=0.4)                        # Papa'nin adimi (uzak)
sfx('tepik-hafif',36.12,-19)                              # inis (Eight out of ten)
sfx('uzun-koklama',40.55,-27)                             # S3-3 koklama
sfx('koku',41.05,-28)                                     # koku seridi
sfx('toynak',49.0,-26)                                    # yola cikis
sfx('burun-cekme',50.7,-27)                               # S3-4 pie koklama
sfx('surup',65.15,-24)                                    # S3-5 surup damlasi
sfx('toynak',67.5,-26); sfx('uzun-koklama',67.9,-28)      # yavas adim + Mm mm koklama
sfx('toynak',69.1,-27)                                    # S4-1 gozler kapali adim
sfx('toynak3',74.55,-24,src_t1=0.9)                       # son adim
sfx('thwup',75.26,-17)                                    # burun agaca
sfx('mmf',75.7,-24)                                       # bogulmus mmf
sfx('pop',77.16,-17)                                      # kurtulma
sfx('yaprak-citirti',78.4,-31)                            # S4-2 yapisik yaprak
sfx('ruzgar',80.4,-27,fi=0.4,fo=0.8)                      # 'the wind turned'
sfx('uzak-cift-can',85.9,-16,fo=0.8)                      # S4-3 DONG DONG
sfx('kaz-surusu',90.2,-23,fi=0.3,fo=0.8)                  # kaz V insert
sfx('kosu',104.2,-25,fi=0.05,fo=0.35,loop_to=1.25)        # S4-4/S5-1 kosu
sfx('yun',110.3,-29)                                      # kolla silme
sfx('yaprak-citirti',111.05,-31)                          # yaprak yapisir
sfx('yaprak-dususu',120.0,-27)                            # S5-2 yaprak duser
sfx('ruzgar',125.0,-30,fi=0.8,fo=1.2)                     # gunes batisi esintisi
sfx('el-cani-uzak',165.95,-23,fo=0.6); sfx('el-cani-uzak',169.3,-27,fo=0.6)   # S6-4 yumusak can
sfx('yun',173.95,-31)                                     # S6-5 burun silme
sfx('koku',177.6,-27)                                     # serit geri gelir
sfx('kosu',183.55,-27,fi=0.1,fo=0.5,loop_to=2.4)          # kosu baslar -> S7-1
sfx('koku-ters',186.3,-28)                                # serit kopar
sfx('kaz-surusu',191.5,-21,fi=0.3,fo=0.8)                 # S7-1 kaz V
sfx('toynak',200.1,-25)                                   # S8-1 Baba iki adim
sfx('cift-can',203.1,-21,fo=0.8)                          # ding... dong
# ---- ek efektler: kare kare inceleme listesi
import os as _os
if _os.path.exists(Y+'/ek_efektler.json'):
    EK=json.load(open(Y+'/ek_efektler.json')); man=[(c['file'],c['t']) for c in cues if c['stem']=='sfx']; n_ek=0; alt=0
    for e in EK:
        ad=e['ad']; t=e['t']; pk=e['tepe']
        fam={'kaz':'kaz-yakin','adim':None}.get(ad,ad)
        if fam and any(_os.path.basename(f).startswith(fam) and abs(tt-t)<0.35 for f,tt in man): continue
        if e['tur']=='dongu': sfx('dortnala',t,pk,fi=0.15,fo=0.45,loop_to=round(max(0.8,e['t_end']-t),3)); n_ek+=1; continue
        if ad=='adim': sfx('adim1' if alt%2==0 else 'adim2',t,pk); alt+=1; n_ek+=1; continue
        if ad=='kaz': sfx('kaz-yakin',t,pk); n_ek+=1; continue
        if ad=='fren': sfx('fren',t,pk); sfx('doink',t+0.42,pk-3); n_ek+=2; continue
        sfx(ad,t,pk); n_ek+=1
    print('ek efekt cue:',n_ek)
for c in old:                                              # S8-2..S9-2b onaylanmis efektler
    if c['stem']=='sfx' and c['t']>=205: cues.append(dict(c))
# ------------------------------------------------------------------ ORTAM
def loop_gain(p,target): x=dec(p); return target-db(x)
GUN=Y+'/sfx/ortam-gunduz-ormani-dongu.mp3'; GECE=Y+'/sfx/ortam-gece-ormani-dongu.mp3'
cue('ortam',GUN,0.0,src_t0=0.0,src_t1=None,fi=1.5,fo=2.0,gain_db=round(loop_gain(GUN,-42.5),1),loop_to=137.0,env=[[0,0],[124.6,0],[130.0,-3],[136.5,-30]])
cue('ortam',GECE,126.0,src_t0=0.0,src_t1=None,fi=6.0,fo=3.0,gain_db=round(loop_gain(GECE,-43.5),1),loop_to=round(TOTAL-126.0,3),env=[[0,-5],[12.75,0],[round(TOTAL-126.0-3.5,3),0],[round(TOTAL-126.0,3),-12]])
# ------------------------------------------------------------------ MUZIK (ducking: diyalog pencerelerinde -8 dB)
def env_for(t0,t1,base,duck,wins,pre=0.3,post=0.5):
    pts=[[0.0,base]]
    for a,b in wins:
        if b<t0 or a>t1: continue
        a=max(a,t0); b=min(b,t1)
        pts+= [[a-pre-t0,base],[a-t0,base+duck],[b-t0,base+duck],[b+post-t0,base]]
    pts.append([t1-t0,base]); pts=sorted(pts); out=[]
    for x,y in pts:
        if out and abs(x-out[-1][0])<1e-6: out[-1][1]=min(out[-1][1],y)
        else: out.append([round(max(0,x),3),y])
    return out
def mus(p,t0,t1,fi,fo,target,extra=None):
    g=target-db(dec(p)); e=env_for(t0,t1,0,-8,DWIN)
    if extra: e=sorted(e+extra); e=[q for i,q in enumerate(e) if i==0 or q[0]>e[i-1][0]]
    cue('muzik',p,t0,src_t0=0.0,src_t1=round(t1-t0,3),fi=fi,fo=fo,gain_db=round(g,1),env=e)
mus(Y+'/muzik/M0_acilis_140s.mp3',0.0,134.0,2.0,8.0,-25.0)
mus(IS+'/el/muzik/M1_S6-S7_64s.mp3',137.25,137.25+60.883,1.5,1.2,-25.0)
lastd=max(b for a,b in DWIN); m2t=196.833; m2e=TOTAL
mus(IS+'/el/muzik/M2_S8-S9_58s.mp3',m2t,m2e,1.0,2.5,-25.0,extra=[[round(lastd+0.6-m2t,3),0],[round(lastd+1.8-m2t,3),4],[round(m2e-m2t-0.01,3),4]])
def _py(o):
    if isinstance(o,dict): return {k:_py(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [_py(v) for v in o]
    if isinstance(o,(np.floating,)): return round(float(o),4)
    if isinstance(o,(np.integer,)): return int(o)
    return o
json.dump(_py(cues),open(Y+'/cues.json','w'),indent=1)
print(len(cues),'cue;',len(dia),'replik; asim>0.25:',[(d['id'],d['asim']) for d in dia if d['asim']>0.25])
