import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import pygame
import os
import threading
import pydub
import scipy

from SimpleEqualizer.multiadd import multiadd


class SoundSynthesis(multiadd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__eq = None
        self.fileName = 'whiteNoise.wav'

    def __deleteOldWav(self):
        # fileName: a string
        # returns: nothing
        # delete a wav file
        if os.path.exists(self.fileName):
            os.remove(self.fileName)

    def generareTarget(self, sampleRate, duration):
        # sampleRate: in Hz
        # duration: in seconds
        # returns: a numpy array of floats
        # generate a target
        # x axis: frequency
        # y axis: amplitude
        result = self.multiadd(sampleRate, duration)
        return result

    def makewhitenoise(self, sampleRate, duration):
        # sampleRate: in Hz
        # duration: in seconds
        # returns: a numpy array of floats
        # generate a target
        # x axis: frequency
        # y axis: amplitude
        result = np.random.normal(0, 1, int(sampleRate * duration))
        fft = np.fft.fft(result)

        for freq in range(0, len(fft)):
            if freq <41:
                fft[freq] *= 10000
            elif freq < 210:
                fft[freq] *= (-0.03846153846*freq + 5.576923077)*10000
            elif freq < 1000:
                fft[freq] *= (0.0031645569620253164557*freq - 3.1645569620253164557)*10000
            elif freq < 3000:
                fft[freq] *= (0.005*freq - 5.000)*10000
            elif freq < 9000:
                fft[freq] *= (-0.0015*freq + 14.5000)*10000
            elif freq < 20000:
                fft[freq] *= (-0.0014545454545454545455*freq + 14.090909090909090910)*10000
            else:
                fft[freq] *= 0
        result = np.fft.ifft(fft).astype(np.float64)*(10**(1/20))
        return abs(result)

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
        '''for freq in range(0, len(fft)):
            try:
                if fft[freq] > 0:
                    fft[freq] = (fft[freq - 1] + fft[freq + 1]) / 2
            except:
                pass'''

        plt.subplot(211)
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.xscale('log.txt')
        plt.xlim(0, 20000)
        plt.psd(fft, Fs=rate*2, NFFT=128, scale_by_freq=True, sides='default')
        plt.grid()
        plt.subplot(212)
        plt.xlabel('t')
        plt.xlim(0, 20000)
        plt.ylabel('Amplitude')
        plt.plot(data, 'b-')
        plt.grid()
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
    samples = soundSynthesis.generareTarget(48000, 5)
    #samples = soundSynthesis.makewhitenoise(48000, 5)
    soundSynthesis.saveWav(samples, 48000)
    #soundSynthesis.playWav()
    soundSynthesis.checkingWav()
