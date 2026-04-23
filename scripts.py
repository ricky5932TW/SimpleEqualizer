import numpy as np
from package.tuningInstructor.tuningInstructor import TuningInstructor
from package.soundAnalyze.soundAnalyze import SoundAnalyzer
from runtime_state import write_status


def _repeat_count(repeat_count):
    try:
        count = int(repeat_count)
    except (TypeError, ValueError):
        count = 1
    return max(1, min(count, 20))


def _record_frequency_average(analyzer, recording_name, repeat_count, label):
    repeat_count = _repeat_count(repeat_count)
    spectra = []
    frequencies = None
    for index in range(repeat_count):
        suffix = f" ({index + 1}/{repeat_count})" if repeat_count > 1 else ""
        write_status(f'Playing and recording {label}{suffix}...')
        analyzer.play_and_record()
        write_status(f'Computing FFT {label}{suffix}...')
        analyzer.fft(recording_name, smooth=True)
        spectra.append(np.copy(analyzer.r_fft))
        frequencies = np.copy(analyzer.ana_frequency)

    min_length = min(len(spectrum) for spectrum in spectra)
    analyzer.r_fft = np.mean(np.vstack([spectrum[:min_length] for spectrum in spectra]), axis=0)
    analyzer.ana_frequency = frequencies[:min_length]
    return repeat_count


class SimpleEqualizer:

    @staticmethod
    def analyze_without_optimize(lowerBound=150, recordingName='soundFile/record.wav',
                                 playFile='soundFile/noise.wav',
                                 fileName='data/rawData.csv', fig_name='difference',
                                 output_filename='static/temp_img/full.png', repeat_count=1, *args, **kwargs):
        write_status('Analyzing without optimization...')
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = lowerBound
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        repeats = _record_frequency_average(analyzer, recordingName, repeat_count, 'full response')
        status = 'Rendering averaged full response...' if repeats > 1 else 'Rendering full response...'
        write_status(status)
        analyzer.render_fft_plot(fig_name=fig_name, output_filename=output_filename, save_fig=True, smooth=True)
        analyzer.saveRawData(fileName=fileName, optimize=False)

    @staticmethod
    def analyze_with_optimize(lowerBound=150, recordingName='soundFile/record.wav',
                              playFile='soundFile/noise.wav',
                              fileName='data/rawData.csv', fig_name='difference',
                              output_filename='static/temp_img/full.png', repeat_count=1, *args, **kwargs):
        write_status('Analyzing with optimization...')
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = lowerBound
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        repeats = _record_frequency_average(analyzer, recordingName, repeat_count, 'optimized response')
        status = 'Rendering averaged optimized response...' if repeats > 1 else 'Rendering optimized response...'
        write_status(status)
        analyzer.render_fft_plot(fig_name=fig_name, output_filename=output_filename, save_fig=True, smooth=True)
        analyzer.saveRawData(fileName=fileName, optimize=True)

    @staticmethod
    def instructor(points=np.array([63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]),
                   recordingName='soundFile/record.wav',
                   playFile='soundFile/whiteNoise.wav',
                   separateDataFileName='data/separateData.csv',
                   gainFileName='data/1000HzGain.txt',
                   output_filename='static/temp_img/separated_spectrum.png',
                   repeat_count=1, *args, **kwargs):
        write_status('Analyzing limited-band response...')
        analyzer = SoundAnalyzer()
        analyzer.lowerBound = 0
        analyzer.points = points
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        _record_frequency_average(analyzer, recordingName, repeat_count, 'limited-band response')
        write_status('Generating tuning instructions...')
        analyzer.saveSeparateData(fileName=separateDataFileName, optimize=0)
        analyzer.save1000HzGain(fileName=gainFileName)
        instructor = TuningInstructor(separateDataFileName, gainFileName)
        instructor.loadAverageGain()
        instructor.loadCSV()
        instructor.printInstruction(vocal_enhance=True)

        #instructor.savePlot(fileName=output_filename)

    @staticmethod
    def white_noise_test(recordingName='soundFile/record.wav',
                         playFile='soundFile/whiteNoise.wav',
                         fig_name='Spectrum', output_filename='static/temp_img/Spectrum.png', repeat_count=1, *args,
                         **kwargs):
        analyzer = SoundAnalyzer()
        if 'lowerBound' in kwargs:
            analyzer.lowerBound = kwargs['lowerBound']
        analyzer.recordingName = recordingName
        analyzer.playFile = playFile
        repeats = _record_frequency_average(analyzer, recordingName, repeat_count, 'white noise')
        status = 'Rendering averaged white-noise spectrum...' if repeats > 1 else 'Rendering white-noise spectrum...'
        write_status(status)
        analyzer.render_fft_plot(save_fig=True, smooth=True, fig_name=fig_name, output_filename=output_filename)
        if 'save_raw' in kwargs:
            if kwargs['optimize']:
                analyzer.saveRawData(fileName=kwargs['save_raw'], optimize=True)
            else:
                analyzer.saveRawData(fileName=kwargs['save_raw'], optimize=False)
