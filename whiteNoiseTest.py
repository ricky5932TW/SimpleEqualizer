from soundAnalyze import SoundAnalyzer

# Create a SoundAnalyzer object

if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    eqSYS_0.lowerBound = 150
    eqSYS_0.recordingname = 'soundFile/record.wav'
    eqSYS_0.playFile = 'soundFile/noise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('soundFile/record.wav', plot=1,smooth=1)
