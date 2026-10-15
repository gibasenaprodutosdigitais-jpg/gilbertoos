#!/bin/bash
set -e
cd "$(dirname "$0")"
FPS=30
TOTAL=599.095

ffmpeg -y -loglevel error -i "audio/sc00.wav" -i "audio/sc01.wav" -i "audio/sc02.wav" -i "audio/sc03.wav" -i "audio/sc04.wav" -i "audio/sc05.wav" -i "audio/sc06.wav" -i "audio/sc07.wav" -i "audio/sc08.wav" -i "audio/sc09.wav" -i "audio/sc10.wav" -i "audio/sc11.wav" -i "audio/sc12.wav" -i "audio/sc13.wav" -i "audio/sc14.wav" -i "audio/sc15.wav" -i "audio/sc16.wav" -i "audio/sc17.wav" -i "audio/sc18.wav" -i "audio/sc19.wav" -i "audio/sc20.wav" \
  -filter_complex "[0]adelay=500|500[a0];[1]adelay=20520|20520[a1];[2]adelay=46090|46090[a2];[3]adelay=62050|62050[a3];[4]adelay=91258|91258[a4];[5]adelay=123821|123821[a5];[6]adelay=155269|155269[a6];[7]adelay=184605|184605[a7];[8]adelay=215995|215995[a8];[9]adelay=236098|236098[a9];[10]adelay=255274|255274[a10];[11]adelay=294013|294013[a11];[12]adelay=324416|324416[a12];[13]adelay=369866|369866[a13];[14]adelay=404461|404461[a14];[15]adelay=424018|424018[a15];[16]adelay=453502|453502[a16];[17]adelay=475534|475534[a17];[18]adelay=500933|500933[a18];[19]adelay=535272|535272[a19];[20]adelay=565571|565571[a20];[a0][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][a11][a12][a13][a14][a15][a16][a17][a18][a19][a20]amix=inputs=21:normalize=0,dynaudnorm=p=0.7:s=6,alimiter=limit=0.95[mix]" -map "[mix]" -t $TOTAL -ar 48000 -ac 2 audio/mix.wav

ffmpeg -y -loglevel error -framerate $FPS -start_number 0 -i frames/f-%05d.png \
  -i audio/mix.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \
  -c:a aac -b:a 192k -movflags +faststart -shortest \
  "Estudo - Reengenharia Empresarial (mapa executivo).mp4"

echo "OK -> Estudo - Reengenharia Empresarial (mapa executivo).mp4"
