# Cue-sheet tabanli stem render: cues.json -> stems/*.wav (48 kHz stereo float), toplam sure timeline'dan
import json, subprocess, numpy as np, soundfile as sf, sys, os
SR=48000
def load(p, mono=False):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','f32le','-ac','2','-ar',str(SR),'-'],capture_output=True)
    a=np.frombuffer(r.stdout,dtype=np.float32).reshape(-1,2).copy(); return a
def lin(db): return 10**(db/20)
def fade(a, fi, fo):
    n=len(a); i=int(fi*SR); o=int(fo*SR)
    if i>0: a[:i]*=np.linspace(0,1,i)[:,None]
    if o>0: a[n-o:]*=np.linspace(1,0,o)[:,None]
    return a
def render(cues, total, out_dir):
    stems={}
    for c in cues:
        st=c['stem']; buf=stems.setdefault(st, np.zeros((int(total*SR)+SR,2),np.float32))
        a=load(c['file'])
        s0=int(c.get('src_t0',0)*SR); s1=int(c['src_t1']*SR) if c.get('src_t1') else len(a); a=a[s0:s1].copy()
        if c.get('loop_to'):  # dongu: hedef sureye kadar 0,25 sn capraz ile tekrar
            need=int(c['loop_to']*SR); xf=int(0.25*SR); out=a.copy()
            while len(out)<need:
                nxt=a.copy(); out[-xf:]=out[-xf:]*np.linspace(1,0,xf)[:,None]+nxt[:xf]*np.linspace(0,1,xf)[:,None]
                out=np.concatenate([out,nxt[xf:]])
            a=out[:need]
        if c.get('tempo') and abs(c['tempo']-1)>1e-3:   # atempo (<=1.05)
            sf.write('_t.wav',a,SR,subtype='FLOAT'); subprocess.run(['ffmpeg','-v','error','-y','-i','_t.wav','-af',f"atempo={c['tempo']}",'-c:a','pcm_f32le','_t2.wav'],check=True); a=load('_t2.wav')
        a=fade(a, c.get('fi',0.01), c.get('fo',0.02))*lin(c.get('gain_db',0))
        # zarf (ducking vb.): [(t_rel, dB), ...] noktalari arasi dogrusal
        if c.get('env'):
            t=np.arange(len(a))/SR; pts=sorted(c['env']); pts=[q for i,q in enumerate(pts) if i==0 or q[0]>pts[i-1][0]]; g=np.interp(t,[p[0] for p in pts],[p[1] for p in pts]); a=a*lin(g)[:,None].astype(np.float32)
        p0=int(c['t']*SR); p1=min(p0+len(a), len(buf)); buf[p0:p1]+=a[:p1-p0]
    os.makedirs(out_dir,exist_ok=True)
    for st,buf in stems.items():
        sf.write(f'{out_dir}/{st}.wav', buf[:int(total*SR)], SR, subtype='FLOAT')
    return stems
if __name__=='__main__':
    cues=json.load(open(sys.argv[1])); tl=json.load(open(sys.argv[2])); render(cues, tl['toplam_sn'], sys.argv[3]); print('ok', tl['toplam_sn'])
