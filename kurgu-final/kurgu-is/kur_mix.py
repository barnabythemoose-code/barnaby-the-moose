# yeni stemlerden miks: toplam -> kompresor -> -15 LUFS -> limiter (gecikme telafili) -> olcum
import sys, json, subprocess, numpy as np, soundfile as sf, re, os
Y='/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu/yeni'; IS='/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu/is'
ST=Y+'/out/stems/'; OUT=Y+'/out/'; SR=48000
tl=json.load(open(IS+'/out/timeline.json'))
stems={n:(sf.read(ST+n+'.wav',dtype='float32')[0] if os.path.exists(ST+n+'.wav') else None) for n in ['diyalog','sfx','ortam','muzik']}
N=max(len(v) for v in stems.values() if v is not None)
m=np.zeros((N,2),np.float32)
for v in stems.values():
    if v is not None: m[:len(v)]+=v
def ebur(p):
    o=subprocess.run(['ffmpeg','-i',p,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1]), float(re.findall(r'LRA:\s+(-?[\d.]+) LU',o)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',o)[-1])
raw=OUT+'mixB_raw.wav'; sf.write(raw,m,SR,subtype='FLOAT'); comp=OUT+'mixB_comp.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',raw,'-af','acompressor=threshold=-30dB:ratio=1.35:attack=40:release=700:knee=4','-c:a','pcm_f32le',comp],check=True)
I,LRA,TP=ebur(comp); Id0=ebur(ST+'diyalog.wav')[0]; g=-15.5-Id0; fin=OUT+'mixB.wav'  # diyalog -16 LUFS'a sabitle
subprocess.run(['ffmpeg','-v','error','-y','-i',comp,'-af',f'volume={g:.2f}dB,alimiter=limit=0.64:attack=5:release=80:level=false','-c:a','pcm_s24le',fin],check=True)
def _lag(ref,sig,t0,dur=10.0):
    a=ref[int(t0*SR):int((t0+dur)*SR)].mean(1); b=sig[int(t0*SR):int((t0+dur)*SR)].mean(1); n=len(a); A=np.fft.rfft(a,2*n); B=np.fft.rfft(b,2*n); xc=np.fft.irfft(A.conj()*B,2*n); xc=np.concatenate([xc[-2000:],xc[:2001]]); return int(np.argmax(xc))-2000
ref=sf.read(comp,dtype='float32')[0]; fx=sf.read(fin,dtype='float32')[0]; lg=_lag(ref,fx,110.0)
if lg>0: fx=np.concatenate([fx[lg:],np.zeros((lg,2),np.float32)]); sf.write(fin,fx,SR,subtype='PCM_24')
I2,LRA2,TP2=ebur(fin)
o=subprocess.run(['ffmpeg','-i',fin,'-af','silencedetect=n=-50dB:d=1.5','-f','null','-'],capture_output=True,text=True).stderr; sil=re.findall(r'silence_start: ([\d.]+)',o)
x=fx.mean(1)
def rms(a,b): a=max(0,int(a*SR)); b=min(len(x),int(b*SR)); seg=x[a:b]; return 20*np.log10(np.sqrt((seg**2).mean())+1e-9)
jumps=[(s['ad'],round(float(s['t0']),2),round(float(rms(s['t0'],s['t0']+3)-rms(s['t0']-3,s['t0'])),1)) for s in tl['timeline'][1:]]
# diyalog stem tek basina LUFS (konusma seviyesi)
Id,_,_=ebur(ST+'diyalog.wav') if stems['diyalog'] is not None else (None,None,None)
res=dict(ham_I=I,gain=round(g,2),I=I2,LRA=LRA2,TP=TP2,limiter_gecikme=lg,sessizlik=sil,sicrama=jumps,asan=[j for j in jumps if j[2]>6],diyalog_stem_I_ham=Id,diyalog_I_tahmini=(round(Id+g,1) if Id else None))
json.dump(res,open(OUT+'olcum.json','w'),indent=1,ensure_ascii=False)
print('ham I',I,'-> I',I2,'LRA',LRA2,'TP',TP2,'gecikme',lg,'sessizlik',sil,'\n sicrama>+6:',res['asan'],'\n diyalog (bus sonrasi tahmini LUFS):',res['diyalog_I_tahmini'])
