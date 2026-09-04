import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wf
import io
import requests
import sys

# Usage: python record_post_high_sr.py [device_index] [samplerate]
args = sys.argv[1:]
device = int(args[0]) if len(args) >= 1 else None
samplerate = int(args[1]) if len(args) >= 2 else 96000
duration = 5

print('Using device:', device)
print('Samplerate:', samplerate)
print('Duration (s):', duration)
try:
    if device is not None:
        sd.default.device = device
    sd.default.samplerate = samplerate
    sd.default.channels = 1
except Exception as e:
    print('Warning setting defaults:', e)

try:
    rec = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    print('Recording...')
    sd.wait()
    print('Done')
    samples = rec.squeeze()
    maxAmp = float(np.max(np.abs(samples)))
    print('Max amplitude:', maxAmp)
    # save wav
    wav_path = 'tools/last_record.wav'
    wf.write(wav_path, samplerate, (samples * 32767).astype('int16'))
    print('Saved', wav_path)
    # POST to server
    with open(wav_path, 'rb') as f:
        files = {'audio': ('capture.wav', f, 'audio/wav')}
        print('Posting to server...')
        r = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=30)
        print('Status', r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text[:1000])
except Exception as e:
    print('ERROR', e)
    raise
