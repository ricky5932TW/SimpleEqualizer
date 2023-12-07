# make white noise
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import pygame
import os


class SoundSynthesis:
    def __init__(self, *args, **kwargs):
        self.fileName = 'whiteNoise.wav'
        self.__deleteOldWav()

    def __deleteOldWav(self):
        # fileName: a string
        # returns: nothing
        # delete a wav file
        if os.path.exists(self.fileName):
            os.remove(self.fileName)

    def makeWhiteNoise(self, duration, sampleRate):
        # duration: in seconds
        # sampleRate: in Hz
        # returns: a numpy array of floats
        # make white noise
        # save as a wav file
        numSamples = int(duration * sampleRate)
        samples = np.random.normal(0, 1, numSamples)
        return samples

    def saveWav(self, samples, sampleRate):
        # samples: a numpy array of floats
        # sampleRate: in Hz
        # fileName: a string
        # returns: nothing
        # save as a wav file
        self.__deleteOldWav()
        wavfile.write(self.fileName, sampleRate, samples)

    def playWav(self, time=0):
        # fileName: a string
        # returns: nothing
        # play a wav file
        pygame.init()
        pygame.mixer.music.load(self.fileName)
        self.__timeCountDown(time)
        pygame.mixer.music.play()
        pygame.event.wait()

    def checkingWav(self):
        # fileName: a string
        # returns: nothing
        # check a wav file with fft
        # x axis: frequency
        # y axis: amplitude
        rate, data = wavfile.read(self.fileName)
        fft = np.fft.fft(data)
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.psd(data, Fs=rate, NFFT=1024, scale_by_freq=True, sides='default')
        plt.show()

    def __timeCountDown(self, duration):
        # duration: in seconds
        # returns: nothing
        # count down
        countDown = duration
        while countDown > 0:
            print(countDown)
            countDown -= 1
            pygame.time.delay(1000)


if __name__ == '__main__':
    soundSynthesis = SoundSynthesis()
    samples = soundSynthesis.makeWhiteNoise(10, 384000)
    soundSynthesis.saveWav(samples, 384000)
    soundSynthesis.playWav()
    soundSynthesis.checkingWav()
