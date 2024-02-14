import numpy as np
from scipy.io.wavfile import write
from scipy.signal import chirp
from soundAnalyze import SoundAnalyzer


class SweepSignalGenerator:
    def __init__(self, sample_rate, duration, f, h):
        self.sample_rate = sample_rate
        self.duration = duration
        self.f = f  # Frequency points for the gain
        self.h = h  # Gain values in dB
        self.__sample = int(self.duration * self.sample_rate)
        self.__noise = self.__generate_sweep()

    def __generate_sweep(self):
        t = np.linspace(0, self.duration, self.__sample, endpoint=False)
        return chirp(t, f0=self.f[0], f1=self.f[-1], t1=self.duration, method='logarithmic')

    def __interpolate(self):
        self.freqs = np.fft.rfftfreq(self.__sample, d=1 / self.sample_rate)  # get the frequency
        self.interp_h = np.interp(np.log10(self.freqs), np.log10(self.f), self.h)  # interpolate gain curve
        self.harman_response = np.zeros(len(self.freqs))
        self.harman_response[:] = 10 ** (self.interp_h / 20)  # convert dB to linear scale

    def __apply(self):
        noise_fft = np.fft.rfft(self.__noise)  # apply fft
        harman_fft = noise_fft * self.harman_response  # apply gain curve in frequency domain
        self.__result = np.fft.irfft(harman_fft, self.__sample)  # apply inverse fft

    def generate(self):
        self.__interpolate()
        self.__apply()
        return self.__result

# Parameters
sample_rate = 384000  # in Hz
duration = 2.5  # in seconds
freqs = np.array([10, 20, 40, 210, 1000, 3000, 20000])
gains_db = np.array([2, 2, 2, -3, 0, 10, -20])
gains_db = -gains_db

# Generate the sweep signal
generator = SweepSignalGenerator(sample_rate, duration, freqs, gains_db)
sweep_signal = generator.generate()

# Normalize the signal to prevent clipping
max_val = np.max(np.abs(sweep_signal))
normalized_signal = sweep_signal / max_val

# Save the signal as a .wav file
write('sweep_signal.wav', sample_rate, normalized_signal.astype(np.float32))

# fft the signal
eqSYS_0 = SoundAnalyzer()
eqSYS_0.fft('sweep_signal.wav', plot=1)

print("Sweep signal generated and saved as 'sweep_signal.wav'")