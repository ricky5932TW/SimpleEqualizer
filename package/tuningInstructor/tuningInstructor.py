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
                    stdDiffGain[freq] += 4
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

        with open('instruction.txt', 'w') as f:
            for freq in stdDiffGain:
                f.write(f'{freq} Hz: {stdDiffGain[freq]} dB\n')

    def savePlot(self, fileName='../../temp_img/separated_spectrum.png'):
        plt.plot(self.criticalFreqs, self.gains, label='responce')
        plt.plot((0, 20000), (self.averageGain, self.averageGain), '--', label='average(target)')
        plt.xscale('log')
        plt.grid(True, which="both")
        plt.title('Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Gain (dB)')
        plt.legend()
        plt.savefig(fileName)



    def __checkInit(self):
        if self.CSVFileName is None:
            raise ValueError('CSVFileName is not set')


if __name__ == '__main__':
    instructor = TuningInstructor('../../data/separateData.csv', '../../data/1000HzGain.txt')
    instructor.loadAverageGain()
    instructor.loadCSV()
    instructor.printInstruction()
    instructor.savePlot()
