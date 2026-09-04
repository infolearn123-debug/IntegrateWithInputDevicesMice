from flask import Flask, render_template, request, jsonify
import io
import datetime
import base64
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.io import wavfile
import os

app = Flask(__name__)


def analyze_bytes(wav_bytes, state):
    buf = io.BytesIO(wav_bytes)
    sr, samples = wavfile.read(buf)

    # Ensure float32
    if samples.dtype.kind in ('i', 'u'):
        # integer -> normalize
        maxv = np.iinfo(samples.dtype).max
        samples = samples.astype(np.float32) / float(maxv)

    if samples.ndim > 1:
        samples = samples.mean(axis=1)

    # Short-time energy
    frame_len = int(0.02 * sr) or 1
    hop = max(1, frame_len // 2)
    squared = samples ** 2
    window = np.ones(frame_len)
    energy = np.convolve(squared, window, mode="valid") / frame_len
    times = np.arange(len(energy)) * (hop / sr)

    peak = float(np.max(energy))
    mean_e = float(np.mean(energy))
    std_e = float(np.std(energy))
    score = (peak - mean_e) / (std_e + 1e-9)
    threshold = mean_e + 2.5 * std_e
    is_spike = peak > threshold

    f, t, Sxx = signal.spectrogram(samples, fs=sr, nperseg=1024, noverlap=512)

    fig, axes = plt.subplots(3, 1, figsize=(6, 8))
    ax = axes[0]
    times_wave = np.arange(len(samples)) / sr
    ax.plot(times_wave, samples, color="C0")
    ax.set_ylabel("Amplitude")
    ax.set_xlim(0, times_wave[-1])

    ax = axes[1]
    ax.plot(times[: len(energy)], energy, color="C1")
    ax.axhline(threshold, color="r", linestyle="--", label="threshold")
    ax.set_ylabel("Energy")
    ax.legend()

    ax = axes[2]
    im = ax.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-12), shading="auto")
    fig.colorbar(im, ax=ax, format="%+2.0f dB")
    ax.set_ylabel("Freq [Hz]")
    ax.set_xlabel("Time [s]")

    plt.tight_layout()
    out_buf = io.BytesIO()
    fig.savefig(out_buf, format="png")
    plt.close(fig)
    out_buf.seek(0)

    alert = "SPIKE" if is_spike else "No spike"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    event = f"{timestamp} | score={score:.2f} | peak={peak:.6f} | {alert}"
    state = state or []
    state = [event] + state[:199]
    log_text = "\n".join(state)

    img_b64 = base64.b64encode(out_buf.getvalue()).decode('ascii')

    return img_b64, f"{alert} (score {score:.2f})", log_text, state


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_route():
    # Expect file field 'audio' containing WAV bytes
    f = request.files.get('audio')
    if not f:
        return jsonify({'error': 'no audio provided'}), 400
    wav_bytes = f.read()
    # simple in-memory state persisted per-process (demo only)
    state = request.form.get('state', '')
    state_list = state.split('\n') if state else []

    img_b64, alert, log_text, new_state = analyze_bytes(wav_bytes, state_list)
    return jsonify({'image_base64': img_b64, 'alert': alert, 'log': log_text})


@app.route('/snapshot', methods=['POST'])
def snapshot_route():
    # Accept an image file (field name 'snapshot') and save it with timestamp
    f = request.files.get('snapshot')
    if not f:
        return jsonify({'error': 'no snapshot provided'}), 400
    snapshots_dir = os.path.join(os.path.dirname(__file__), 'snapshots')
    os.makedirs(snapshots_dir, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    filename = f'snapshot_{ts}.png'
    path = os.path.join(snapshots_dir, filename)
    f.save(path)
    return jsonify({'saved': filename})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
