# B090 ses kutuphanesi: cues.json + kaynaklar -> zaman koduyla adlandirilmis tekil ogeler + tam uzunluk izler + cue sheet
import json, subprocess, os, csv, re, shutil, unicodedata, tempfile, numpy as np, soundfile as sf
SR=48000; FPS=24
W='/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu'; IS=W+'/is'
OUT=W+'/kutuphane/B090-ses-kutuphanesi'; TMP=W+'/kutuphane/_tmp'
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(TMP,exist_ok=True)
for d in ['01-diyalog','01-diyalog/S1-S4-yeni-dublaj','02-efekt/yerlesim','02-efekt/kaynak','02-efekt/kaynak/alternatifler','03-ortam','03-ortam/alternatifler','04-muzik','05-hazir-miksler-B-efektli','05-hazir-miksler-A-efektsiz','06-S1-S4-blok','07-orijinal-klip-sesleri','08-tam-uzunluk-izler','09-referans']: os.makedirs(f'{OUT}/{d}',exist_ok=True)
cues=json.load(open(IS+'/out/cues.json')); tl=json.load(open(IS+'/out/timeline.json')); TL=tl['timeline']; TOTAL=tl['toplam_sn']; T={x['ad']:x for x in TL}
rep={r['id']:r for r in json.load(open(IS+'/vc_girdi/replikler.json'))}
TXT={'S8-2_A68':("Anne","Who's there?"),'S8-2_H69':("Hazel","They kept the bell for you."),'S8-2_B70':("Barnaby","They waited."),'S8-3_A71':("Anne","Barnaby?"),'S8-3_B72':("Barnaby","Mama."),'S8-4_A73':("Anne","Look how big you are."),'S8-4_B74a':("Barnaby","I followed Papa's pie."),'S8-4_B74b':("Barnaby","It was a tree."),'S8-4_A75':("Anne","Papa's pie has a tree in it."),'S8-4_P76':("Baba","Hmm, maple."),'S9-1_A77':("Anne","Now we can ring it, Papa."),'S9-1_P78':("Baba","Hmm."),'S9-2a_A79':("Anne","Thank you, Hazel."),'S9-2b_B81':("Barnaby","So, ten?"),'S9-2b_H82':("Hazel","Ten out of ten."),'S6-4_Hmm':("Barnaby (ham Seedance)","Hmm.")}
DUB40={'H1':("Hazel","First bell, Barnaby. Last bell is sunset."),'H2':("Hazel","They're going our way."),'B1':("Barnaby","No time!"),'H3':("Hazel","Four out of ten, Barnaby."),'B2':("Barnaby","Four?"),'B3':("Barnaby","Papa's step!"),'B4':("Barnaby","Oh."),'H4':("Hazel","Eight out of ten.")}
SFXAD={'v2_a-hand-pulled-small-brass-bell-on-a-wood_LcY6IM':'el-cani','one-single-distant-canada-goose-honk-hig_v1_2Wv0AU':'kaz-otusu-uzak','v2_two-soft-slow-hoof-steps-on-dry-autumn-l_1byJJW':'toynak-adimlari-yaprak','one-single-crisp-dry-leaf-crunching-unde_v1_mb30Fo':'kuru-yaprak-citirtisi','two-quick-deep-sniffs-through-a-big-soft_v1_9F8l2L':'burun-cekme','a-tiny-soft-touch-of-two-furry-noses-a-v_v1_7QywER':'burun-burna-dokunus','a-tiny-sticky-tap-a-hoof-tip-touching-st_v1_eczWyI':'yapiskan-toynak-tik','v2_a-small-hazelnut-set-down-gently-on-a-wo_sYd1oY':'findik-masaya','v2_three-gentle-soft-thumps-of-large-furry-_v3Vd38':'tabure-pat-pat','tepik_v1_Hq3Izf':'tepik-agir','tepik_v1_hafif':'tepik-hafif'}
def tc(t): m=int(t//60); s=t-60*m; return f"{m:02d}m{int(s):02d}s{int(round((s-int(s))*1000)):03d}"
def smpte(t): f=int(round(t*FPS)); return f"00:{f//FPS//60:02d}:{f//FPS%60:02d}:{f%FPS:02d}", f
def slug(s,n=34):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode(); s=re.sub(r"[^A-Za-z0-9]+","-",s).strip('-'); return s[:n].rstrip('-')
def sahne(t):
    s=[x for x in TL if x['t0']<=t+1e-6]; return s[-1]['ad'] if s else '?'
def nch(p): return int(subprocess.run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','stream=channels','-of','csv=p=0',p],capture_output=True,text=True).stdout.strip() or 2)
def load(p,t0=0.0,t1=None,tempo=1.0,unity_mono=False):
    # render.py ile ayni sira: 48 kHz stereo float'a cevir -> kes -> (varsa) atempo
    if unity_mono and nch(p)==1:
        cmd=['ffmpeg','-v','error','-i',p,'-ss',f'{t0:.6f}']+(['-to',f'{t1:.6f}'] if t1 else [])+['-f','f32le','-ac','1','-ar',str(SR),'-']
        a=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32); a=np.stack([a,a],1).copy()
    else:
        cmd=['ffmpeg','-v','error','-i',p,'-ss',f'{t0:.6f}']+(['-to',f'{t1:.6f}'] if t1 else [])+['-f','f32le','-ac','2','-ar',str(SR),'-']
        a=np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32).reshape(-1,2).copy()
    if abs(tempo-1)>1e-3:
        t_in=TMP+'/_t.wav'; t_out=TMP+'/_t2.wav'; sf.write(t_in,a,SR,subtype='FLOAT')
        subprocess.run(['ffmpeg','-v','error','-y','-i',t_in,'-af',f'atempo={tempo}','-c:a','pcm_f32le',t_out],check=True)
        a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',t_out,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True).stdout,np.float32).reshape(-1,2).copy()
    return a
