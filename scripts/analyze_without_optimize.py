from scripts import SimpleEqualizer

if __name__ == '__main__':
    SimpleEqualizer.analyze_without_optimize(fileName='../data/rawData_mi_stereo.csv',lowerBound=300)
    SimpleEqualizer.white_noise_test()
