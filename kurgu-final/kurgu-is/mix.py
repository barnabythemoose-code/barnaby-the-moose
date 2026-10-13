# Stemlerden A/B miks: toplama -> hedef -15 LUFS -> TP -1 limiter -> olcum (I, TP, LRA, sessizlik, M-3s sicramalari)
import sys, json, subprocess, numpy as np, soundfile as sf, re, os
IS=sys.argv[1]; ST=IS+'/out/stems/'; OUT=IS+'/out/'; SR=48000
tl=json.load(open(IS+'/out/timeline.json'))
def rd(n):
    p=ST+n+'.wav'; return sf.read(p,dtype='float32')[0] if os.path.exists(p) else None
stems={n:rd(n) for n in ['blok','hazirA','hazirB','diyalog','ortam','sfx','muzik']}
N=len(stems['blok'])
def mixof(names):
    m=np.zeros((N,2),np.float32)
    for n in names:
        if stems[n] is not None: m+=stems[n][:N]
    return m
def ebur(p):
    o=subprocess.run(['ffmpeg','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1]); LRA=float(re.findall(r'LRA:\s+(-?[\d.]+) LU',o)[-1]); TP=float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',o)[-1])
    return I,LRA,TP
res={}
for ad,names in [('B',['blok','hazirB','diyalog','ortam','sfx','muzik']),('A',['blok','hazirA','diyalog','ortam','muzik'])]:
    m=mixof(names); raw=OUT+f'mix{ad}_raw.wav'; sf.write(raw,m,SR,subtype='FLOAT')
    comp=OUT+f'mix{ad}_comp.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af','acompressor=threshold=-26dB:ratio=1.8:attack=40:release=700:knee=4','-c:a','pcm_f32le',comp],check=True)
    I,LRA,TP=ebur(comp); g=-15.0-I
    fin=OUT+f'mix{ad}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',comp,'-af',f'volume={g:.2f}dB,alimiter=limit=0.82:attack=5:release=80:level=false','-c:a','pcm_s24le',fin],check=True)
    I2,LRA2,TP2=ebur(fin)
    # sessizlik (>1,5 sn, -50 dB)
    o=subprocess.run(['ffmpeg','-i',fin,'-af','silencedetect=n=-50dB:d=1.5','-f','null','-'],capture_output=True,text=True).stderr
    sil=re.findall(r'silence_start: ([\d.]+)',o)
    # kesim noktalarinda M-3s sicramasi: her kesimden once/sonra 3 sn RMS (LUFS yaklasigi: K-agirliksiz RMS dBFS farki)
    x=sf.read(fin,dtype='float32')[0].mean(1)
    def rms(a,b):
        a=max(0,int(a*SR)); b=min(len(x),int(b*SR)); seg=x[a:b]; return 20*np.log10(np.sqrt((seg**2).mean())+1e-9)
    jumps=[]
    for s in tl['timeline'][1:]:
        t=s['t0']; d=rms(t,t+3)-rms(t-3,t); jumps.append((s['ad'],round(float(t),2),round(float(d),1)))
    segs=[(s_['ad'],round(float(rms(s_['t0'],s_['t1'])),1)) for s_ in tl['timeline']]
    res[ad]=dict(seg_rms=segs,ham_I=I,gain=round(g,2),I=I2,LRA=LRA2,TP=TP2,sessizlik=sil,sicrama=jumps,asan=[j for j in jumps if j[2]>6])
    print(ad,'ham I',I,'-> I',I2,'LRA',LRA2,'TP',TP2,'sessizlik',sil); print(' sicrama>+6:',res[ad]['asan'])
json.dump(res,open(OUT+'olcum-ses.json','w'),indent=1,ensure_ascii=False)