NORM={}
def save(path,a):
    pk=float(np.abs(a).max()) if len(a) else 0.0
    if pk>=1.0:
        g=10**(-0.5/20)/pk; a=a*g; NORM[os.path.relpath(path,OUT)]=round(20*np.log10(g),1)
    sf.write(path,a,SR,subtype='PCM_24',format='FLAC'); return len(a)/SR
rows=[]
def row(dosya,klasor,kat,t,sure,karakter='',metin='',kazanc='',tempo='',zarf='',kaynak='',k0='',k1='',not_='',kullanilan_sure=None):
    if t is None or t=='': s,f,sah,t1='','','',''
    else: s,f=smpte(t); sah=sahne(t); t1=round(t+sure,3)
    rows.append(dict(dosya=dosya,klasor=klasor,kategori=kat,sahne=sah,film_t0_sn=('' if t in (None,'') else round(t,3)),film_tc=s,kare=f,sure_sn=round(sure,3),kurguda_kullanilan_sure_sn=round(kullanilan_sure if kullanilan_sure is not None else sure,3),film_t1_sn=t1,karakter=karakter,metin=metin,kurguda_kullanilan_kazanc_dB=kazanc,tempo=tempo,zarf_otomasyon=zarf,kaynak_dosya=kaynak,kaynak_t0=k0,kaynak_t1=k1,**{'not':not_}))
def rel(p): return os.path.relpath(p,IS)
def idscene_t0(i):
    pre=i.split('_')[0]; c=[x for x in TL if x['ad']==pre or x['ad'].startswith(pre+' ') or x['ad'].startswith(pre+'-')]; return c[0]['t0'] if c else None
