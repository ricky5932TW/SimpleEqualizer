from SimpleEqualizer.package.tuningInstructor.tuningInstructor import TuningInstructor
from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer

if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    # default values:150 (~55Hz)
    eqSYS_0.lowerBound = 150
    eqSYS_0.recordingname = '../../SimpleEqualizer/soundFile/record.wav'
    # for white noise: '../../SimpleEqualizer/soundFile/whiteNoise.wav'
    eqSYS_0.playFile = '../../SimpleEqualizer/soundFile/noise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('../../SimpleEqualizer/soundFile/record.wav', plot=1, smooth=True)
    eqSYS_0.save1000HzGain(fileName='../../SimpleEqualizer/data/1000HzGain.txt')
    eqSYS_0.saveSeparateData(fileName='../../SimpleEqualizer/data/separateData.csv')
    instructor = TuningInstructor('../../SimpleEqualizer/data/separateData.csv', '../../SimpleEqualizer/data/1000HzGain.txt')
    instructor.loadAverageGain()
    instructor.loadCSV()
    instructor.printInstruction()

