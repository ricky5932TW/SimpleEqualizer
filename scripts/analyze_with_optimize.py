from scripts import SimpleEqualizer

if __name__ == '__main__':
    SimpleEqualizer.analyze_with_optimize(fileName='../data/rawData_k92.csv', lowerBound=0)
    SimpleEqualizer.white_noise_test()