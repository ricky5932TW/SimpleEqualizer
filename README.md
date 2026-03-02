# SimpleEqualizer 🎚️

Welcome to **SimpleEqualizer** - your ultimate tool for adjusting your built-in equalizer on PCs, especially useful for car audio systems! This project is all about enhancing your audio experience by providing an easy way to fine-tune your stereo system.

## Features 🌟

- **Quick EQ Adjustments**: Say goodbye to the tedious process of EQ settings adjustment.
- **Persistent Settings**: Our solution helps your EQ settings stay intact through Windows updates.
- **User-Friendly Interface**: Utilizing a combination of Python, Flask, HTML, CSS, and JavaScript for a seamless experience.
- **Hardware Compatibility**: Works best with quality hardware for accurate adjustments.

## Installation Guide 🛠️

This section guides you through the setup process to get this project up and running on your system.

### Using an Integrated Development Environment (IDE)

1. **Clone the Repository**
   - Open your preferred IDE and use the clone repository feature.
   - Enter the URL: `https://github.com/ricky5932TW/SimpleEqualizer`
   - Choose the directory where you wish to save the project.

2. **Install Dependencies**
   - Navigate to the project folder and locate the `requirements.txt` file.
   - Execute the following command in your IDE's terminal or command prompt: `pip install -r requirements.txt`

3. **Run the Project**
   - Ensure all dependencies are installed without errors.
   - Open and run the project code through your IDE.
   - Start the application by running `web_gui.py` to launch the web interface.

### Using Command Line Interface (CLI)

1. **Clone the Repository**
   - Open your command line interface (CLI) and enter: `git clone https://github.com/ricky5932TW/SimpleEqualizer`
   - Change to the project directory: `cd SimpleEqualizer`

2. **Install Dependencies**
   - Within the project directory, execute: `pip install -r requirements.txt`

3. **Run the Project**
   - After installing all dependencies, start the application by running:
     ```
     python web_gui.py
     ```
   - This will launch the web interface.

---

## Program Structure 📁

```
SimpleEqualizer/
├── web_gui.py              # Flask web application entry point; defines all HTTP routes
├── measurement.py          # MeasurementService class; bridges web requests to core logic
├── scripts.py              # SimpleEqualizer facade class; orchestrates measurement workflows
├── requirements.txt        # Python dependency list
│
├── package/                # Core reusable packages
│   ├── soundAnalyze/       # Audio analysis module
│   │   └── soundAnalyze.py     # SoundAnalyzer class: recording, FFT, and data export
│   ├── tuningInstructor/   # EQ tuning instruction generator
│   │   └── tuningInstructor.py # TuningInstructor class: computes per-band gain adjustments
│   ├── soundSynthesis/     # Noise/signal generation module
│   │   └── soundSynthesis.py   # NoiseGenerator class: shaped noise WAV file generator
│   ├── sweepGenerator/     # Sweep signal generator
│   │   └── sweepGenerator.py   # SweepSignalGenerator class: logarithmic chirp generator
│   └── sweep_with_EqualLoudness/ # Equal-loudness sweep generator
│       └── sweep_with_EqualLoudness.py
│
├── scripts/                # Standalone runner scripts for manual use
│   ├── scripts.py          # SimpleEqualizer facade (scripts-folder path variant)
│   ├── analyze_with_optimize.py
│   ├── analyze_without_optimize.py
│   ├── instructor.py
│   ├── white_noise_test.py
│   ├── TxtOp.py            # Simple text file read/write utility
│   └── old_file/           # Archived legacy scripts
│
├── templates/              # Jinja2 HTML templates (served by Flask)
│   ├── index.html          # Main navigation page
│   ├── full.html           # Full-band correction page
│   ├── limited.html        # Limited-band correction page
│   └── white_noise_test.html
│
├── static/                 # Static web assets
│   ├── style.css           # Stylesheet
│   ├── script.js           # Front-end JavaScript (polling, form submission)
│   ├── status.txt          # Runtime status updated by the server
│   └── icon.webp           # App icon
│
├── soundFile/              # Input WAV files used during measurement
│   ├── noise.wav           # Shaped noise test signal
│   ├── whiteNoise.wav      # White noise test signal
│   ├── sweep_signal.wav    # Logarithmic sweep signal
│   └── record.wav          # Microphone recording output (runtime)
│
├── data/                   # CSV output from measurements
│   ├── rawData.csv         # Full-spectrum frequency response data
│   ├── separateData.csv    # Per-band gain data
│   └── 1000HzGain.txt      # 1 kHz reference gain value
│
├── temp_img/               # Temporary plot images served to the browser
│   ├── full.png            # Full-spectrum frequency response plot
│   └── Spectrum.png        # White-noise spectrum plot
│
├── result/                 # Historical measurement result images
└── uml/                    # UML diagrams of the system architecture
```

### Key Classes and Responsibilities

| Class | File | Responsibility |
|---|---|---|
| `SoundAnalyzer` | `package/soundAnalyze/soundAnalyze.py` | Records audio, computes FFT, exports CSV data |
| `TuningInstructor` | `package/tuningInstructor/tuningInstructor.py` | Computes per-band EQ gain instructions from measured data |
| `NoiseGenerator` | `package/soundSynthesis/soundSynthesis.py` | Generates shaped noise WAV files for playback |
| `SweepSignalGenerator` | `package/sweepGenerator/sweepGenerator.py` | Generates logarithmic sweep (chirp) WAV files |
| `SimpleEqualizer` | `scripts.py` | High-level facade; orchestrates record → analyze → export workflows |
| `MeasurementService` | `measurement.py` | Static service layer called by the Flask routes |

### Request Flow

```
Browser → Flask (web_gui.py)
            └─→ MeasurementService (measurement.py)
                    └─→ SimpleEqualizer (scripts.py)
                            ├─→ SoundAnalyzer   (play_and_record → fft → saveRawData)
                            └─→ TuningInstructor (loadCSV → printInstruction)
```

---

## Technology Stack 🛠️

| Layer | Technology | Purpose |
|---|---|---|
| **Web Framework** | [Flask](https://flask.palletsprojects.com/) | HTTP routing, template rendering, REST-like API |
| **Front-end** | HTML5 / CSS3 / JavaScript | UI pages and status polling |
| **Template Engine** | Jinja2 (bundled with Flask) | Dynamic HTML rendering |
| **Audio Playback** | [Pygame](https://www.pygame.org/) (`pygame.mixer`) | Low-latency WAV file playback |
| **Audio Recording** | [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) | PCM microphone capture at 384 kHz |
| **Signal Processing** | [SciPy](https://scipy.org/) (`scipy.signal`, `scipy.io.wavfile`) | FFT smoothing (Savitzky-Golay), WAV I/O, digital filters |
| **Numerical Computing** | [NumPy](https://numpy.org/) | Array operations, FFT, frequency axis calculation |
| **Data Storage** | [Pandas](https://pandas.pydata.org/) | CSV read/write for frequency-response data |
| **Plotting** | [Matplotlib](https://matplotlib.org/) | Frequency-response spectrum images |
| **Concurrency** | `multiprocessing` / `threading` (stdlib) | Simultaneous playback and recording |
| **Language** | Python 3.8+ | Core application language |

