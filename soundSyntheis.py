import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

'''
# Define Harman curve frequency response
f = np.array([20, 40, 210, 1000, 3000, 9000, 20000])
h = np.array([ 4,  4,  -3,    0,   10,    1,   -20])



# Generate random noise signa
duration = 5 # 5 seconds of noise
fs = 44100 # 44100 Hz sampling rate
samples = int(fs * duration)
noise = np.random.randn(samples)

# Interpolate Harman curve frequency response
freqs = np.fft.fftfreq(samples, d=1/fs)
interp_h = np.interp(np.log10(freqs[freqs > 0]), np.log10(f), h)
harman_response = np.zeros(samples)
harman_response[freqs > 0] = 10**(interp_h/20) # convert dB to linear scale
harman_response[0] = 0 # avoid DC component gain

# Apply Harman curve frequency response to noise signal PSD
noise_psd = np.abs(np.fft.fft(noise))**2 / samples
harman_psd = noise_psd * harman_response**2

# Apply inverse FFT to obtain Harman curve noise signal
noise_harman = np.real(np.fft.ifft(np.sqrt(harman_psd) * np.exp(1j*np.angle(np.fft.fft(noise)))))

# Save Harman curve noise signal as WAV file
scaled = np.int16(noise_harman/np.max(np.abs(noise_harman)) * 32767)
wavfile.write('harman_noise.wav', fs, scaled)

# Plot the resulting noise signal and its spectrum
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(np.linspace(0, duration, samples), noise_harman)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax2.semilogx(freqs[freqs > 0], 10*np.log10(harman_psd[freqs > 0]))
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Power (dB)')
# grid
ax1.grid()
ax2.grid()
ax2.set_xlim([20, 20000])
ax2.set_ylim([-15, 20])
plt.show()
'''

# package it by class
class NoiseGenerator:
    def __init__(self, duration=5, sampleRate=384000, *args, **kwargs):
        super().__init__()
        self.__duration = duration
        self.__sampleRate = sampleRate
        self.__result = None
        self.__sample = int(sampleRate * duration)
        self.__noise = np.random.randn(self.__sample)
        self.f = np.array([20, 40, 210, 1000, 3000, 9000, 20000, 40000])
        self.h = np.array([4, 4, -3, 0, 10, 1, -20, -80])
        # checking **kwargs to reverse the curve
        if 'reverse' in kwargs:
            if kwargs['reverse'] == True:
                self.h = -self.h

    def freqAndGain(self, freq, gain):
        # freq: in Hz
        # gain: in dB
        # returns: nothing
        # set the frequency response
        # x axis: frequency
        # y axis: gain
        _pass = 0
        try:
            newGain = np.array(gain)
            newFreq = np.array(freq)
            _pass = 1
        except:
            print("Error: freqAndGain(freq, gain)")

        if _pass == 1:
            self.f = newGain
            self.h = newFreq

    def __interpolate(self):
        self.freqs = np.fft.fftfreq(self.__sample, d=1 / self.__sampleRate)
        self.interp_h = np.interp(np.log10(self.freqs[self.freqs > 0]), np.log10(self.f), self.h)
        self.harman_response = np.zeros(self.__sample)
        self.harman_response[self.freqs > 0] = 10 ** (self.interp_h / 20)  # convert dB to linear scale
        self.harman_response[0] = 0  # avoid DC component gain

    def __apply(self):
        self.noise_psd = np.abs(np.fft.fft(self.__noise)) ** 2 / self.__sample
        self.harman_psd = self.noise_psd * self.harman_response ** 2
        self.noise_harman = np.real(np.fft.ifft(np.sqrt(self.harman_psd) * np.exp(1j * np.angle(np.fft.fft(self.__noise)))))
        self.__result = self.noise_harman

    def generate(self):
        self.__interpolate()
        self.__apply()
        return self.__result

    def saveWav(self):
        try:
            #remove old file
            os.remove('noise.wav')
        except:
            pass
        scaled = np.int16(self.__result / np.max(np.abs(self.__result)) * 32767)
        wavfile.write('noise.wav', self.__sampleRate, scaled)

    def plot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(np.linspace(0, self.__duration, self.__sample), self.__result)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax2.semilogx(self.freqs[self.freqs > 0], 10 * np.log10(self.harman_psd[self.freqs > 0]))
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Power (dB)')
        # grid
        ax1.grid()
        ax2.grid()
        ax2.set_xlim([20, 20000])
        ax2.set_ylim([-15, 20])
        plt.show()

if __name__ == '__main__':
    noise = NoiseGenerator(reverse=True)
    noise.generate()
    noise.saveWav()
    noise.plot()