from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer

if __name__ == '__main__':
    # for making a complete tuning data
    eqSYS_0 = SoundAnalyzer()
    # default values:150 (~55Hz)
    eqSYS_0.lowerBound = 150
    eqSYS_0.recordingName = '../../SimpleEqualizer/soundFile/record.wav'
    # for white noise: '../../SimpleEqualizer/soundFile/whiteNoise.wav'
    eqSYS_0.playFile = '../../SimpleEqualizer/soundFile/noise.wav'
    eqSYS_0.playandRecord()
    eqSYS_0.fft('../../SimpleEqualizer/soundFile/record.wav', smooth=True, fig_name='Spectrum',
                output_filename='../../SimpleEqualizer/data/full.png')
    eqSYS_0.saveRawData(fileName='../../data/rawData_3inches.csv', optimize=False)
