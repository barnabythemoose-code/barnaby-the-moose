# kare imzasi: her kare 16x9 gri -> vektor; iki video arasinda ofset bul
import subprocess, numpy as np, sys
def sigs(p, w=32, h=18):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    a=np.frombuffer(r,np.uint8).reshape(-1,h*w).astype(np.float32)
    a-=a.mean(1,keepdims=True); n=np.linalg.norm(a,axis=1,keepdims=True)+1e-6; return a/n
def best_offset(short, long):
    S=sigs(short); L=sigs(long); best=(-1,0)
    for off in range(0, len(L)-len(S)+1):
        c=float((S*L[off:off+len(S)]).sum(1).mean())
        if c>best[0]: best=(c,off)
    return best, len(S), len(L)
if __name__=='__main__':
    (c,off),ns,nl=best_offset(sys.argv[1],sys.argv[2])
    print(f"{sys.argv[1].split('/')[-1]} ({ns} kare) in {sys.argv[2].split('/')[-1]} ({nl} kare): offset {off} kare = {off/24:.3f} sn, corr {c:.3f}, aralik {off/24:.3f}-{(off+ns)/24:.3f}")
