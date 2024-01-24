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
        print(func.__name__ + 'time: ', end)

    return wrapper


class SoundAnalyzer(NoiseGenerator):
    def __init__(self, fileName='noise.wav', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oldCSVData = None
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
        # self.points = [125, 250, 500, 1000, 2000, 4000, 8000, 16000]
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
        RATE = 384000  # 采样频率
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
            # self.r_fft = self.r_fft[:self.find_nearest(self.ana_frequency, 20000, position=True)]
            self.r_fft = np.abs(self.r_fft / np.mean(self.r_fft))  # normalize the fft result
            self.r_fft = np.hamming(len(self.r_fft)) * self.r_fft  # apply hamming window
            # smooth the data
            self.r_fft = signal.savgol_filter(self.r_fft, 51, 3)
            self.ana_frequency = np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate * 2)  # get the frequency
            """frameRate from source at "np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate)"should double it when it is 
            384000Hz, quad when it is 762000Hz. I don't know why"""
            x = self.ana_frequency[:int(len(self.ana_frequency) / 4)]
            y = 10 * np.log10(self.r_fft[:int(len(self.ana_frequency) / 4)])
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
            # plt.ylim(80, 115)
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

    def testing_getSeparateGain(self):
        """This function is still under testing"""
        # find the gain of distance between the 1000hz and each point
        self.points = np.array([20, 40, 210, 1000, 3000, 9000, 20000])
        # self.h = np.array([4, 4, -3, 0, 10, 1, -20])
        for i in range(len(self.points)):
            point = self.points[i]
            position = self.find_nearest(self.ana_frequency, point, position=True)
            if point == self.points[0]:
                self.ana_gain.append(10 * np.log(np.mean(self.r_fft[self.find_nearest(self.ana_frequency,
                                                                                      1,
                                                                                      position=True):
                                                                    position +
                                                                    self.find_nearest(self.ana_frequency,
                                                                                      self.find_middle_log_scale(
                                                                                          self.points[0],
                                                                                          self.points[1]),
                                                                                      position=True)])))
            elif point == self.points[-1]:
                self.ana_gain.append(10 * np.log(np.mean(self.r_fft[position -
                                                                    self.find_nearest(self.ana_frequency,
                                                                                      self.find_middle_log_scale(
                                                                                          self.points[-1],
                                                                                          self.points[-2]),
                                                                                      position=True):
                                                                    position +
                                                                    self.find_nearest(self.ana_frequency,
                                                                                      self.find_middle_log_scale(
                                                                                          self.points[-1],
                                                                                          self.points[-2]),
                                                                                      position=True)])))
            else:
                self.ana_gain.append(10 * np.log(np.mean(self.r_fft[position -
                                                                    self.find_nearest(self.ana_frequency,
                                                                                      self.find_middle_log_scale(
                                                                                          self.points[i],
                                                                                          self.points[i - 1]),
                                                                                      position=True):
                                                                    position +
                                                                    self.find_nearest(self.ana_frequency,
                                                                                      self.find_middle_log_scale(
                                                                                          self.points[i],
                                                                                          self.points[i + 1]),
                                                                                      position=True)])))

        print(self.ana_gain)
        self.saveRawData()

    def getSeparateGain(self, range=100):
        # self.points = np.array([20, 40, 210, 1000, 3000, 9000, 20000])
        for point in self.points:
            position = self.find_nearest(self.ana_frequency, point, position=True)
            self.ana_gain.append(
                10 * np.log(np.mean(self.r_fft[position - int(point / 2.1): position + int(point / 4)])))
        print(self.ana_gain)

    @staticmethod
    def find_middle_log_scale(target, range, divide=10):
        result = np.sqrt(target * range)
        if result > target:
            print(int(result) - 1)
            return int(result) - 1
        elif result < target:
            print(int(result) + 1)
            return int(result) + 1

    def averageTheGain(self):
        # find overall average gain
        self.averageGain = 10 * np.log(
            np.sqrt((np.mean((np.square(self.r_fft[:self.find_nearest(self.ana_frequency, 20000, position=True)]))))))
        print(self.averageGain)
        # save as txt
        with open('averageGain.txt', 'w') as f:
            f.write(str(self.averageGain))

    def rms(self, data):
        return np.mean(data)
        # return np.sqrt(np.mean(np.square(data)))

    def saveRawData(self, fileName='rawData.csv', optimize=False):
        # delete the old file
        global oldCsvY
        if optimize:
            try:
                self.oldCSVData = pd.read_csv(fileName)
                oldCsvX = np.array(self.oldCSVData['freqs'])
                oldCsvY = np.array(self.oldCSVData['gain'])
            except:
                print('No old data, please run the program without optimization first')
        try:
            os.remove(fileName)
        except:
            pass

        position = self.find_nearest(self.ana_frequency, 1000, position=True)
        gain1000 = 10 * np.log(np.mean(self.r_fft[position - int(1000 / 4): position + int(1000 / 4)]))
        # save with pandas
        x = self.ana_frequency[55:int(len(self.ana_frequency) / 4.7) - 1]
        y = (20 * np.log10(self.r_fft[55:int(len(self.ana_frequency) / 4.7) - 1])) - gain1000 + 15
        y = -y

        if optimize:
            # check if the new data is similar to the old data, if yes, use the new data, if not, use the old data +
            # 0.3 *new data
            count = 0
            for i in range(len(x)):
                if np.abs(y[i] - oldCsvY[i]) < 3:
                    y[i] = oldCsvY[i]
                else:
                    y[i] = oldCsvY[i] + 0.01 * y[i]
                    count += 1
            print(str(count) + ' / ' + str(len(x)))
        df = pd.DataFrame({'freqs': x, 'gain': y})
        df.to_csv(fileName, index=False)


if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    eqSYS_0.playandRecord()
    eqSYS_0.fft('record.wav', plot=True)
    # soundAnalyzer.systemSensitivity()
    #eqSYS_0.averageTheGain()
    #eqSYS_0.getSeparateGain()
    eqSYS_0.saveRawData(optimize=True)
