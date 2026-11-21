"""Contact sheet for visual QA.  usage: sheet.py s05 [n_frames=12] [t0 t1]   -> build/frames/s05_sheet.png
Picks the newest render of the scene (any quality). Frames run left-to-right, top-to-bottom; the printed line says the spacing."""
import sys, glob, os, subprocess, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sid = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
vids = sorted(glob.glob(f"{ROOT}/media/videos/{sid}/*/{sid.upper()}.mp4"), key=os.path.getmtime)
v = vids[-1]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v]))
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
t1 = float(sys.argv[4]) if len(sys.argv) > 4 else dur
cols = 3 if n <= 9 else 4
rows = -(-n // cols)
step = (t1 - t0) / n
os.makedirs(f"{ROOT}/build/frames", exist_ok=True)
out = f"{ROOT}/build/frames/{sid}_sheet.png"
vf = (f"fps=1/{step:.4f},scale=640:-1,"
      f"tile={cols}x{rows}:padding=4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0 + step / 2), "-t", str(t1 - t0), "-i", v, "-vf", vf, "-frames:v", "1", out], check=True)
print(out, f"({v.split('/')[-2]}, {dur:.1f}s, one frame every {step:.1f}s from {t0+step/2:.1f}s)")
