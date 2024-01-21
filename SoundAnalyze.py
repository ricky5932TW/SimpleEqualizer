import scipy
from matplotlib import pyplot as plt
import pandas as pd
from Target import Target
from soundSyntheis import NoiseGenerator
import pygame
import os
import threading
import pyaudio
import wave
import time
import numpy as np
import scipy.signal as signal


def timing(func):
    def wrapper(*args, **kwargs):
        print(func.__name__ + ' start')
        start = time.time()
        func(*args, **kwargs)
        end = time.time() - start
        print('time: ', end)

    return wrapper


class SoundAnalyzer(NoiseGenerator):
    def __init__(self, fileName='noise.wav', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csvFileName = None
        self.ana_frequency_10dB = None
        self.r_fft_10dB = None
        self.averageGain = None
        self.ana_gain = []
        self.ana_frequency = None
        self.r_fft = None
        self.fileName = fileName
        self.__closeflag = False
        self.fftData = None
        self.points = [32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
        self.gainDiff = []

    @timing
    def playandRecord(self, load='noise.wav', wave_out_path="record.wav", record_second=1):
        # play noise.wav and record the sound at the same time by threading
        t_play = threading.Thread(target=self.play)  # play noise.wav
        t_record = threading.Thread(target=self.record_audio)  # record the sound
        # t_countTime = threading.Thread(target=self.countTime())  # count the time

        t_play.start()  # start the thread
        t_record.start()  # start the thread
        # t_countTime.start()

        t_play.join()  # wait for the thread to finish
        t_record.join()  # wait for the thread to finish
        # t_countTime.join()

    def play(self, load='noise.wav'):
        # play noise.wav
        pygame.mixer.init()  # initialize the mixer module
        pygame.mixer.music.load(load)  # load the sound file
        pygame.mixer.music.play()  # play the sound file
        while pygame.mixer.music.get_busy() == True:  # check if the sound is playing
            continue

    @timing
    def record_audio(self, wave_out_path="record.wav", record_second=3):
        self.__removeOldWav(wave_out_path)  # remove old noise.wav
        CHUNK = 2048  # 每个缓冲区的帧数
        FORMAT = pyaudio.paInt32  # 采样位数
        CHANNELS = 1  # 单声道
        RATE = 762000  # 采样频率
        """ 录音功能 """
        p = pyaudio.PyAudio()  # 实例化对象
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # 打开流，传入响应参数
        wf = wave.open(wave_out_path, 'wb')  # 打开 wav 文件。
        wf.setnchannels(CHANNELS)  # 声道设置
        wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
        wf.setframerate(RATE)  # 采样频率设置

        for _ in range(0, int(RATE * record_second / CHUNK)):
            data = stream.read(CHUNK)
            wf.writeframes(data)  # 写入数据
        stream.stop_stream()  # 关闭流
        stream.close()
        p.terminate()
        wf.close()
        self.__closeflag = True

    def __removeOldWav(self, fileName):
        # remove old noise.wav
        try:
            os.remove(fileName)
        except:
            pass

    def fft(self, wave, plot=False, sensitivity=False):
        # read the wave file then do fft and plot
        waveData, framerate = self.__readWav(wave)  # read the wave file
        waveData = waveData * np.hamming(len(waveData))  # apply hamming window

        if not sensitivity:
            self.r_fft = np.fft.rfft(waveData)  # do fft
            #self.r_fft = self.r_fft[:self.find_nearest(self.ana_frequency, 20000, position=True)]
            self.r_fft = np.abs(self.r_fft / np.mean(self.r_fft))  # normalize the fft result
            self.r_fft = np.hamming(len(self.r_fft)) * self.r_fft  # apply hamming window
            self.ana_frequency = np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate * 2)  # get the frequency
            """frameRate from source at "np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate)"should double it when it is 
            384000Hz, quad when it is 762000Hz. I don't know why"""
            x = self.ana_frequency[:len(self.ana_frequency)]
            y = 20 * np.log10(self.r_fft[:len(self.ana_frequency)])
        else:
            self.r_fft_10dB = np.fft.rfft(waveData)
            self.r_fft_10dB = np.abs(self.r_fft_10dB / max(self.r_fft_10dB))
            self.r_fft_10dB = np.hamming(len(self.r_fft_10dB)) * self.r_fft_10dB
            self.ana_frequency_10dB = np.fft.rfftfreq(len(self.r_fft_10dB), d=1 / framerate * 4)
            x = self.ana_frequency_10dB[:len(self.ana_frequency_10dB)]
            y = self.r_fft_10dB[:len(self.ana_frequency_10dB)]

        if plot:  # plot the result
            # biggest 30% of the fft result
            plt.plot(x, y)
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude (dB)')
            plt.title('FFT of Signal')

            plt.xlim(20, 20000)
            #plt.ylim(80, 115)
            plt.xscale('log')
            plt.grid()
            plt.show()
            # save the figure
            # fig.savefig('fft10db.png')

    def __readWav(self, _wave):
        # read the wave file
        # return: np.array
        f = wave.open(_wave, 'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)
        waveData = np.frombuffer(strData, dtype=np.int32)
        f.close()
        return waveData, framerate

    def find_nearest(self, array, value, position=False):
        array = np.asarray(array)
        # find the nearest value around target 100Hz in the array
        idx = (np.abs(array - value)).argmin()

        if position:
            return idx
        else:
            return array[idx]

    def getSeparateGain(self, range=100):
        # find the gain of distance between the 1000hz and each point
        self.points = np.array([20, 40, 210, 1000, 3000, 9000, 20000])
        for point in self.points:
            position = self.find_nearest(self.ana_frequency, point, position=1)
            self.ana_gain.append(
                20 * np.log(np.mean(self.r_fft[position - min(range, point):position + range])))
        print(self.ana_gain)
        self.saveRawData()

    def averageTheGain(self):
        # find overall average gain
        self.averageGain = 20 * np.log(
            np.average(self.r_fft[:self.find_nearest(self.ana_frequency, 20000, position=True)]))
        print(self.averageGain)

    def saveRawData(self, fileName='rawData.csv'):
        # delete the old file
        try:
            os.remove(fileName)
        except:
            pass
        # save with pandas
        df = pd.DataFrame({'freqs': self.points, 'gain': self.ana_gain})
        df.to_csv(fileName, index=False)


if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    # soundAnalyzer.playandRecord()
    eqSYS_0.fft('noise.wav', plot=True)
    # soundAnalyzer.systemSensitivity()
    eqSYS_0.getSeparateGain()
    eqSYS_0.averageTheGain()
    eqSYS_0.saveRawData(fileName='noise.csv')

'''
    eqSYS_10 = SoundAnalyzer()
    eqSYS_10.fft('noise+10dB.wav', plot=1)
    eqSYS_10.getSeparateGain()
    eqSYS_10.averageTheGain()
'''