# ---- 01 diyalog
for c in cues:
    if c['stem']!='diyalog': continue
    i=c['id']; kim,metin=(rep[i]['kim'].capitalize(),rep[i]['metin']) if i in rep else TXT[i]
    tp=c.get('tempo',1.0) or 1.0; a=load(c['file'],c.get('src_t0',0.0),c.get('src_t1'),tp)
    fn=f"{tc(c['t'])}_{i}_{kim.split()[0]}_{slug(metin)}.flac"; d=save(f'{OUT}/01-diyalog/{fn}',a)
    nt='ham seviye (kazanc uygulanmadi)'+ ('; tempo UYGULANDI' if abs(tp-1)>1e-3 else '')
    st0=idscene_t0(i)
    if st0 is not None and c['t']<st0-1e-3: nt+=f"; SES-ONCE (J-cut): sahne kesiminden {int(round((st0-c['t'])*FPS))} kare once baslar, BILEREK, kaydirma"
    if i=='S6-4_Hmm': nt+='; Seedance klibinden ham kesit'
    row(fn,'01-diyalog','diyalog',c['t'],d,kim,metin,c.get('gain_db',0),tp,'',rel(c['file']),c.get('src_t0',0.0),c.get('src_t1') or '',nt)
LJ=json.load(open(IS+'/izol/dub40_lines/liste.json'))
for L in LJ['replikler']:
    kim,metin=DUB40[L['id']]; a=load(IS+f"/izol/dub40_lines/{L['id']}.wav",unity_mono=True)
    fn=f"{tc(L['t'])}_S1-S4_{L['id']}_{kim}_{slug(metin)}.flac"; d=save(f'{OUT}/01-diyalog/S1-S4-yeni-dublaj/{fn}',a)
    row(fn,'01-diyalog/S1-S4-yeni-dublaj','diyalog (yeni dublaj, 0-44 sn)',L['t'],d,kim,metin,L['kazanc_dB'],L['tempo'],'',f"izol/dub40_lines/{L['id']}.wav",'','',f"kirpilmis+tempo uygulanmis hal; ham TTS: el/dub40/{L['id']}.mp3 (ElevenLabs eleven_v3); eski Seedance replik penceresi {L['pencere'][0]}-{L['pencere'][1]} sn; ham seviye, mono->stereo birebir")
# ---- 02 efekt
seen={}
for c in cues:
    if c['stem']!='sfx': continue
    base=os.path.splitext(os.path.basename(c['file']))[0]; ad=SFXAD.get(base,slug(base))
    if base not in seen:
        a=load(c['file']); src=f"{ad}__{base}.flac"; save(f'{OUT}/02-efekt/kaynak/{src}',a); seen[base]=(src,a)
        row(src,'02-efekt/kaynak','efekt kaynak',None,len(a)/SR,'','','','','',rel(c['file']),'','','tek kopya kaynak; yerlesimler 02-efekt/yerlesim')
    src,a=seen[base]; fn=f"{tc(c['t'])}_{sahne(c['t']).split()[0]}_{ad}.flac"; d=save(f'{OUT}/02-efekt/yerlesim/{fn}',a)
    row(fn,'02-efekt/yerlesim','efekt',c['t'],d,'','',c.get('gain_db',0),'','',rel(c['file']),'','',f'kaynak: 02-efekt/kaynak/{src}; ham seviye')
for d_ in ['el/sfx','el/sfx2']:
    for f in sorted(os.listdir(IS+'/'+d_)):
        b=os.path.splitext(f)[0]
        if b in seen or not f.endswith(('.mp3','.wav')) or b.startswith('breeze') or 'breeze' in b: continue
        a=load(IS+'/'+d_+'/'+f); fn=f'{slug(b,60)}.flac'; save(f'{OUT}/02-efekt/kaynak/alternatifler/{fn}',a)
        row(fn,'02-efekt/kaynak/alternatifler','efekt alternatif (kurguda kullanilmadi)',None,len(a)/SR,'','','','','',f'{d_}/{f}','','','ElevenLabs SFX varyanti; kurguda kullanilmadi')
