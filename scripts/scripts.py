import numpy as np
from SimpleEqualizer.package.tuningInstructor.tuningInstructor import TuningInstructor
from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer


class SimpleEqualizer:
    def __init__(self):
        pass

    @staticmethod
    def analyze_without_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                                 playFile='../../SimpleEqualizer/soundFile/noise.wav',
                                 fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                                 output_filename='../../SimpleEqualizer/data/full.png',*args, **kwargs):
        eqSYS = SoundAnalyzer()
        eqSYS.lowerBound = lowerBound
        eqSYS.recordingName = recordingName
        eqSYS.playFile = playFile
        eqSYS.playandRecord()
        eqSYS.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        eqSYS.saveRawData(fileName=fileName, optimize=False)

    @staticmethod
    def analyze_with_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                              playFile='../../SimpleEqualizer/soundFile/noise.wav',
                              fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                              output_filename='../../SimpleEqualizer/data/full.png',*args, **kwargs):
        eqSYS = SoundAnalyzer()
        eqSYS.lowerBound = lowerBound
        eqSYS.recordingName = recordingName
        eqSYS.playFile = playFile
        eqSYS.playandRecord()
        eqSYS.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        eqSYS.saveRawData(fileName=fileName, optimize=True)

    @staticmethod
    def instructor(points=np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]),
                   recordingName='../../SimpleEqualizer/soundFile/record.wav',
                   playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                   separateDataFileName='../../SimpleEqualizer/data/separateData.csv',
                   gainFileName='../../SimpleEqualizer/data/1000HzGain.txt',
                   *args, **kwargs):
        eqSYS = SoundAnalyzer()
        eqSYS.lowerBound = 0
        eqSYS.points = points
        eqSYS.recordingName = recordingName
        eqSYS.playFile = playFile
        eqSYS.playandRecord()
        eqSYS.fft(recordingName, smooth=True)
        eqSYS.saveSeparateData(fileName=separateDataFileName, optimize=0)
        eqSYS.save1000HzGain(fileName=gainFileName)
        instructor = TuningInstructor(separateDataFileName, gainFileName)
        instructor.loadAverageGain()
        instructor.loadCSV()
        instructor.printInstruction(vocal_enhance=True)
        instructor.savePlot()

    @staticmethod
    def white_noise_test(recordingName='../../SimpleEqualizer/soundFile/record.wav',
                         playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                         fig_name='Spectrum', output_filename='../../SimpleEqualizer/data/Spectrum.png',*args, **kwargs):
        eqSYS = SoundAnalyzer()
        eqSYS.recordingName = recordingName
        eqSYS.playFile = playFile
        eqSYS.playandRecord()
        eqSYS.fft('../../SimpleEqualizer/soundFile/record.wav', save_fig=True, smooth=1,fig_name=fig_name,
                  output_filename=output_filename)

