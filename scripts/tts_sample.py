import sys, soundfile as sf, numpy as np
import espeakng_loader
espeakng_loader.get_library_path=lambda: '/opt/homebrew/lib/libespeak-ng.dylib'
espeakng_loader.get_data_path=lambda: '/opt/homebrew/share/espeak-ng-data'
from kokoro import KPipeline
text = ("Pick a number. Any number. Is it prime? For small numbers, you can just check. "
        "But zoom out, and something strange happens. The primes look random up close, "
        "and yet, from far away, they follow a curve so smooth you could draw it with a ruler. "
        "The Riemann hypothesis is a claim about exactly how random the primes are allowed to be. "
        "And after one hundred and sixty seven years, it appears to have fallen.")
pipes = {}
for voice in sys.argv[1:]:
    lang = voice[0]
    if lang not in pipes: pipes[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
    chunks = [a for _,_,a in pipes[lang](text, voice=voice, speed=1.0)]
    sf.write(f"tts_samples/kokoro_{voice}.wav", np.concatenate(chunks), 24000)
    print("wrote", voice)
