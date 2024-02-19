import numpy as np

from SimpleEqualizer.package.tuningInstructor.tuningInstructor import TuningInstructor
from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer

if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    # default values:150 (~52Hz)
    eqSYS_0.lowerBound = 0
    eqSYS_0.points = np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000])
    eqSYS_0.recordingname = '../../SimpleEqualizer/soundFile/record.wav'
    # for white noise: '../../SimpleEqualizer/soundFile/whiteNoise.wav'
    eqSYS_0.playFile = '../../SimpleEqualizer/soundFile/whiteNoise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('../../SimpleEqualizer/soundFile/record.wav', plot=1, smooth=True)
    # saveSeparateData first, then save1000HzGain
    eqSYS_0.saveSeparateData(fileName='../../SimpleEqualizer/data/separateData.csv', optimize=0)
    eqSYS_0.save1000HzGain(fileName='../../SimpleEqualizer/data/1000HzGain.txt')
    instructor = TuningInstructor('../../SimpleEqualizer/data/separateData.csv', '../../SimpleEqualizer/data'
                                                                                 '/1000HzGain.txt')
    instructor.loadAverageGain()
    instructor.loadCSV()
    instructor.printInstruction(vocal_enhance=True)

