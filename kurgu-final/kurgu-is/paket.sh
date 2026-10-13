#!/bin/bash
# Teslim paketi: B090-final-kurgu.zip (stems FLAC) + 28 MB parcalar + onizleme
set -e
W=$1; cd $W
rm -f B090-final-kurgu.zip B090-final-kurgu.z[0-9]* 2>/dev/null || true
mkdir -p paket/teslim/stems paket/kurgu-is
cp teslim/B090-TG-FINAL-B-efektli.mp4 teslim/B090-TG-FINAL-A-efektsiz.mp4 teslim/RAPOR.md teslim/kontakt.jpg teslim/h23-sinir-sayfasi.jpg teslim/ses-log.csv paket/teslim/
cp teslim/stems-flac/*.flac paket/teslim/stems/
cp bin/*.py is/out/cues.json is/out/timeline.json is/out/olcum-ses.json is/out/olcum-final.json is/out/kesim-Y.json is/out/benzerlik-final.json is/out/stt-tam.json paket/kurgu-is/ 2>/dev/null || true
cp is/agiz/*.jpg paket/kurgu-is/ 2>/dev/null || true
cd paket && zip -q -r ../B090-final-kurgu.zip teslim kurgu-is && cd ..
ls -la B090-final-kurgu.zip
# 28 MB parcalar (zip -s): B090-final-kurgu-parca.zip + .z01..
rm -f B090-final-kurgu-parca.z* 2>/dev/null || true
cd paket && zip -q -r -s 28m ../B090-final-kurgu-parca.zip teslim kurgu-is && cd ..
ls -la B090-final-kurgu-parca.z*
# telefon onizleme (<= 28 MB)
ffmpeg -v error -y -i teslim/B090-TG-FINAL-B-efektli.mp4 -c:v libx264 -preset medium -crf 26 -vf scale=854:480 -c:a aac -b:a 128k -movflags +faststart teslim/B090-TG-FINAL-B-onizleme-480p.mp4
ls -la teslim/B090-TG-FINAL-B-onizleme-480p.mp4
