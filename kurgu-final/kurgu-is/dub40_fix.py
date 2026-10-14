import subprocess, numpy as np, sys
SR=48000
def dec(p, ac=2, tempo=1.0):
    af=['-af',f'atempo={tempo}'] if tempo!=1.0 else []
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p]+af+['-f','f32le','-ac',str(ac),'-ar',str(SR),'-'],capture_output=True).stdout,np.float32).reshape(-1,ac).copy()
def db(x): return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
def smooth_gain(n, regs, depth_db, ramp=0.08):
    g=np.ones(n,np.float32); r=int(ramp*SR); dep=10**(depth_db/20)
    for a,b in regs:
        a=int(a*SR); b=int(b*SR)
        g[a+r:b-r]=dep
        g[a:a+r]=1-(1-dep)*(0.5-0.5*np.cos(np.linspace(0,np.pi,r)))
        g[b-r:b]=dep+(1-dep)*(0.5-0.5*np.cos(np.linspace(0,np.pi,r)))
    return g
orig=dec('ses/TG-ARA-KURGU-S1-S4-mobil-v2.wav'); N=len(orig)
v0=dec('izol/blok-0-8_voice.mp3',1)[:,0]; v8=dec('izol/blok-8-44_voice.mp3',1)[:,0]
iso=np.zeros(N,np.float32); n0=min(len(v0),int(8.5*SR)); iso[:n0]=v0[:n0]; s8=int(8*SR); n8=min(len(v8),N-s8); iso[s8:s8+n8]=np.maximum(np.abs(iso[s8:s8+n8]),np.abs(v8[:n8]))
# 1) gurultu dipleri (onceki revizyonla ayni)
dip=smooth_gain(N,[(13.6,16.4)],-8)*smooth_gain(N,[(25.4,27.0)],-10)
# 2) eski konusma pencereleri: tespit edilen bolgeler ∪ replik pencereleri, ±0.08 s
old=[(1.57,5.13),(18.87,21.48),(23.77,26.13),(30.92,31.93),(37.62,39.03)]
gate=smooth_gain(N,old,-30)
# 3) dolgu: 6.0-9.0 ortam dongusu
amb=orig[int(6.0*SR):int(9.0*SR)]; xf=int(0.3*SR); w=np.linspace(0,1,xf,dtype=np.float32)[:,None]
loop=amb.copy(); 
while len(loop)<N+len(amb):
    nxt=amb.copy(); loop[-xf:]=loop[-xf:]*(1-w)+nxt[:xf]*w; loop=np.concatenate([loop,nxt[xf:]])
loop=loop[:N]; loop*=10**((-27.0-db(loop))/20)
fill=np.zeros_like(orig)
for a,b in old:
    pre=orig[int((a-0.6)*SR):int(a*SR)]; post=orig[int(b*SR):int((b+0.6)*SR)]
    tgt=min(np.mean([db(pre),db(post)])+0.5,-20.0)
    sl=slice(int((a-0.1)*SR),int((b+0.1)*SR)); fill[sl]=loop[sl]*10**((tgt-(-27.0))/20)
bed=orig*(dip*gate)[:,None]+fill*(1-gate)[:,None]
# 4) yeni replikler
L=[('H1',1.86,5.06,1.0),('H2',19.22,20.32,1.0),('B1',20.64,21.40,1.0),('H3',23.86,25.18,1.2),('B2',25.62,26.08,1.0),('B3',31.04,31.94,1.0),('B4',37.70,37.98,1.12),('H4',38.06,39.02,0.92)]
dub=np.zeros(N,np.float32); rep=[]; import os, json; os.makedirs('izol/dub40_lines',exist_ok=True); LJ=[]
for name,a,b,tp in L:
    x=dec(f'el/dub40/{name}.mp3',1,tp)[:,0]
    # bas/son sessizligi kirp (-45 dBFS)
    w=int(0.05*SR); env=np.array([np.abs(x[i:i+w]).max() for i in range(0,len(x)-w,w)]); thr=10**(-38/20)
    act=np.where(env>thr)[0]; i0=max(0,act[0]*w-int(0.03*SR)); i1=min(len(x),(act[-1]+1)*w+int(0.10*SR))
    on=np.where(env>env.max()*10**(-12/20))[0][0]*w-i0  # sesli baslangic (ornek)
    x=x[i0:i1]
    cap=int(((b-a)+0.35)*SR)
    if len(x)>cap: x=x[:cap]; x[-int(0.08*SR):]*=np.linspace(1,0,int(0.08*SR),dtype=np.float32)
    ref=db(iso[int(a*SR):int(b*SR)]); g=10**((ref-db(x))/20); g=min(g,0.95/np.abs(x).max())
    s=max(0,int((a+0.06)*SR)-on); dub[s:s+len(x)]+=x*g
    a_eff=s/SR
    subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-c:a','pcm_s24le',f'izol/dub40_lines/{name}.wav'],input=x.astype(np.float32).tobytes(),check=True); LJ.append(dict(id=name,t=round(a_eff,3),sure=round(len(x)/SR,3),tempo=tp,kazanc_dB=round(float(20*np.log10(g)),1),pencere=[a,b]))
    bedwin=bed[int(a*SR):int(b*SR)]
    rep.append((name,round(a_eff,2),round(a_eff+len(x)/SR,2),round(b,2),'yeni dB',round(db(x*g),1),'eski-ses-kalinti dB',round(db(orig[int(a*SR):int(b*SR)]*gate[int(a*SR):int(b*SR),None]),1),'yatak dB',round(db(bedwin),1)))
