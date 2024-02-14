from soundAnalyze import SoundAnalyzer

if __name__ == '__main__':
    eqSYS_0 = SoundAnalyzer()
    eqSYS_0.fft('soundFile/noise.wav', plot=1)
    eqSYS_0.fft('soundFile/noise10000Hz.wav', plot=1)