# ---- 03 ortam
for c in cues:
    if c['stem']!='ortam': continue
    if c.get('loop_to'):
        a=load(c['file']); save(f'{OUT}/03-ortam/esinti-sakin-dongu-ham.flac',a); row('esinti-sakin-dongu-ham.flac','03-ortam','ortam kaynak',None,len(a)/SR,'','','','','',rel(c['file']),'','','esinti dongusu, HAM (cok kisik, ~-55 dBFS RMS); kurguda +14.6 dB ile kullanildi')
        need=int(c['loop_to']*SR); xf=int(0.25*SR); out=a.copy()
        while len(out)<need:
            nxt=a.copy(); out[-xf:]=out[-xf:]*np.linspace(1,0,xf)[:,None]+nxt[:xf]*np.linspace(0,1,xf)[:,None]; out=np.concatenate([out,nxt[xf:]])
        out=out[:need]*10**(c.get('gain_db',0)/20)
        fn=f"{tc(c['t'])}_S8-2_S9-2b_esinti-yatak-{c['loop_to']}s_kazancli.flac"; d=save(f'{OUT}/03-ortam/{fn}',out)
        row(fn,'03-ortam','ortam',c['t'],d,'','',c.get('gain_db',0),'','',rel(c['file']),'','',f"KAZANC UYGULANDI (+{c.get('gain_db',0)} dB): kurgudaki seviyede, 0.25 sn capraz dongu; S8-2 basindan film sonuna surekli yatak")
        continue
    a=load(c['file'],c.get('src_t0',0.0),c.get('src_t1')); fn=f"{tc(c['t'])}_{sahne(c['t']).split()[0]}_ortam.flac"; d=save(f'{OUT}/03-ortam/{fn}',a)
    sure_hedef=(c['src_t1']-c.get('src_t0',0.0)); nt='Seedance klip sesi, konusma pencereleri sessize alinmis (SUREKLI ODA TONU DEGIL, buyuk kismi sessiz); ham seviye; surekli yatak istersen 03-ortam/alternatifler esinti dosyalarini dongule'
    if d<sure_hedef-0.02: nt+=f'; kaynak ses {d:.3f} sn de bitiyor (sahne {sure_hedef:.3f} sn), son {sure_hedef-d:.3f} sn yi oda tonu ile uzat'
    row(fn,'03-ortam','ortam',c['t'],d,'','',c.get('gain_db',0),'','',rel(c['file']),c.get('src_t0',0.0),round(c.get('src_t0',0.0)+d,3),nt,kullanilan_sure=d)
for f in ['soft-steady-night-breeze-moving-through-_v1_8UwtYq.mp3','v2_soft-steady-night-breeze-moving-through-_67lgpK.mp3']:
    a=load(IS+'/el/sfx/'+f); fn=f'{slug(os.path.splitext(f)[0],60)}.flac'; save(f'{OUT}/03-ortam/alternatifler/{fn}',a)
    row(fn,'03-ortam/alternatifler','ortam alternatif',None,len(a)/SR,'','','','','',f'el/sfx/{f}','','','ElevenLabs esinti (12 sn); kurgudaki dongu bunun alcak geciren filtreli hali; S6 altina surekli yatak olarak dongulenebilir')
