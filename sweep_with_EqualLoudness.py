import numpy as np
from scipy.io.wavfile import write
from scipy.signal import chirp, equal_loudness_contour

class SweepSignalGenerator:
    def __init__(self, sample_rate, duration):
        self.sample_rate = sample_rate
        self.duration = duration
        self.__sample = int(self.duration * self.sample_rate)
        self.__noise = self.__generate_sweep()

    def __generate_sweep(self):
        t = np.linspace(0, self.duration, self.__sample, endpoint=False)
        return chirp(t, f0=20, f1=20000, t1=self.duration, method='logarithmic')

    def __interpolate(self):
        # Generate equal loudness contour for the given sample rate and duration
        self.freqs = np.fft.rfftfreq(self.__sample, d=1 / self.sample_rate)
        self.elc_gains = equal_loudness_contour(self.freqs, phon_level=80)  # Example for 80 phons

    def __apply(self):
        noise_fft = np.fft.rfft(self.__noise)  # apply fft
        elc_fft = noise_fft * self.elc_gains  # apply equal loudness contour in frequency domain
        self.__result = np.fft.irfft(elc_fft, self.__sample)  # apply inverse fft

    def generate(self):
        self.__interpolate()
        self.__apply()
        return self.__result

# Parameters
sample_rate = 384000  # in Hz
duration = 3  # in seconds

# Generate the sweep signal
generator = SweepSignalGenerator(sample_rate, duration)
sweep_signal = generator.generate()

# Normalize the signal to prevent clipping
max_val = np.max(np.abs(sweep_signal))
normalized_signal = sweep_signal / max_val

# Save the signal as a .wav file
write('sweep_signal.wav', sample_rate, normalized_signal.astype(np.float32))

print("Sweep signal generated and saved as 'sweep_signal.wav'")