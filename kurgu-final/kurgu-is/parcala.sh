#!/bin/bash
# master_video_crf14.mov (video) + out/mixB.wav -> 20 sn'lik MOV parcalar (H.264 kopya + PCM 24 bit, ornek-hassas ses dilimi)
set -e
Y=/tmp/claude-0/-home-user-barnaby-the-moose/092a3a41-7dca-5bb2-96ae-2443fc1a8e4e/scratchpad/kurgu/yeni
M=$Y/master; cd $M; rm -rf parca; mkdir -p parca
ffmpeg -v error -y -i master_video_crf14.mov -an -c:v copy -f segment -segment_time 20 -reset_timestamps 1 -segment_start_number 1 parca/_v_%02d.mov
i=0; acc=0
for f in parca/_v_*.mov; do
  n=$(basename $f .mov | sed 's/_v_//'); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)
  fr=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $f)
  ffmpeg -v error -y -i $f -i $Y/out/mixB.wav -filter_complex "[1:a]atrim=start=${acc}:duration=${d},asetpts=PTS-STARTPTS[a]" -map 0:v -map "[a]" -c:v copy -c:a pcm_s24le -ar 48000 -ac 2 -movflags +faststart "parca/B090-TG-FINAL-v24-part${n}.mov"
  echo "part$n baslangic=${acc} sure=${d} kare=${fr}"
  acc=$(python3 -c "print(round($acc+$d,6))")
done
rm -f parca/_v_*.mov; ls -la parca/ | awk '{print $5,$9}'
