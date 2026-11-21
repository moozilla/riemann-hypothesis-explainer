import sys, espeakng_loader
espeakng_loader.get_library_path=lambda: '/opt/homebrew/lib/libespeak-ng.dylib'
espeakng_loader.get_data_path=lambda: '/opt/homebrew/share/espeak-ng-data'
from kokoro import KPipeline
p = KPipeline(lang_code='a', repo_id="hexgrad/Kokoro-82M", model=False)
for w in sys.argv[1:]:
    for r in p(w): print(w, '->', r.phonemes)
