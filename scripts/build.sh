#!/bin/zsh
# Final render + assembly.  usage: scripts/build.sh [jobs=3] [scene ids...]
cd "$(dirname "$0")/.."
JOBS=${1:-3}; shift 2>/dev/null
SCENES=(${@:-$(ls scenes | sed -n 's/^\(s[0-9][0-9]\)\.py$/\1/p')})
mkdir -p build/final build/logs
: > build/overruns.log
render() { s=$1; S=$(echo $s | tr a-z A-Z)
  .venv/bin/manim -r 1920,1080 --fps 30 --media_dir build/final/media scenes/$s.py $S > build/logs/$s.log 2>&1 \
    && echo "ok $s" || echo "FAILED $s (see build/logs/$s.log)"; }
for s in $SCENES; do
  while (( $(jobs -r | wc -l) >= JOBS )); do sleep 1; done
  render $s &
done; wait
# assemble: pad every scene's audio to its exact video length first, otherwise the concat drifts out of sync
mkdir -p build/final/norm; : > build/final/list.txt
for f in $(ls scenes | sed -n 's/^\(s[0-9][0-9]\)\.py$/\1/p'); do
  v=build/final/media/videos/$f/1080p30/$(echo $f | tr a-z A-Z).mp4
  [[ -f $v ]] || { echo "missing $f"; continue; }
  if [[ ! -f build/final/norm/$f.mov || $v -nt build/final/norm/$f.mov ]]; then
    d=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 $v)
    ffmpeg -v error -y -i $v -c:v copy -af "aresample=48000,apad" -c:a pcm_s16le -t $d build/final/norm/$f.mov
  fi
  echo "file '$PWD/build/final/norm/$f.mov'" >> build/final/list.txt
done
ffmpeg -v error -y -f concat -safe 0 -i build/final/list.txt -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" -c:a aac -b:a 192k -movflags +faststart build/riemann_hypothesis_explainer.mp4
ffprobe -v error -show_entries stream=codec_type,duration -of csv=p=0 build/riemann_hypothesis_explainer.mp4
cat build/overruns.log