# ---- 04 muzik
for c in cues:
    if c['stem']!='muzik': continue
    base=os.path.splitext(os.path.basename(c['file']))[0]; a=load(c['file']); fn=f"{tc(c['t'])}_{base}_ham.flac"; d=save(f'{OUT}/04-muzik/{fn}',a)
    env=sorted(c.get('env') or []); env=[q for i,q in enumerate(env) if i==0 or q[0]>env[i-1][0]]; env=[q for q in env if q[0]<=c['src_t1']+1e-6]; g0=c.get('gain_db',0)
    with open(f"{OUT}/04-muzik/{tc(c['t'])}_{base}_seviye-otomasyonu.csv",'w',newline='') as fh:
        w=csv.writer(fh); w.writerow(['film_t_sn','film_tc','toplam_kazanc_dB','not'])
        w.writerow([round(c['t'],3),smpte(c['t'])[0],round(g0+env[0][1],1) if env else g0,f"muzik baslangici; fade-in {c.get('fi',0)} sn"])
        for p in env: w.writerow([round(c['t']+p[0],3),smpte(c['t']+p[0])[0],round(g0+p[1],1),''])
        w.writerow([round(c['t']+c['src_t1'],3),smpte(c['t']+c['src_t1'])[0],'',f"muzik sonu (fade-out {c.get('fo',0)} sn, bu noktadan geriye)"])
    row(fn,'04-muzik','muzik',c['t'],d,'','',g0,'','evet (csv)',rel(c['file']),0.0,round(c['src_t1'],3),f"HAM tam parca ({d:.1f} sn); kurguda 0-{c['src_t1']:.3f} sn kullanildi (film {c['t']:.3f}-{c['t']+c['src_t1']:.3f}), fade-in {c.get('fi',0)} sn, fade-out {c.get('fo',0)} sn; taban kazanc {g0} dB + ducking otomasyonu yandaki csv (film zamani -> toplam dB, zaman sirali)",kullanilan_sure=c['src_t1'])
# ---- 05 hazir miksler
for c in cues:
    if c['stem'] not in ('hazirB','hazirA'): continue
    a=load(c['file'],c.get('src_t0',0.0),c.get('src_t1')); var='B-efektli' if c['stem']=='hazirB' else 'A-efektsiz'
    fn=f"{tc(c['t'])}_{sahne(c['t']).split()[0]}_{var}.flac"; d=save(f'{OUT}/05-hazir-miksler-{var}/{fn}',a)
    env=c.get('env'); row(fn,f'05-hazir-miksler-{var}','hazir miks (diyalog+efekt, sahibin onceki asamasi)',c['t'],d,'','',c.get('gain_db',0),'',(f"{env} (sn, dB; kurguda uygulandi, dosyada YOK)" if env else ''),rel(c['file']),c.get('src_t0',0.0),c.get('src_t1') or '','kurgudaki kesimle ayni uzunluk; ham seviye; B veya A dan BIRINI kullan')
# ---- 06 S1-S4 blok
B=OUT+'/06-S1-S4-blok'; KES=T['S1-S4 blok']['t1']
def kes_blok(a):
    a=a[:int(KES*SR)].copy(); n=int(0.04*SR); a[-n:]*=np.linspace(1,0,n)[:,None]; return a
