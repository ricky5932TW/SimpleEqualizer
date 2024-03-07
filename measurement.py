from scripts import SimpleEqualizer


class Measurement_mission:
    @staticmethod
    def Measurement(standard, lower_bound, filePATH, optimize):
        if optimize == '0' or optimize == 0 or optimize == 'False' or optimize == 'false' or optimize == False:
            SimpleEqualizer.analyze_without_optimize(lowerBound=int(lower_bound), fileName=filePATH, playFile=standard)
        else:
            SimpleEqualizer.analyze_with_optimize(lowerBound=int(lower_bound), fileName=filePATH, playFile=standard)

        SimpleEqualizer.white_noise_test()

    @staticmethod
    def Measurement_limited(band):
        SimpleEqualizer.instructor(points=band)
        SimpleEqualizer.white_noise_test()

    @staticmethod
    def whiteNoiseTest():
        SimpleEqualizer.white_noise_test()


if __name__ == '__main__':
    Measurement_mission.Measurement('soundFile/noise.wav', 150, 'data/rawData2.csv', optimize='0')
