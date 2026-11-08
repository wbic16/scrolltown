#!/usr/bin/env bash
# Synthesize a soft pad GUIDE track following the LYRICS.md section map and mux it onto the master.
# GUIDE ONLY — the sung master is Will's Suno render, which drops onto the same 90s map.
set -euo pipefail
cd "$(dirname "$0")/.."
B=build

# section plan: start(s) dur(s) freqs...
SECTIONS=(
  "0  11 146.83 185.00 220.00"        # S1 kid montage      -> D
  "11 11 196.00 246.94 293.66"        # S2 keeping the town -> G
  "22 11 123.47 146.83 185.00"        # S3 one lamp         -> Bm
  "33 10 196.00 246.94 293.66"        # S4 hay at dawn      -> G
  "43 11 110.00 138.59 164.81"        # S5 scroll by scroll -> A
  "54 11 123.47 146.83 185.00"        # S6 decades          -> Bm
  "65 12 146.83 185.00 220.00 293.66" # S7 planet chorus    -> D (fuller)
  "77 7  196.00 246.94 293.66"        # S8a 2100 horizon    -> G
  "84 6  110.00 138.59 164.81"        # S8b cards -> A, unresolved on purpose
)

args=(); filters=""; n=0
for s in "${SECTIONS[@]}"; do
  read -ra parts <<< "$s"
  start=${parts[0]}; dur=${parts[1]}
  outst=$(awk -v d="$dur" 'BEGIN{printf "%.2f", d-1.6}')
  delay=$(( start * 1000 ))
  for f in "${parts[@]:2}"; do
    args+=(-f lavfi -i "sine=frequency=${f}:duration=${dur}:sample_rate=44100")
    filters+="[${n}:a]volume=0.05,afade=t=in:st=0:d=1.6,afade=t=out:st=${outst}:d=1.6,adelay=${delay}:all=1[t${n}];"
    n=$((n+1))
  done
done
mix=""; for ((i=0;i<n;i++)); do mix+="[t${i}]"; done
filters+="${mix}amix=inputs=${n}:normalize=0,atrim=0:90,alimiter=limit=0.8[aout]"

ffmpeg -y -v error "${args[@]}" -filter_complex "$filters" -map "[aout]" $B/guide.wav
ffmpeg -y -v error -i intro-video.mp4 -i $B/guide.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 128k intro-video-guide.mp4
echo "GUIDE DONE"
