# bir PNG/JPG karesini (veya bir videonun ilk karesini) baska bir videonun karelerinde ara
import subprocess, numpy as np, sys
def sig_img(p,w=32,h=18):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    a=np.frombuffer(r,np.uint8).astype(np.float32); a-=a.mean(); return a/(np.linalg.norm(a)+1e-6)
def sigs(p,w=32,h=18):
    r=subprocess.run(['ffmpeg','-v','error','-i',p,'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    a=np.frombuffer(r,np.uint8).reshape(-1,h*w).astype(np.float32); a-=a.mean(1,keepdims=True); return a/(np.linalg.norm(a,axis=1,keepdims=True)+1e-6)
q=sig_img(sys.argv[1]); L=sigs(sys.argv[2]); c=L@q; top=np.argsort(-c)[:5]
print(sys.argv[1].split('/')[-1],'in',sys.argv[2].split('/')[-1],'->',[(int(i),round(i/24,3),round(float(c[i]),4)) for i in top])
