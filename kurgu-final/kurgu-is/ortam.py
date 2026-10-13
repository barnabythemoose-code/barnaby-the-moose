# Seedance klip sesinden konusmasiz ortam: replik pencereleri (+-0,1 sn) ayni klibin en sessiz 0,6 sn'lik oda tonuyla (dongu, 15 ms capraz) degistirilir
import subprocess,numpy as np,soundfile as sf,json,sys,os
IS=sys.argv[1]; SR=48000
rep=json.load(open(IS+'/vc_girdi/replikler.json'))
def dec(p):
    o=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(o,dtype=np.float32).reshape(-1,2).copy()
SRC={'S6-1':'ses/TG-S6-1_d01.wav'}
for klip in ['S6-1','S6-2-D2','S6-3-E2','S6-4','S6-5','S7-1-B','S8-1-B2']:
    src=IS+'/'+SRC.get(klip,f'ses/B090-TG-{klip}_d01.wav')
    if not os.path.exists(src): src=IS+f'/02-klipler-ham/B090-TG-{klip}_d01.mp4'
    x=dec(src); n=len(x)
    win=[(max(0,r['t0']-0.10),min(n/SR,r['t1']+0.10)) for r in rep if r['klip']==klip]
    # en sessiz 0,6 sn (pencereler disinda)
    best=None; L=int(0.6*SR); hop=int(0.05*SR)
    for s in range(0,n-L,hop):
        t=s/SR
        if any(a-0.6<t<b for a,b in win): continue
        e=float((x[s:s+L]**2).mean())
        if best is None or e<best[0]: best=(e,s)
    tone=x[best[1]:best[1]+L].copy(); xf=int(0.015*SR)
    out=x.copy()
    for a,b in win:
        i0=int(a*SR); i1=int(b*SR); need=i1-i0
        buf=np.zeros((need+L,2),np.float32); pos=0
        while pos<need:
            seg=tone.copy()
            if pos>0: seg[:xf]*=np.linspace(0,1,xf)[:,None]; buf[pos:pos+xf]*=np.linspace(1,0,xf)[:,None]
            buf[pos:pos+L]+=seg; pos+=L-xf
        fill=buf[:need]
        # kenarlarda capraz
        fill[:xf]=fill[:xf]*np.linspace(0,1,xf)[:,None]+x[i0:i0+xf]*np.linspace(1,0,xf)[:,None]
        fill[-xf:]=fill[-xf:]*np.linspace(1,0,xf)[:,None]+x[i1-xf:i1]*np.linspace(0,1,xf)[:,None]
        out[i0:i1]=fill
    sf.write(IS+f'/ortam/{klip}_ortam.wav',out,SR,subtype='FLOAT')
    print(klip,'oda tonu @%.2f'%(best[1]/SR),'pencere',len(win),'kaynak',os.path.basename(src))
