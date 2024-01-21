import numpy as np
import matplotlib.pyplot as plt


class SensitivityMeasurementAgent():
    def __init__(self, normalnoise=None, boostnoise=None, gainDiff=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normalnoise = normalnoise
        self.boostnoise = boostnoise
        self.gainDiff = gainDiff
        self.status = None
        self.__checkInit()

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
        if self.normalnoise is None:
            self.status = 'Error: normalnoise is None'
            print('Error: normalnoise is None')
            return False
        if self.boostnoise is None:
            self.status = 'Error: boostnoise is None'
            print('Error: boostnoise is None')
            return False
        return True
