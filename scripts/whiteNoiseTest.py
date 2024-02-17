from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer

# Create a SoundAnalyzer object

if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    eqSYS_0.recordingname = '../../SimpleEqualizer/soundFile/record.wav'
    eqSYS_0.playFile = '../../SimpleEqualizer/soundFile/whiteNoise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('../../SimpleEqualizer/soundFile/record.wav', plot=1,smooth=1)
