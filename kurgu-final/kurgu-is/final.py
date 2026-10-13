# Final kodlama: video_raw + miks -> teslim mp4 (CRF 17 High yuv420p 24p, AAC 192k 48k, faststart); >15 Y sicramali kesimlerde 0,5 sn pozlama yumusatma (sendcmd+eq)
import json,subprocess,sys
IS=sys.argv[1]; T=sys.argv[2]
rows=json.load(open(IS+'/out/kesim-Y.json'))
cmds=[]
for a,b,t,d in rows:
    if abs(d)<=15 or b=='Son kart': continue
    amp=-0.06 if d>0 else 0.06      # gelen klip daha parlaksa karart, karanliksa aydinlat; 6 adimda sifira
    for k in range(6):
        cmds.append(f"{t+k/12:.4f} eq brightness {amp*(1-k/5):.4f};")
    cmds.append(f"{t+0.5:.4f} eq brightness 0;")
open(IS+'/out/eq_cmd.txt','w').write('\n'.join(cmds)+'\n')
vf="format=yuv420p"   # parlaklik rampalari kaldirildi (Owner: kayma hissi)
for ad,name in (('B','B090-TG-FINAL-B-efektli.mp4'),('A','B090-TG-FINAL-A-efektsiz.mp4')):
    subprocess.run(['ffmpeg','-v','error','-y','-i',IS+'/out/video_raw.mp4','-i',IS+f'/out/mix{ad}.wav','-map','0:v','-map','1:a','-vf',vf,'-r','24','-c:v','libx264','-preset','medium','-crf','17','-profile:v','high','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-movflags','+faststart','-shortest',T+'/'+name],check=True)
    print('ok',name)
