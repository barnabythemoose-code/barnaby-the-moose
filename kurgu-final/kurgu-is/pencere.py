# Seedance sesli kliplerde konusma pencerelerini bul: 20 ms RMS zarfi, esik = taban+12 dB, beklenen araliklarla eslestir
import numpy as np, soundfile as sf, sys, json
SR=48000
def env(x, hop=0.02):
    n=int(hop*SR); m=len(x)//n; e=np.sqrt((x[:m*n].reshape(m,n)**2).mean(1)+1e-12); return 20*np.log10(e)
def regions(db, thr, hop=0.02, minlen=0.12, gap=0.25):
    on=db>thr; out=[]; i=0
    while i<len(on):
        if on[i]:
            j=i
            while j<len(on) and on[j]: j+=1
            out.append([i*hop,j*hop]); i=j
        else: i+=1
    # birlestir
    m=[]
    for r in out:
        if m and r[0]-m[-1][1]<gap: m[-1][1]=r[1]
        else: m.append(r)
    return [r for r in m if r[1]-r[0]>=minlen]
klipler=json.load(open(sys.argv[1])); res={}
for ad,info in klipler.items():
    x,sr=sf.read(info['wav']); x=x.mean(1) if x.ndim>1 else x
    db=env(x); taban=np.percentile(db,10); thr=max(taban+12,-45)
    regs=regions(db,thr)
    res[ad]={'taban_dB':round(float(taban),1),'esik':round(float(thr),1),'aktif':[[round(a,2),round(b,2)] for a,b in regs],'beklenen':info['beklenen']}
    print(ad,'taban',round(float(taban),1),'aktif',[[round(a,2),round(b,2)] for a,b in regs])
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