d=save(f'{B}/00m00s000_S1-S4_blok_ORIJINAL_mobil-v2.flac',kes_blok(load(IS+'/ses/TG-ARA-KURGU-S1-S4-mobil-v2.wav'))); row('00m00s000_S1-S4_blok_ORIJINAL_mobil-v2.flac','06-S1-S4-blok','blok',0.0,d,'','',0,'','','ses/TG-ARA-KURGU-S1-S4-mobil-v2.wav',0.0,round(KES,3),f'mobil kaba kurgunun orijinal sesi, dokunulmamis (Seedance konusmalari + yaprak/ayak sesleri dahil); kurgudaki kesim noktasinda ({KES:.3f} sn = kare {int(round(KES*FPS))}) 40 ms fade ile kesildi')
d=save(f'{B}/00m00s000_S1-S4_blok_KURGUDAKI_yeni-dublaj-miks_rev3.flac',kes_blok(load(IS+'/ses_dn/TG-ARA-KURGU-S1-S4-mobil-v2_rev3.wav'))); row('00m00s000_S1-S4_blok_KURGUDAKI_yeni-dublaj-miks_rev3.flac','06-S1-S4-blok','blok',0.0,d,'','',0,'','','ses_dn/TG-ARA-KURGU-S1-S4-mobil-v2_rev3.wav',0.0,round(KES,3),f'finaldeki hal = 08/S1-S4-blok izi: 0-44 sn yeni dublaj (YATAK + SADECE-YENI-REPLIKLER + hafif esinti), 44.5 sn sonrasi orijinal (yalniz 0.95 tepe sinirlayicidan gecti); {KES:.3f} sn de kesildi')
d=save(f'{B}/00m00s000_S1-S4_blok_0-44_YATAK_eski-konusma-susturulmus.flac',load(IS+'/izol/dub40_bed_0-44.5.wav')); row('00m00s000_S1-S4_blok_0-44_YATAK_eski-konusma-susturulmus.flac','06-S1-S4-blok','blok yatak',0.0,d,'','',0,'','','izol/dub40_bed_0-44.5.wav','','','orijinal blok, 5 eski konusma penceresinde -30 dB + bloğun kendi ortam dongusuyle dolgu; 13.6-16.4 sn -8 dB ve 25.4-27.0 sn -10 dB gurultu kisma uygulanmis; yeni replik ve esinti YOK; 44.5 sn den sonra ORIJINAL ile devam et (ek yapisi ayni)')
d=save(f'{B}/00m00s000_S1-S4_blok_0-44_SADECE-YENI-REPLIKLER.flac',load(IS+'/izol/dub40_dubonly_0-44.5.wav',unity_mono=True)); row('00m00s000_S1-S4_blok_0-44_SADECE-YENI-REPLIKLER.flac','06-S1-S4-blok','blok diyalog',0.0,d,'','',0,'','','izol/dub40_dubonly_0-44.5.wav','','','8 yeni replik, kurgudaki yerinde ve kurgudaki seviyesinde (kazanclar uygulanmis); tekil ham halleri 01-diyalog/S1-S4-yeni-dublaj')
d=save(f'{B}/00m00s000_S1-S4_blok_0-44_IZOLE-ESKI-KONUSMA.flac',np.concatenate([load(IS+'/izol/blok-0-8_voice.mp3')[:int(8*SR)],load(IS+'/izol/blok-8-44_voice.mp3')])); row('00m00s000_S1-S4_blok_0-44_IZOLE-ESKI-KONUSMA.flac','06-S1-S4-blok','blok referans',0.0,d,'','',0,'','','izol/blok-0-8_voice.mp3 + izol/blok-8-44_voice.mp3','','','ElevenLabs ses ayirma ciktisi: yalniz eski Seedance konusmalari (zamanlama referansi, mikse koyma)')
d=save(f'{B}/00m00s000_S1-S4_blok_0-44_KALINTI_konusma-cikarilmis_gurultu-azaltilmis.flac',load(IS+'/izol/resid_0-44_dn.wav')); row('00m00s000_S1-S4_blok_0-44_KALINTI_konusma-cikarilmis_gurultu-azaltilmis.flac','06-S1-S4-blok','blok yatak (alternatif)',0.0,d,'','',0,'','','izol/resid_0-44_dn.wav','','','orijinal - izole konusma, afftdn gurultu azaltma; eski konusma kismen duyulur, yalniz alternatif')
amb=load(IS+'/ses/TG-ARA-KURGU-S1-S4-mobil-v2.wav',6.0,9.0); d=save(f'{B}/ortam-dongusu_blok-6-9sn.flac',amb); row('ortam-dongusu_blok-6-9sn.flac','06-S1-S4-blok','ortam kaynak',None,d,'','','','','','ses/TG-ARA-KURGU-S1-S4-mobil-v2.wav',6.0,9.0,'blogun kendi temiz ortamindan 3 sn; bosluk doldurmak icin dongule')
json.dump(dict(eski_konusma_pencereleri_sn=LJ['eski_konusma_pencereleri'],gurultu_bolgeleri_sn=[[13.6,16.4],[25.4,27.0]],aciklama='Orijinal blokta Seedance konusmalarinin bulundugu araliklar ve sikayet edilen gurultu bolgeleri (sn). Orijinali kullaniyorsan bu araliklari sustur/kis.'),open(f'{B}/eski-konusma-pencereleri.json','w'),indent=1)
# ---- 07 orijinal klip sesleri (EDL kare araliklari)
RAW=IS+'/02-klipler-ham/'
EDL=[('S5-1a','TG-S5-1a_d01.mp4',24,142),('S5-1b','TG-S5-1b_d01.mp4',9,97),('S5-2a','TG-S5-2a_d01.mp4',0,96),('S5-2b','TG-S5-2b_d02.mp4',0,96),('S5-2c','TG-S5-2c_d01.mp4',0,96),('S5-3a','TG-S5-3a_d01.mp4',0,87),('S5-3b','TG-S5-3b_d01.mp4',0,264),('S6-1','TG-S6-1_d01.mp4',0,139),('S6-2-D1','B090-TG-S6-2-D1_d01.mp4',0,126),('S6-2-D2','B090-TG-S6-2-D2_d01.mp4',0,145),('S6-3-E1','B090-TG-S6-3-E1_d01.mp4',0,142),('S6-3-E2','B090-TG-S6-3-E2_d01.mp4',0,100),('S6-4','B090-TG-S6-4_d01.mp4',0,188),('S6-5','B090-TG-S6-5_d01.mp4',0,289),('S7-1-B','B090-TG-S7-1-B_d01.mp4',0,289),('S8-1-B2 genis','B090-TG-S8-1-B2_d01.mp4',17,70),('S8-1-B2 Anne punch-in','B090-TG-S8-1-B2_d01.mp4',70,193),('S8-2','B090-TG-S8-2_d01.mp4',0,145),('S8-3','B090-TG-S8-3_d01.mp4',0,193),('S8-4','B090-TG-S8-4_d01.mp4',0,265),('S9-1','B090-TG-S9-1_d01.mp4',0,193),('S9-2a','B090-TG-S9-2a_d01.mp4',0,97),('S9-2b','B090-TG-S9-2b_d01.mp4',0,145)]
VC_KLIP={'S6-1','S6-2-D2','S6-3-E2','S6-4','S6-5','S7-1-B','S8-1-B2 genis','S8-1-B2 Anne punch-in'}
HAZIR_KLIP=lambda ad: ad.startswith('S5') or ad in ('S6-2-D1','S6-3-E1')
for ad,f,a,b in EDL:
    has=subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=codec_type','-of','csv=p=0',RAW+f],capture_output=True,text=True).stdout.strip()
    t0=T[ad]['t0']
    if not has: row('(yok)','07-orijinal-klip-sesleri','orijinal klip sesi',t0,0,'','','','','',f'02-klipler-ham/{f}',round(a/FPS,3),round(b/FPS,3),'klipte ses izi yok'); continue
    x=load(RAW+f,a/FPS,b/FPS); fn=f"{tc(t0)}_{slug(ad)}_{os.path.splitext(f)[0]}_ham-klip-sesi.flac"; d=save(f'{OUT}/07-orijinal-klip-sesleri/{fn}',x)
    nt=('ICINDE SEEDANCE KONUSMASI VAR; kurguda bu konusmalar ElevenLabs ile degistirildi (01-diyalog); yalniz ortam/efekt kaynagi, konusma pencerelerini sustur' if ad in VC_KLIP else
        'ICINDE SEEDANCE KONUSMASI VAR; 05 hazir miks AYNI konusmayi icerir, ikisini ust uste koyma' if HAZIR_KLIP(ad) else 'Seedance klip sesi; kurguda kullanilmadi (03-ortam esinti + 02-efekt kullanildi)')
    row(fn,'07-orijinal-klip-sesleri','orijinal klip sesi',t0,d,'','','','','',f'02-klipler-ham/{f}',round(a/FPS,3),round(b/FPS,3),nt)
