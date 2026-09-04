import numpy as np
from scipy.io import wavfile
import io
import requests

fs = 16000
t = np.linspace(0, 1.0, fs, endpoint=False)
# a short chirp + spike
sig = 0.1 * np.sin(2*np.pi*440*t)
sig[2000:2010] += 0.9  # short spike
buf = io.BytesIO()
wavfile.write(buf, fs, (sig * 32767).astype('int16'))
buf.seek(0)
files = {'audio': ('test.wav', buf, 'audio/wav')}
try:
    r = requests.post('http://127.0.0.1:5000/analyze', files=files, timeout=10)
    print('STATUS', r.status_code)
    print(r.text[:2000])
except Exception as e:
    print('ERROR', e)
