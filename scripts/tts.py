"""Generate one WAV per beat with Kokoro. Usage: tts.py [voice] [speed]  -> build/audio/<key>.wav + build/durations.json"""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, soundfile as sf
import espeakng_loader
espeakng_loader.get_library_path = lambda: '/opt/homebrew/lib/libespeak-ng.dylib'
espeakng_loader.get_data_path = lambda: '/opt/homebrew/share/espeak-ng-data'
from kokoro import KPipeline
from script import beats

voice = sys.argv[1] if len(sys.argv) > 1 else "af_heart"
speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
only = set(sys.argv[3:])
PRON = {"Alpöge": "Alpurgay", "Weil": "Vay", "Dirichlet": "Dirishlay"}
SR = 24000
pipe = KPipeline(lang_code=voice[0], repo_id="hexgrad/Kokoro-82M")
os.makedirs("build/audio", exist_ok=True)
dpath = "build/durations.json"
durs = json.load(open(dpath)) if os.path.exists(dpath) else {}

def trim(a, thr=0.004):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0: return a
    return a[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.12 * SR)]

for key, sc, b in beats():
    if only and key not in only and sc["id"] not in only: continue
    t = b["text"]
    for k, v in PRON.items(): t = t.replace(k, v)
    t = t.replace("'in the long run'", "in the long run").replace("'", "’") if False else t
    parts = []
    for r in pipe(t, voice=voice, speed=speed, split_pattern=r"\n+"):
        a = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        parts.append(trim(a)); parts.append(np.zeros(int(0.18 * SR), dtype=np.float32))
    a = np.concatenate(parts[:-1]).astype(np.float32)
    a = a / max(1e-6, np.abs(a).max()) * 0.89
    sf.write(f"build/audio/{key}.wav", a, SR)
    durs[key] = round(len(a) / SR, 3)
    print(key, durs[key], flush=True)
json.dump(durs, open(dpath, "w"), indent=0)
print("TOTAL", round(sum(durs.values()), 1), "s", "voice", voice)
