from matplotlib import pyplot as plt

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


class SoundAnalyzer(NoiseGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r_fft = None
        self.fileName = 'noise.wav'
        self.__closeflag = False
        self.fftData = None

    def playandRecord(self):
        # play noise.wav and record the sound at the same time by threading
        t_play = threading.Thread(target=self.play)  # play noise.wav
        t_record = threading.Thread(target=self.record_audio)  # record the sound
        t_countTime = threading.Thread(target=self.countTime)  # count the time

        t_play.start()  # start the thread
        t_record.start()  # start the thread
        t_countTime.start()

        t_play.join()  # wait for the thread to finish
        t_record.join()  # wait for the thread to finish
        t_countTime.join()

    def play(self):
        # play noise.wav
        pygame.mixer.init()  # initialize the mixer module
        pygame.mixer.music.load(self.fileName)  # load the sound file
        pygame.mixer.music.play()  # play the sound file
        while pygame.mixer.music.get_busy() == True:  # check if the sound is playing
            continue

    def record_audio(self, wave_out_path="record.wav", record_second=3):
        self.__removeOldWav(wave_out_path)  # remove old noise.wav
        CHUNK = 2048  # 每个缓冲区的帧数
        FORMAT = pyaudio.paInt32  # 采样位数
        CHANNELS = 1  # 单声道
        RATE = 192000  # 采样频率
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

    def countTime(self):
        t = 0
        self.__closeflag = False
        while True:
            print(t)
            t += 1
            time.sleep(1)
            if self.__closeflag:
                break

    def fft(self, wave, plot=False):
        # read the wave file then do fft and plot
        waveData, framerate = self.__readWav(wave)  # read the wave file
        self.r_fft = np.fft.rfft(waveData)  # do fft
        self.r_fft = np.abs(self.r_fft / max(self.r_fft))  # normalize
        frequency = np.fft.rfftfreq(len(self.r_fft), d=1 / framerate)  # get the frequency
        if plot:  # plot the result
            plt.xscale('symlog')
            plt.xlim(1, 20000)
            plt.grid()
            plt.plot(frequency[:len(frequency)], 10 * np.log10(self.r_fft[:len(frequency)]))
            plt.xlabel('Frequency')
            plt.ylabel('Gain')
            plt.show()

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

    def set1000Hzas1dB(self):
        # set the 1000Hz as 1dB
        gain1000 = self.find_nearest(self.r_fft, 1000)
        print(gain1000)
        self.r_fft = self.r_fft - gain1000 + 1

    def getgain(self, freq):
        # get the gain of the frequency
        # return: float
        pass

    def find_nearest(self, array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]


if __name__ == '__main__':
    soundAnalyzer = SoundAnalyzer()
    soundAnalyzer.fft("record.wav", plot=True)
