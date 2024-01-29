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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lowerBound = 150
        self.gainbias = 15
        self.playFile = 'noise.wav'
        self.oldCSVData = None
        self.csvFileName = None
        self.ana_frequency_10dB = None
        self.r_fft_10dB = None
        self.averageGain = None
        self.ana_gain = []
        self.ana_frequency = None
        self.r_fft = None
        self.recordingname = None
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

        t_play.start()  # start the thread
        t_record.start()  # start the thread

        t_play.join()  # wait for the thread to finish
        t_record.join()  # wait for the thread to finish

    def play(self):
        # play noise.wav
        pygame.mixer.init()  # initialize the mixer module
        pygame.mixer.music.load(self.playFile)  # load the sound file
        pygame.mixer.music.play()  # play the sound file
        while pygame.mixer.music.get_busy() == True:  # check if the sound is playing
            continue

    @timing
    def record_audio(self, record_second=3):
        self.__removeOldWav(self.recordingname)  # remove old noise.wav
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
        wf = wave.open(self.recordingname, 'wb')  # 打开 wav 文件。
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

    @staticmethod
    def __removeOldWav(fileName):
        # remove old noise.wav
        try:
            os.remove(fileName)
        except:
            pass

    def fft(self, wave, plot=False):
        # read the wave file then do fft and plot
        waveData, framerate = self.__readWav(wave)  # read the wave file
        waveData = waveData * np.hamming(len(waveData))  # apply hamming window

        self.r_fft = np.fft.rfft(waveData)  # do fft
        # self.r_fft = self.r_fft[:self.find_nearest(self.ana_frequency, 20000, position=True)]
        self.r_fft = np.abs(self.r_fft / np.mean(self.r_fft))  # normalize the fft result
        self.r_fft = np.hamming(len(self.r_fft)) * self.r_fft  # apply hamming window
        # smooth the data
        self.r_fft = signal.savgol_filter(self.r_fft, 73, 3)
        self.ana_frequency = np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate * 2)  # get the frequency
        """frameRate from source at "np.fft.rfftfreq(len(self.r_fft), d=1.0 / framerate)"should double it when it is 
        384000Hz, quad when it is 762000Hz. I don't know why"""
        x = self.ana_frequency[:int(len(self.ana_frequency) / 4)]
        y = 10 * np.log10(self.r_fft[:int(len(self.ana_frequency) / 4)])

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

    @staticmethod
    def __readWav(_wave):
        # read the wave file
        # return: np.array
        f = wave.open(_wave, 'rb')
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)
        waveData = np.frombuffer(strData, dtype=np.int32)
        f.close()
        return waveData, framerate

    @staticmethod
    def find_nearest(array, value, position=False):
        array = np.asarray(array)
        # find the nearest value around target 100Hz in the array
        idx = (np.abs(array - value)).argmin()

        if position:
            return idx
        else:
            return array[idx]

    def saveSeparateData(self, fileName='separateData.csv', optimize=False):
        """ save the data in csv file"""
        global oldCsvY
        if optimize:
            try:
                self.oldCSVData = pd.read_csv(fileName)
                oldCsvX = np.array(self.oldCSVData['freqs'])
                oldCsvY = np.array(self.oldCSVData['gain'])
            except:
                print('No old data, please run the program without optimization first')
        for point in self.points:
            position = self.find_nearest(self.ana_frequency, point, position=True)  # find the position of the point
            y = signal.savgol_filter(self.r_fft, 142, 2)    # smooth the data
            part_y = y[position - int(point / 2.1): position + int(point / 2.1)]    # get the data around the point
            self.ana_gain.append(
                10 * np.log(np.mean(list(filter(lambda x: x > 0.7*np.max(part_y), part_y))))) # get the average gain
        print(self.ana_gain)
        if optimize:
            # check if the new data is similar to the old data, if yes, use the new data, if not, use the old data +
            # 0.3 *new data
            count = 0
            for i in range(len(self.points)):
                if np.abs(self.ana_gain[i] - oldCsvY[i]) < 1:
                    self.ana_gain[i] = oldCsvY[i]
                else:
                    self.ana_gain[i] = oldCsvY[i] + 0.1 * self.ana_gain[i]
                    count += 1
            print(str(count) + ' / ' + str(len(self.points)))
        # save as csv
        df = pd.DataFrame({'freqs': self.points, 'gain': self.ana_gain})
        df.to_csv(fileName, index=False)

    @staticmethod
    def find_middle_log_scale(target, range):
        result = np.sqrt(target * range)
        if result > target:
            print(int(result) - 1)
            return int(result) - 1
        elif result < target:
            print(int(result) + 1)
            return int(result) + 1

    def save1000HzGain(self, fileName='1000HzGain.txt'):
        # get the gain of 1000Hz
        position = self.find_nearest(self.ana_frequency, 1000, position=True)
        gain1000 = 10 * np.log(np.mean(self.r_fft[position - int(1000 / 10): position + int(1000 / 10)]))
        # save the gain of 1000Hz
        with open(fileName, 'w') as f:
            f.write(str(gain1000))
        # save in txt file


    @staticmethod
    def rms(data):
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
        gain1000 = 10 * np.log(np.mean(self.r_fft[position - int(1000 / 10): position + int(1000 / 10)]))
        # save with pandas
        # 55 -> about 20Hz, little less than 20Hz
        # 150 -> about 50Hz, most speakers can't play lower than 50Hz, except for subwoofer
        x = self.ana_frequency[self.lowerBound:int(len(self.ana_frequency) / 4.7) - 1]   # get the frequency
        x[0] = 0  # set the frequency below 50Hz as 0
        y = (20 * np.log10(self.r_fft[150:int(len(self.ana_frequency) / 4.7) - 1])) - gain1000 + self.gainbias
        y = -y  # reverse the curve

        if optimize:
            # check if the new data is similar to the old data, if yes, use the new data, if not, use the old data +
            # 0.3 *new data
            count = 0
            for i in range(len(x)):
                if np.abs(y[i] - oldCsvY[i]) < 0.1:
                    y[i] = oldCsvY[i]
                else:
                    y[i] = oldCsvY[i] + 0.01 * y[i]
                    count += 1
            print(str(count) + ' / ' + str(len(x)))
        # smooth the data
        y = signal.savgol_filter(y, 91, 2)
        df = pd.DataFrame({'freqs': x, 'gain': y})
        df.to_csv(fileName, index=False)


if __name__ == '__main__':
    '''
    # for making a complete tuning data
    eqSYS_0 = SoundAnalyzer()
    eqSYS_0.recordingname = 'record.wav'
    eqSYS_0.playFile = 'noise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('record.wav', plot=True)
    eqSYS_0.saveRawData(fileName='rawDataBuiltin.csv',optimize=1)
    '''
    # for making a tuning data with signed frequency
    eqSYS_1 = SoundAnalyzer()
    eqSYS_1.points = np.array([63,125,250,500,1000,2000,4000,8000,16000])
    eqSYS_1.recordingname = 'record.wav'
    eqSYS_1.playFile = 'noise.wav'
    eqSYS_1.playandRecord()
    eqSYS_1.fft('record.wav', plot=True)
    eqSYS_1.save1000HzGain()
    eqSYS_1.saveSeparateData(optimize=0)

