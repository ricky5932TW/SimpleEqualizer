from scripts import SimpleEqualizer
from package.history import History


class MeasurementService:
    @staticmethod
    def run_measurement(standard, lower_bound, filePATH, optimize, repeat_count=1):
        run_id = History.record_start(
            "full",
            {
                "standard": standard,
                "lower_bound": lower_bound,
                "filePATH": filePATH,
                "optimize": optimize,
                "repeat_count": repeat_count,
            },
        )
        try:
            if optimize == '0' or optimize == 0 or optimize == 'False' or optimize == 'false' or optimize == False:
                SimpleEqualizer.analyze_without_optimize(lowerBound=int(lower_bound), fileName=filePATH,
                                                         playFile=standard, repeat_count=repeat_count)
            else:
                SimpleEqualizer.analyze_with_optimize(lowerBound=int(lower_bound), fileName=filePATH, playFile=standard,
                                                      repeat_count=repeat_count)
            SimpleEqualizer.white_noise_test(repeat_count=repeat_count)
        except Exception as exc:
            History.record_finish(run_id, "error", [], note=str(exc))
            raise
        History.record_finish(run_id, "ok", ["static/temp_img/full.png", "static/temp_img/Spectrum.png"])

    @staticmethod
    def run_measurement_limited(band, repeat_count=1):
        run_id = History.record_start("limited", {"band": band, "repeat_count": repeat_count})
        try:
            SimpleEqualizer.instructor(points=band, repeat_count=repeat_count)
            SimpleEqualizer.white_noise_test(repeat_count=repeat_count)
        except Exception as exc:
            History.record_finish(run_id, "error", [], note=str(exc))
            raise
        History.record_finish(run_id, "ok", ["static/temp_img/Spectrum.png"])

    @staticmethod
    def white_noise_test(repeat_count=1):
        run_id = History.record_start("white_noise", {"repeat_count": repeat_count})
        try:
            SimpleEqualizer.white_noise_test(repeat_count=repeat_count)
        except Exception as exc:
            History.record_finish(run_id, "error", [], note=str(exc))
            raise
        History.record_finish(run_id, "ok", ["static/temp_img/Spectrum.png"])


if __name__ == '__main__':
    MeasurementService.run_measurement('soundFile/noise.wav', 150, 'data/rawData2.csv', optimize='0')
