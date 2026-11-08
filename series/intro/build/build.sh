#!/usr/bin/env bash
# Assemble the Scrolltown intro master from clips + stills, per LYRICS.md time map (90s total).
set -euo pipefail
cd "$(dirname "$0")/.."
B=build
CLIPS=clips
STILLS=stills
SERIF=/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf
SANS=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf
C1=$(ls $CLIPS/*clip1*.mp4)   # kid montage
C2=$(ls $CLIPS/*clip2*.mp4)   # keeping the town
C3=$(ls $CLIPS/*clip3*.mp4)   # code night
C4=$(ls $CLIPS/*clip4*.mp4)   # hay dawn
C5=$(ls $CLIPS/*clip5*.mp4)   # phext ignition
C6=$(ls $CLIPS/*clip6*.mp4)   # decades
P7=$(ls $STILLS/*still7*.webp) # planet lattice
P8=$(ls $STILLS/*still8*.webp) # horizon 2100
ENC="-an -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30"

seg () { # input-file, extra-vf, target-duration, out-name
  local fost; fost=$(awk -v d="$3" 'BEGIN{printf "%.2f", d-0.45}')
  ffmpeg -y -v error -i "$1" -vf "scale=1280:720:flags=lanczos,$2,fade=t=in:st=0:d=0.45,fade=t=out:st=${fost}:d=0.45,format=yuv420p" -t "$3" $ENC "$B/$4"
}
# S1-S3, S5-S6: 10s clips gently slowed to 11s; S4 hay stays 10s.
seg "$C1" "setpts=1.1*PTS"        11 seg1.mp4
seg "$C2" "setpts=1.1*PTS"        11 seg2.mp4
seg "$C3" "setpts=1.1*PTS"        11 seg3.mp4
seg "$C4" "setpts=1.0*PTS"        10 seg4.mp4
seg "$C5" "setpts=1.1*PTS"        11 seg5.mp4
# S6 decades + year markers (lower corner, warm cream type)
seg "$C6" "setpts=1.1*PTS,drawtext=fontfile=$SANS:fontsize=34:fontcolor=0xFFFBF0:box=1:boxcolor=0x2C2019@0.45:boxborderw=12:x=36:y=h-84:text='2030':enable='between(t,0.3,3.8)',drawtext=fontfile=$SANS:fontsize=34:fontcolor=0xFFFBF0:box=1:boxcolor=0x2C2019@0.45:boxborderw=12:x=36:y=h-84:text='2050':enable='between(t,3.9,7.4)',drawtext=fontfile=$SANS:fontsize=34:fontcolor=0xFFFBF0:box=1:boxcolor=0x2C2019@0.45:boxborderw=12:x=36:y=h-84:text='2080':enable='between(t,7.5,10.8)'" 11 seg6.mp4
# S7 planet: still, slow majestic push-in, 12s (360 frames)
ffmpeg -y -v error -i "$P7" -vf "zoompan=z='1+0.13*on/360':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=360:s=1280x720:fps=30,fade=t=in:st=0:d=0.45,fade=t=out:st=11.55:d=0.45,format=yuv420p" -frames:v 360 $ENC $B/seg7.mp4
# S8a horizon: still, slow rise toward the bright region (not reached), 7s (210 frames)
ffmpeg -y -v error -i "$P8" -vf "zoompan=z='1.08+0.14*on/210':x='iw/2-(iw/zoom/2)':y='max(0,(ih-ih/zoom)/2 - on*1.1)':d=210:s=1280x720:fps=30,fade=t=in:st=0:d=0.45,fade=t=out:st=6.55:d=0.45,format=yuv420p" -frames:v 210 $ENC $B/seg8.mp4
# Cards on cream: 2100 (2s) / thirty years to go. (2s) / SCROLLTOWN title (2s, no fade-out: title is the final frame)
card () { # text, fontsize, duration, out, fadeout(0/1)
  local fo=""; [ "$5" = "1" ] && fo=",fade=t=out:st=$(awk -v d="$3" 'BEGIN{printf "%.2f", d-0.4}'):d=0.4"
  ffmpeg -y -v error -f lavfi -i "color=0xFFFBF0:s=1280x720:r=30:d=$3" -vf "drawtext=fontfile=$SERIF:fontsize=$2:fontcolor=0x46332A:text='$1':x=(w-text_w)/2:y=(h-text_h)/2,fade=t=in:st=0:d=0.4$fo,format=yuv420p" -t "$3" $ENC "$B/$4"
}
card "2100"                  150 2 card2100.mp4 1
card "thirty years to go."    56 2 card30.mp4 1
card "S C R O L L T O W N"  68 2 title.mp4 0

# Concat (all segments share codec/params)
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\nfile 'seg6.mp4'\nfile 'seg7.mp4'\nfile 'seg8.mp4'\nfile 'card2100.mp4'\nfile 'card30.mp4'\nfile 'title.mp4'\n" > $B/list.txt
ffmpeg -y -v error -f concat -safe 0 -i $B/list.txt -c copy intro-video.mp4
# Small download encode
ffmpeg -y -v error -i intro-video.mp4 -vf scale=854:480 -an -c:v libx264 -preset medium -crf 26 -pix_fmt yuv420p -movflags +faststart intro-video-small.mp4
echo "MASTER + SMALL DONE"
