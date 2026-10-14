# v3: yaprak ucusu kompoziti (QA-1 sonrasi): sap dahil sprite, k1844'ten gercek kabuk yamasi, tam opaklik,
# hiza bagli merkezli bulaniklik, monoton ease (2,4,7,10,14,18,23,28,34,40 px), sap-damlasi hold-out, renk rampasi
import numpy as np, os, colorsys
from PIL import Image
from scipy import ndimage as ndi
Y=os.path.dirname(os.path.abspath(__file__)); SRC=Y+'/src'; OUT=Y+'/out'
def load(k): return np.asarray(Image.open(f'{SRC}/k{k:04d}.png').convert('RGB')).astype(np.float32)/255.0
base=load(1843); after=load(1844); H,Wd=base.shape[:2]
# --- 1) sprite: siki maske (yaprak govdesi) + gevsek maskenin ona bagli bilesenleri (sap, uclar)
x0,y0,x1,y1=950,462,1070,556
reg=base[y0:y1,x0:x1]
hsv=np.array([[colorsys.rgb_to_hsv(*p) for p in row] for row in reg]); h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
red=(h<0.09)|(h>0.93); rg=reg[...,0]-reg[...,1]
strict=red&(s>0.70)&(v>0.55)&(rg>0.38); loose=red&(s>0.50)&(v>0.28)&(rg>0.17)
strict=ndi.binary_opening(strict,iterations=1); lab,n=ndi.label(strict); sizes=ndi.sum(strict,lab,range(1,n+1)); strict=lab==(1+int(np.argmax(sizes)))
lab2,n2=ndi.label(ndi.binary_closing(loose,iterations=1)); keep=np.zeros_like(strict)
for i in range(1,n2+1):
    comp=lab2==i
    if (comp&ndi.binary_dilation(strict,iterations=2)).any(): keep|=comp
mask=ndi.binary_fill_holes(keep|strict)
ys,xs=np.where(mask); cy,cx=ys.mean()+y0,xs.mean()+x0; print('yaprak merkez',round(cx,1),round(cy,1),'alan',int(mask.sum()),'bbox',xs.min()+x0,ys.min()+y0,xs.max()+x0,ys.max()+y0)
stem_zone=np.zeros_like(mask); stem_zone[ys.min()+52:, xs.min()+74:]=True
bad=stem_zone&mask&~(rg>0.235)            # sap bolgesinde kirmizi olmayan (kabuk) pikseller
mask=mask&~ndi.binary_dilation(bad,iterations=1)
alpha=np.clip(ndi.gaussian_filter(mask.astype(np.float32),0.75)*1.1,0,1)
yy0,yy1=max(0,ys.min()-3),ys.max()+4; xx0,xx1=max(0,xs.min()-3),xs.max()+4
spr_rgb=reg[yy0:yy1,xx0:xx1]; spr_a=alpha[yy0:yy1,xx0:xx1]
spr=Image.fromarray((np.dstack([spr_rgb,spr_a[...,None]])*255).astype(np.uint8),'RGBA'); spr.save(OUT+'/_sprite.png'); print('sprite',spr.size,'cekirdek rgb',np.round(spr_rgb[spr_a>0.95].mean(axis=0)*255))
# --- 2) govde yamasi: kamera sabit; k1844'ten ayni koordinatlardan gercek kabuk, tuylu dikdortgen
pm=np.zeros((H,Wd),np.float32); pm[464:580,956:1086]=1.0; pm=ndi.gaussian_filter(pm,2.0)
def patch_trunk(img): return img*(1-pm[...,None])+after*pm[...,None]
# --- 2b) sap damlasi matte'i (k1843): yaprak damlanin arkasinda kalsin
b=base*255; sap=(b[...,0]>190)&(b[...,1]>110)&(b[...,2]<140); sap[:, :820]=False; sap[:, 960:]=False; sap[:250,:]=False; sap[420:,:]=False
sap=ndi.binary_dilation(sap,iterations=2); sapm=ndi.gaussian_filter(sap.astype(np.float32),1.0); print('sap matte px',int(sap.sum()))
# --- 3) yol: kumulatif yer degistirme tablosu (px) -> e(i)
disp=np.array([2,4,7,10,14,18,23,28,34,40],np.float32); E=np.cumsum(disp)/disp.sum()
P0=np.array([cx,cy]); P1=np.array([921.0,348.0]); N=10; K0=1834
def pos_e(e): return P0+(P1-P0)*e+np.array([30.0,-22.0])*np.sin(np.pi*e**0.85)*0.6+np.array([2.5,2.0])*np.sin(np.pi*min(e/0.07,1.0))
ROT=np.cumsum([0,0,6,14,24,36,48,58,66,72]).astype(np.float32)
def rot_e(e): return -float(np.interp(e,E,ROT))
def scale_e(e): return 1.0+0.12*e
def render_sprite(e):
    im=spr.rotate(rot_e(e),resample=Image.BICUBIC,expand=True); sc=scale_e(e)
    im=im.resize((max(2,int(round(im.width*sc))),max(2,int(round(im.height*sc)))),Image.LANCZOS)
    p=pos_e(e); return im,(int(round(p[0]-im.width/2)),int(round(p[1]-im.height/2)))
def layer(e_prev,e,sub=40,shutter=0.4):
    acc=np.zeros((H,Wd,4),np.float32); d=e-e_prev
    for j in range(sub):
        t=e-d*shutter/2+d*shutter*(j+0.5)/sub          # merkezli, uzunluk = 0.4 x yer degistirme
        im,(px,py)=render_sprite(t); tmp=Image.new('RGBA',(Wd,H),(0,0,0,0)); tmp.alpha_composite(im,(px,py)); a=np.asarray(tmp).astype(np.float32)/255
        acc[...,:3]+=a[...,:3]*a[...,3:4]; acc[...,3]+=a[...,3]
    cov=acc[...,3]/sub; rgb=acc[...,:3]/np.maximum(acc[...,3:4],1e-6); return rgb,np.clip(cov*1.6,0,1)
RAMP={1839:(1.02,3,2),1840:(1.10,7,4),1841:(1.19,11,7),1842:(1.29,17,10),1843:(1.34,21,13)}
prev_e=0.0
for i in range(N):
    k=K0+i; img=load(k); e=float(E[i])
    img=patch_trunk(img)
    rgb,a=layer(prev_e,e,shutter={1841:0.5,1842:0.6,1843:0.75}.get(k,0.4))
    if k in RAMP:
        g,lg,lb=RAMP[k]; rgb=np.clip(rgb*g+np.array([0,lg/255,lb/255]),0,1)
    if k==1843: a=a*(1-sapm)                           # damla yapragin onunde
    out=img*(1-a[...,None])+rgb*a[...,None]
    Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)).save(f'{OUT}/k{k:04d}.png')
    print(k,'konum',np.round(pos_e(e),1),'yer degistirme',round(float(np.linalg.norm(pos_e(e)-pos_e(prev_e))),1),'rot',round(rot_e(e),1)); prev_e=e
tiles=[]
for k in range(1832,1846):
    f=f'{OUT}/k{k:04d}.png' if 1834<=k<=1843 else f'{SRC}/k{k:04d}.png'
    tiles.append(Image.open(f).crop((600,150,1200,600)).resize((450,338),Image.LANCZOS))
sheet=Image.new('RGB',(450*7,338*2))
for i,im in enumerate(tiles): sheet.paste(im,((i%7)*450,(i//7)*338))
sheet.save(OUT+'/_serit.png'); print('serit hazir')