# ---- 08 tam uzunluk izler (stems) + referans miks
STN={'blok':'S1-S4-blok','hazirB':'hazir-miksler-B-efektli','hazirA':'hazir-miksler-A-efektsiz','ortam':'ortam','diyalog':'diyalog','sfx':'efekt','muzik':'muzik'}
for st,ad in STN.items():
    a=load(IS+f'/out/stems/{st}.wav'); a=a[:int(TOTAL*SR)]; fn=f'{ad}_TAM-UZUNLUK_kurgudaki-seviye.flac'; d=save(f'{OUT}/08-tam-uzunluk-izler/{fn}',a)
    row(fn,'08-tam-uzunluk-izler','tam uzunluk iz',0.0,d,'','','','','evet (kurgudaki kazanc/zarf/fade uygulandi)','out/stems/'+st+'.wav','','','0:00 a koy, film ile ornek hassasiyetinde hizali; kategori toplami (hazir miks icin B VEYA A). Bus islem yok: izlerin toplami = REFERANS in kompresor/limiter oncesi hali')
d=save(f'{OUT}/08-tam-uzunluk-izler/REFERANS_tam-miks-B-efektli.flac',load(IS+'/out/mixB.wav')); row('REFERANS_tam-miks-B-efektli.flac','08-tam-uzunluk-izler','referans miks',0.0,d,'','','','','','out/mixB.wav','','','benim son miksim: iz toplami (B) + bus kompresor (esik -30 dB, oran 1.35, atak 40 ms, birakma 700 ms) + +7 dB + tepe sinirlayici 0.64 (-3.9 dBFS); -15.6 LUFS, TP -2.5, LRA 8.1; limiter gecikmesi telafi edildi, izlerle hizali; yalniz referans')
shutil.copy(W+'/teslim/B090-TG-FINAL-B-onizleme-480p.mp4',OUT+'/09-referans/B090-TG-FINAL-B-onizleme-480p.mp4')
# ---- normalize notlari
for r in rows:
    k=f"{r['klasor']}/{r['dosya']}"
    if k in NORM: r['not']+=f"; DIKKAT: kaynak 0 dBFS asiyordu, dosya {NORM[k]} dB kisilarak -0.5 dBFS tepeye normalize edildi (kurgu kazancina {-NORM[k]:+.1f} dB ekle)"
