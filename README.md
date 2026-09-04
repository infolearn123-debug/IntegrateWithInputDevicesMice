---
sdk: gradio
app_file: app.py
--- 

# Microphone Spike Detector

Simple Gradio app that captures microphone audio, computes short-time energy
and a spectrogram, and raises spike alerts when the energy exceeds a threshold.

Live demo: (deploy this repository to a Hugging Face Space with `sdk: gradio`)

How to run locally

1. Create a virtual environment and activate it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

Local setup (recommended)

This project is tested with Python 3.10. If you have a newer system Python (for
example 3.13) you may encounter wheel/build errors for packages like `numpy`.
Follow these steps on Windows to create a Python 3.10 virtual environment and
run the app:

```powershell
# Install Python 3.10 from https://www.python.org/downloads/ if you don't have it
# Create a venv with the 3.10 interpreter (uses the py launcher)
py -3.10 -m venv .venv
. .venv\Scripts\Activate.ps1    # PowerShell
# or use: .venv\Scripts\activate for cmd.exe
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python app.py
```

If you prefer conda you can create a conda env instead:

```powershell
conda create -n mic-spike python=3.10 -y
conda activate mic-spike
pip install -r requirements.txt
python app.py
```


What it uses

- `gradio` for the web UI
- `numpy`/`scipy` for signal processing
- `matplotlib` for visualization

How it works

On each user-captured audio clip the app computes a short-time energy
envelope and a spectrogram. A spike is raised when the energy peak exceeds
mean + 2.5 * std. This is a demo — treat it as a teaching example, not a
production detector.

Files of interest

- `app.py` — the Gradio application and DSP logic
- `requirements.txt` — pinned dependencies used to build the Space
- `.github/workflows/verify-and-deploy.yml` — CI verify + deploy pipeline template
