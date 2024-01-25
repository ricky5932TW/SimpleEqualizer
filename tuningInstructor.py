import numpy as np
import matplotlib.pyplot as plt
import pandas


class TuningInstuctor():
    def __init__(self, filename=None, averageGainFile=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gainAndFreq = None
        self.CSVFileName = filename
        self.averageGainFile = averageGainFile
        self.averageGain = None
        self.__checkInit()
        self.status = None
        self.criticalFreqs = None
        self.gains = None
        self.instruction = None

    def loadAverageGain(self):
        with open(self.averageGainFile, 'r') as f:
            self.averageGain = float(f.read())

    def loadCSV(self):
        """
        freqs,gain
        20,70.69343350982481
        40,75.86023778172492
        210,74.99762659617589
        1000,78.31608365525997
        3000,76.77828485652836
        9000,72.79308333409435
        20000,70.12100273365037
        """
        data = pandas.read_csv(self.CSVFileName)
        self.status = 'loadCSV'
        self.criticalFreqs = np.array(data['freqs'])
        self.gains = np.array(data['gain'])
        # combine the data into dict
        data = dict(zip(self.criticalFreqs, self.gains))
        self.gainAndFreq = data
        print(data)
        print(self.criticalFreqs)
        print(self.gains)
        plt.plot(self.criticalFreqs, self.gains, label='responce')
        plt.plot((0,20000), (self.gains[3],self.gains[3]), '--', label='average(target)')
        plt.xscale('log')
        plt.grid(True, which="both")
        plt.title('Spectrum')
        plt.ylim([self.gains[3]-15, self.gains[3]+15])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain (dB)')
        plt.savefig('spectrum.png')
        plt.legend()
        plt.show()
        return True

    def instructor(self):
        """finding how to tune the gain compared to 1000 Hz"""
        stdGain = self.gains[5]
        diffGain = self.gains-stdGain
        # set diffGain as 0 when the absolute value is less than 3 dB
        diffGain[np.abs(diffGain) < 1] = 0
        #set diffGain half the original value when the absolute value is lager than 12dB
        diffGain[np.abs(diffGain) > 12] = diffGain[np.abs(diffGain) > 12]/2
        diffGain = -diffGain
        # print frequency and gain
        stdDiffGain = dict(zip(self.criticalFreqs, diffGain))
        print(stdDiffGain)







    def savePlot(self, fileName='sensitivity.png'):
        if self.__checkInit():
            plt.figure(figsize=(10, 5))
            plt.plot(self.normalnoise.freqs, self.normalnoise.r_fft, label='normal')
            plt.plot(self.boostnoise.freqs, self.boostnoise.r_fft, label='boost')
            plt.xscale('log')
            plt.grid(True, which="both")
            plt.legend()
            plt.savefig(fileName)
            plt.close()
            self.status = 'Success'
            print('Success')
            return True
        else:
            return False

    def __checkInit(self):
        if self.CSVFileName is None:
            raise ValueError('CSVFileName is not set')


if __name__ == '__main__':
    instructor = TuningInstuctor('separateData.csv', 'averageGain.txt')
    instructor.loadAverageGain()
    instructor.loadCSV()
    instructor.instructor()