for r in rep: print(r)
print('B3 penceresi orig dB',round(db(orig[int(30.92*SR):int(31.93*SR)]),1),'iso dB',round(db(iso[int(30.92*SR):int(31.93*SR)]),1),'| 36.1-36.65 orig',round(db(orig[int(36.1*SR):int(36.65*SR)]),1),'iso',round(db(iso[int(36.1*SR):int(36.65*SR)]),1))
json.dump(dict(replikler=LJ,eski_konusma_pencereleri=old),open('izol/dub40_lines/liste.json','w'),indent=1)
c45=int(44.5*SR)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac','2','-ar',str(SR),'-i','-','-c:a','pcm_s24le','izol/dub40_bed_0-44.5.wav'],input=bed[:c45].astype(np.float32).tobytes(),check=True)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-c:a','pcm_s24le','izol/dub40_dubonly_0-44.5.wav'],input=dub[:c45].astype(np.float32).tobytes(),check=True)
# 5) esinti yatagi
br=dec('el/sfx/breeze_sakin_lp.wav',2); br=np.tile(br,(N//len(br)+1,1))[:N]; br*=10**((-41.0-db(br))/20)
env=np.ones(N,np.float32); env[int(44*SR):int(45*SR)]=np.linspace(1,0,SR); env[int(45*SR):]=0
new=bed+dub[:,None]+br*env[:,None]
# 6) 44 s'de orijinale cross-fade
c0=int(44.0*SR); c1=int(44.5*SR); wv=np.linspace(0,1,c1-c0,dtype=np.float32)[:,None]
out=orig.copy(); out[:c0]=new[:c0]; out[c0:c1]=new[c0:c1]*(1-wv)+orig[c0:c1]*wv
pk=np.abs(out[:c1]).max(); print('tepe (limiter oncesi)',round(20*np.log10(pk),1))

def _lag(ref, sig, SR=48000, t0=None, dur=10.0):
    import numpy as np
    n=min(len(ref),len(sig)); t0=int((n/SR-dur)/2) if t0 is None else t0
    a=ref[int(t0*SR):int((t0+dur)*SR)]; b=sig[int(t0*SR):int((t0+dur)*SR)]
    a=a.mean(1) if a.ndim>1 else a; b=b.mean(1) if b.ndim>1 else b
    m=len(a); A=np.fft.rfft(a,2*m); B=np.fft.rfft(b,2*m); xc=np.fft.irfft(A.conj()*B,2*m)
    xc=np.concatenate([xc[-2000:],xc[:2001]]); return int(np.argmax(xc))-2000
def _shift_back(x, lag):
    import numpy as np
    if lag<=0: return x
    return np.concatenate([x[lag:], np.zeros((lag,)+x.shape[1:],x.dtype)])
lim=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac','2','-ar',str(SR),'-i','-','-af','alimiter=limit=0.95:attack=5:release=60:level=false','-f','f32le','-'],input=out.astype(np.float32).tobytes(),capture_output=True,check=True).stdout,np.float32).reshape(-1,2)
lg=_lag(out,lim,SR,t0=1.0,dur=10.0); print('limiter gecikme (ornek):',lg); lim=_shift_back(lim,lg)
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ac','2','-ar',str(SR),'-i','-','-c:a','pcm_s24le','ses_dn/TG-ARA-KURGU-S1-S4-mobil-v2_rev3.wav'],input=lim.astype(np.float32).tobytes(),check=True)
# kontrol: saniyelik RMS 0-44 (rev3 vs rev2)
r2=dec('ses_dn/TG-ARA-KURGU-S1-S4-mobil-v2_rev2.wav')
print('sn  rev2  rev3'); 
for t in range(0,44): print(t, round(db(r2[t*SR:(t+1)*SR]),1), round(db(out[t*SR:(t+1)*SR]),1))
