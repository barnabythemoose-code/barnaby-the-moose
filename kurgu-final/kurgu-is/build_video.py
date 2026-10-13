import subprocess, os, sys, json
sys.path.insert(0, os.path.dirname(__file__)); from edl import EDL
IS=sys.argv[1]; OUT=sys.argv[2]; os.makedirs(OUT+'/seg', exist_ok=True)
ENC=['-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-r','24','-an']
def run(c): subprocess.run(c, check=True)
segs=[]
for i,(ad,src,a,b,gecis,_,_) in enumerate(EDL):
    out=f'{OUT}/seg/{i:02d}.mp4'
    if os.path.exists(out) and gecis!='punch' and src!='KART':
        n=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip())
        if n==b-a: segs.append(dict(i=i,ad=ad,src=src,a=a,b=b,gecis=gecis,dosya=out,kare=n)); print(i,ad,n,'kare (onbellek)',flush=True); continue
    if src=='KART':
        logo=IS+'/06-marka/barnaby-the-moose-logo.png'
        run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'color=c=0x0a1428:s=1280x720:r=24:d={(b-a)/24}','-loop','1','-t',str((b-a)/24),'-i',logo,
             '-filter_complex','[1:v]scale=420:-1,format=rgba,fade=t=in:st=0.3:d=0.9:alpha=1[l];[0:v][l]overlay=(W-w)/2:(H-h)/2:shortest=1,format=yuv420p',*ENC,out])
    else:
        vf=f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,scale=1280:720:flags=lanczos"
        if gecis=='punch':   # Anne punch-in: 0,25 sn'de 1,00 -> 1,18, Anne (x~%40, y~%55) merkezli
            vf+=",zoompan=z='1.18':x='max(0,min(iw-iw/zoom,512-iw/zoom/2))':y='max(0,min(ih-ih/zoom,396-ih/zoom/2))':d=1:s=1280x720:fps=24"
        run(['ffmpeg','-v','error','-y','-i',IS+'/'+src,'-vf',vf,*ENC,out])
    n=int(subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v','-show_entries','stream=nb_read_frames','-of','csv=p=0',out],capture_output=True,text=True).stdout.strip())
    segs.append(dict(i=i,ad=ad,src=src,a=a,b=b,gecis=gecis,dosya=out,kare=n)); print(i,ad,n,'kare',flush=True)
# birlestirme: xfade olan yerde onceki segmentle birlestir, aksi halde concat
cur=segs[0]['dosya']; tl=[]; t=0
tl.append(dict(ad=segs[0]['ad'],t0=0.0,kare=segs[0]['kare'],gecis='acilis')); t=segs[0]['kare']
for s in segs[1:]:
    g=s['gecis']
    if isinstance(g,tuple) and g[0]=='xfade':
        xf=g[1]; prev_len=t
        nxt=f"{OUT}/seg/x{s['i']:02d}.mp4"
        run(['ffmpeg','-v','error','-y','-i',cur,'-i',s['dosya'],'-filter_complex',f"[0:v][1:v]xfade=transition=fade:duration={xf/24}:offset={(prev_len-xf)/24}",*ENC,nxt])
        cur=nxt; tl.append(dict(ad=s['ad'],t0=(t-xf)/24,kare=s['kare'],gecis=f'xfade {xf} kare')); t=t-xf+s['kare']
    else:
        nxt=f"{OUT}/seg/c{s['i']:02d}.mp4"
        lst=f"{OUT}/seg/l{s['i']:02d}.txt"; open(lst,'w').write(f"file '{os.path.abspath(cur)}'\nfile '{os.path.abspath(s['dosya'])}'\n")
        run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',lst,'-c','copy',nxt])
        cur=nxt; tl.append(dict(ad=s['ad'],t0=t/24,kare=s['kare'],gecis='kesme' if g!='punch' else 'punch-in (ayni plan)')); t+=s['kare']
os.replace(cur, OUT+'/video_raw.mp4')
for x in tl: x['t1']=round(x['t0']+x['kare']/24,3); x['t0']=round(x['t0'],3)
json.dump(dict(toplam_kare=t,toplam_sn=t/24,timeline=tl,segs=segs),open(OUT+'/timeline.json','w'),ensure_ascii=False,indent=1)
print('TOPLAM',t,'kare',round(t/24,3),'sn')
