#!/bin/bash
set -e
cd "$(dirname "$0")"
FPS=30
TOTAL=78.825

# --- cama musical sutil (la2 + mi3, filtrada, baixa) ---
ffmpeg -y -loglevel error \
  -f lavfi -i "sine=frequency=110:sample_rate=48000" \
  -f lavfi -i "sine=frequency=164.81:sample_rate=48000" \
  -f lavfi -i "sine=frequency=220:sample_rate=48000" \
  -filter_complex "[0][1][2]amix=inputs=3,tremolo=f=0.13:d=0.4,lowpass=f=380,\
highpass=f=60,volume=0.05,aecho=0.8:0.6:70:0.25,afade=t=in:d=1.5,afade=t=out:st=$(echo "$TOTAL-2"|bc):d=2" \
  -t $TOTAL -ac 2 -ar 48000 audio/bed.wav

# --- mistura locucao + cama ---
ffmpeg -y -loglevel error -i audio/bed.wav -i "audio/intro.wav" -i "audio/s01.wav" -i "audio/s02.wav" -i "audio/s03.wav" -i "audio/s04.wav" -i "audio/s05.wav" -i "audio/s06.wav" -i "audio/s07.wav" -i "audio/s08.wav" -i "audio/s09.wav" -i "audio/s10.wav" -i "audio/close.wav" \
  -filter_complex "[1]adelay=450|450[a1];[2]adelay=6982|6982[a2];[3]adelay=14073|14073[a3];[4]adelay=20376|20376[a4];[5]adelay=26851|26851[a5];[6]adelay=33782|33782[a6];[7]adelay=40933|40933[a7];[8]adelay=47564|47564[a8];[9]adelay=53018|53018[a9];[10]adelay=59530|59530[a10];[11]adelay=65254|65254[a11];[12]adelay=72045|72045[a12];[0]volume=0.9[bed];[bed][a1][a2][a3][a4][a5][a6][a7][a8][a9][a10][a11][a12]amix=inputs=13:normalize=0,dynaudnorm=p=0.6:s=6,alimiter=limit=0.94[mix]" -map "[mix]" -t $TOTAL -ar 48000 -ac 2 audio/mix.wav

# --- encode final ---
ffmpeg -y -loglevel error -framerate $FPS -start_number 0 -i frames/f-%05d.png \
  -i audio/mix.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow \
  -c:a aac -b:a 192k -movflags +faststart -shortest \
  "Apresentacao 10 e-books - Gilberto Sena.mp4"

echo "OK -> Apresentacao 10 e-books - Gilberto Sena.mp4"
