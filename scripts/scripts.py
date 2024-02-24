import numpy as np
from SimpleEqualizer.package.tuningInstructor.tuningInstructor import TuningInstructor
from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer


class SimpleEqualizer:

    @staticmethod
    def analyze_without_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                                 playFile='../../SimpleEqualizer/soundFile/noise.wav',
                                 fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                                 output_filename='../temp_img/full.png', *args, **kwargs):
        eqSYS0 = SoundAnalyzer()
        eqSYS0.lowerBound = lowerBound
        eqSYS0.recordingName = recordingName
        eqSYS0.playFile = playFile
        eqSYS0.playandRecord()
        eqSYS0.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        eqSYS0.saveRawData(fileName=fileName, optimize=False)

    @staticmethod
    def analyze_with_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                              playFile='../../SimpleEqualizer/soundFile/noise.wav',
                              fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                              output_filename='../temp_img/full.png', *args, **kwargs):
        eqSYS1 = SoundAnalyzer()
        eqSYS1.lowerBound = lowerBound
        eqSYS1.recordingName = recordingName
        eqSYS1.playFile = playFile
        eqSYS1.playandRecord()
        eqSYS1.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        eqSYS1.saveRawData(fileName=fileName, optimize=True)

    @staticmethod
    def instructor(points=np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]),
                   recordingName='../../SimpleEqualizer/soundFile/record.wav',
                   playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                   separateDataFileName='../../SimpleEqualizer/data/separateData.csv',
                   gainFileName='../../SimpleEqualizer/data/1000HzGain.txt',
                   *args, **kwargs):
        eqSYS2 = SoundAnalyzer()
        eqSYS2.lowerBound = 0
        eqSYS2.points = points
        eqSYS2.recordingName = recordingName
        eqSYS2.playFile = playFile
        eqSYS2.playandRecord()
        eqSYS2.fft(recordingName, smooth=True)
        eqSYS2.saveSeparateData(fileName=separateDataFileName, optimize=0)
        eqSYS2.save1000HzGain(fileName=gainFileName)
        instructor0 = TuningInstructor(separateDataFileName, gainFileName)
        instructor0.loadAverageGain()
        instructor0.loadCSV()
        instructor0.printInstruction(vocal_enhance=True)
        instructor0.savePlot()

    @staticmethod
    def white_noise_test(recordingName='../../SimpleEqualizer/soundFile/record.wav',
                         playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                         fig_name='Spectrum', output_filename='../temp_img/Spectrum.png', *args,
                         **kwargs):
        eqSYS3 = SoundAnalyzer()
        if 'lowerBound' in kwargs:
            eqSYS3.lowerBound = kwargs['lowerBound']
        eqSYS3.recordingName = recordingName
        eqSYS3.playFile = playFile
        eqSYS3.playandRecord()
        eqSYS3.fft('../../SimpleEqualizer/soundFile/record.wav', save_fig=True, smooth=True, fig_name=fig_name,
                   output_filename=output_filename)
        if 'save_raw' in kwargs:
            if kwargs['optimize']:
                eqSYS3.saveRawData(fileName=kwargs['save_raw'], optimize=True)
            else:
                eqSYS3.saveRawData(fileName=kwargs['save_raw'], optimize=False)
