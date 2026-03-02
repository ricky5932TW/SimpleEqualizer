import numpy as np
from SimpleEqualizer.package.tuningInstructor.tuningInstructor import TuningInstructor
from SimpleEqualizer.package.soundAnalyze.soundAnalyze import SoundAnalyzer


class SimpleEqualizer:

    @staticmethod
    def analyze_without_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                                 playFile='../../SimpleEqualizer/soundFile/noise.wav',
                                 fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                                 output_filename='../temp_img/full.png', *args, **kwargs):
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = lowerBound
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        analyzer.play_and_record()
        analyzer.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        analyzer.saveRawData(fileName=fileName, optimize=False)

    @staticmethod
    def analyze_with_optimize(lowerBound=150, recordingName='../../SimpleEqualizer/soundFile/record.wav',
                              playFile='../../SimpleEqualizer/soundFile/noise.wav',
                              fileName='../../SimpleEqualizer/data/rawData.csv', fig_name='difference',
                              output_filename='../temp_img/full.png', *args, **kwargs):
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = lowerBound
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        analyzer.play_and_record()
        analyzer.fft(recordingName, smooth=True, fig_name=fig_name, output_filename=output_filename, save_fig=True)
        analyzer.saveRawData(fileName=fileName, optimize=True)

    @staticmethod
    def instructor(points=np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]),
                   recordingName='../../SimpleEqualizer/soundFile/record.wav',
                   playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                   separateDataFileName='../../SimpleEqualizer/data/separateData.csv',
                   gainFileName='../../SimpleEqualizer/data/1000HzGain.txt',
                   *args, **kwargs):
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = 0
        analyzer.points = points
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        analyzer.play_and_record()
        analyzer.fft(recordingName, smooth=True)
        analyzer.saveSeparateData(fileName=separateDataFileName, optimize=0)
        analyzer.save1000HzGain(fileName=gainFileName)
        instructor = TuningInstructor(separateDataFileName, gainFileName)
        instructor.loadAverageGain()
        instructor.loadCSV()
        instructor.printInstruction(vocal_enhance=True)
        instructor.savePlot()

    @staticmethod
    def white_noise_test(recordingName='../../SimpleEqualizer/soundFile/record.wav',
                         playFile='../../SimpleEqualizer/soundFile/whiteNoise.wav',
                         fig_name='Spectrum', output_filename='../temp_img/Spectrum.png', *args,
                         **kwargs):
        analyzer = SoundAnalyzer()
        if 'lowerBound' in kwargs:
            analyzer.lowerBound = kwargs['lowerBound']
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        analyzer.play_and_record()
        analyzer.fft('../../SimpleEqualizer/soundFile/record.wav', save_fig=True, smooth=True, fig_name=fig_name,
                   output_filename=output_filename)
        if 'save_raw' in kwargs:
            if kwargs['optimize']:
                analyzer.saveRawData(fileName=kwargs['save_raw'], optimize=True)
            else:
                analyzer.saveRawData(fileName=kwargs['save_raw'], optimize=False)
