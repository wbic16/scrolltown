#!/bin/bash
# Live-drawing session 03: unpack frames and assemble on aletheia-core
# (ranch-side, per animator skill section 3 — video assembly never runs on
# the Muse VM). Expects ~/frames-03.tar.gz beside this script.
set -e
cd ~
rm -rf live-drawing-03
mkdir -p live-drawing-03/frames
tar -xzf frames-03.tar.gz -C live-drawing-03/frames
cd live-drawing-03
ffmpeg -y -loglevel error -framerate 24 -i frames/frames-03/f%04d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart session-03.mp4
ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames session-03.mp4
sha256sum session-03.mp4
