from scripts import SimpleEqualizer


class Measurement_mission:
    @staticmethod
    def Measurement(standard, lower_bound, filePATH, optimize):
        if optimize == '0':
            SimpleEqualizer.analyze_without_optimize(lowerBound=int(lower_bound), fileName=filePATH, playFile=standard)
        else:
            SimpleEqualizer.analyze_with_optimize(lowerBound=int(lower_bound), fileName=filePATH, playFile=standard)

        SimpleEqualizer.white_noise_test()
