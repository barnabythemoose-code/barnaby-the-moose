# MFCC(13) ortalama kosinus mesafesi + diag-Gauss simetrik KL + spektral merkez; referans = kilit/B1..H3 (benzerlik.py mantigi)
import sys, json, subprocess, numpy as np, glob, os
from scipy.fft import dct
SR=16000
def dec(p):
    o=subprocess.run(["ffmpeg","-v","error","-i",p,"-vn","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(o,dtype=np.float32).astype(float)
def mel_fb(n=40,nfft=512,sr=SR):
    hz2m=lambda f:2595*np.log10(1+f/700); m2hz=lambda m:700*(10**(m/2595)-1)
    pts=m2hz(np.linspace(hz2m(60),hz2m(sr/2),n+2)); b=np.floor((nfft+1)*pts/sr).astype(int); fb=np.zeros((n,nfft//2+1))
    for i in range(n):
        l,c,r=b[i],b[i+1],b[i+2]
        for k in range(l,c): fb[i,k]=(k-l)/max(c-l,1)
        for k in range(c,r): fb[i,k]=(r-k)/max(r-c,1)
    return fb
FB=mel_fb()
def feat(x):
    x=np.append(x[0],x[1:]-0.97*x[:-1]); n,h=400,160; w=np.hanning(n)
    F=np.array([x[s:s+n]*w for s in range(0,len(x)-n,h)])
    en=10*np.log10((F**2).mean(1)+1e-12); F=F[en>en.max()-30]
    P=np.abs(np.fft.rfft(F,512))**2; M=np.log(P@FB.T+1e-10); C=dct(M,type=2,axis=1,norm="ortho")[:,1:13]
    fr=np.fft.rfftfreq(512,1/SR); cen=(P*fr).sum(1)/(P.sum(1)+1e-12); return C,float(np.median(cen))
def stat(C): return C.mean(0),C.std(0)+1e-6
def cosd(a,b): return float(1-a@b/(np.linalg.norm(a)*np.linalg.norm(b)))
def kl(m1,s1,m2,s2): return float(np.mean(0.5*((s1/s2)**2+(s2/s1)**2-2+(m1-m2)**2*(1/s1**2+1/s2**2))))
def agg(paths):
    Cs=[];cens=[]
    for p in paths:
        C,c=feat(dec(p)); Cs.append(C); cens.append(c)
    return np.vstack(Cs),float(np.median(cens))
K=sys.argv[1]; REF={"barnaby":[f"{K}/B1.wav",f"{K}/B2.wav",f"{K}/B3.wav"],"hazel":[f"{K}/H1.wav",f"{K}/H2.wav",f"{K}/H3.wav"]}
refs={k:stat(agg(v)[0]) for k,v in REF.items()}
olcek={k:(round(cosd(refs[k][0],refs[o][0]),4),round(kl(*refs[k],*refs[o]),3)) for k,o in (("barnaby","hazel"),("hazel","barnaby"))}
print("olcek (diger karakter):",olcek)
out=[]
for p in sys.argv[2:]:
    kim="hazel" if "_H" in os.path.basename(p) else ("barnaby" if "_B" in os.path.basename(p) else None)
    if not kim: continue
    C,cen=agg([p]); m,s=stat(C); mr,sr=refs[kim]
    r=dict(dosya=os.path.basename(p),kim=kim,cos=round(cosd(mr,m),4),KL=round(kl(mr,sr,m,s),3),merkez_hz=round(cen))
    out.append(r); print(r)
json.dump(dict(olcek=olcek,sonuc=out),open(sys.argv[1]+"/benzerlik-olcum.json","w"),ensure_ascii=False,indent=1)
