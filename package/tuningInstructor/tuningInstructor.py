import numpy as np
import matplotlib.pyplot as plt
import pandas


class TuningInstructor():
    def __init__(self, filename=None, averageGainFile=None, *args, **kwargs):
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
        plt.plot((0, 20000), (self.averageGain, self.averageGain), '--', label='average(target)')
        plt.xscale('log')
        plt.grid(True, which="both")
        plt.title('Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain (dB)')
        plt.savefig('spectrum.png')
        plt.legend()
        plt.show()

    def printInstruction(self,vocal_enhance=False):
        """finding how to tune the gain compared to 1000 Hz"""
        stdGain = self.averageGain
        diffGain = self.gains - stdGain
        diffGain = -diffGain
        # print frequency and gain
        stdDiffGain = dict(zip(self.criticalFreqs, diffGain))
        if vocal_enhance:
            # add 4 dB to the gain between 2000 and 6000 Hz
            for freq in range(2000, 6000, 100):
                try:
                    stdDiffGain[freq] += 5
                except:
                    pass
        # if the gain is less than 1 , set it to 0
        for freq in stdDiffGain:
            if np.abs(stdDiffGain[freq]) < 1:
                stdDiffGain[freq] = 0
        # if the gain is more than 12, then multiply 1/2
        for freq in stdDiffGain:
            if stdDiffGain[freq] > 12:
                stdDiffGain[freq] *= 0.5
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
    instructor = TuningInstructor('separateData.csv', '1000HzGain.txt')
    instructor.loadAverageGain()
    instructor.loadCSV()
    instructor.printInstruction()