# ---- zaman cizelgesi + cue sheet
with open(OUT+'/zaman-cizelgesi.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['sahne','t0_sn','t1_sn','tc_in','kare_in','kare_out','gecis'])
    for x in TL: w.writerow([x['ad'],x['t0'],x['t1'],smpte(x['t0'])[0],smpte(x['t0'])[1],smpte(x['t1'])[1],x.get('gecis','')])
rows.sort(key=lambda r:((r['film_t0_sn'] if r['film_t0_sn']!='' else 1e9),r['klasor'],r['dosya']))
flds=list(rows[0].keys())
with open(OUT+'/cue-sheet.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.DictWriter(fh,fieldnames=flds); w.writeheader(); [w.writerow(r) for r in rows]
with open(OUT+'/cue-sheet_excel-tr.csv','w',newline='',encoding='utf-8-sig') as fh:
    w=csv.DictWriter(fh,fieldnames=flds,delimiter=';'); w.writeheader()
    for r in rows: w.writerow({k:(str(v).replace('.',',') if isinstance(v,float) else v) for k,v in r.items()})
json.dump(rows,open(OUT+'/cue-sheet.json','w'),ensure_ascii=False,indent=1)
shutil.rmtree(TMP,ignore_errors=True)
print('ok', len(rows), 'satir; normalize:',NORM); import collections; print(collections.Counter(r['klasor'] for r in rows))
