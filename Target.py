"""read the target targetData from the file  as txt
"""
import numpy as np
import matplotlib.pyplot as plt


class Target:
    def __init__(self, targetPath='SimpleEqualizer/referrence/Harman Curve.txt', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.targetData = None
        self.__path = targetPath
        self.__readTarget()

    def __readTarget(self):
        # __path: a string
        # returns: a numpy array of floats
        # read the target targetData from the file  as txt
        # x axis: frequency
        # y axis: amplitude
        self.targetData = np.loadtxt(self.__path)

    def plotTarget(self):
        # targetData: a numpy array of floats
        # returns: nothing
        # plot the target targetData
        # x axis: frequency
        # y axis: amplitude
        data = self.targetData
        plt.psd(data[:, 0], data[:, 1], 'bo-')
        plt.grid()
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')
        plt.show()


if __name__ == '__main__':
    target = Target()
    target.plotTarget()