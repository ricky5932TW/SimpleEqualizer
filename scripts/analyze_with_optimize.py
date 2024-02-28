from scripts import SimpleEqualizer
from TxtOp import TxtOp

if __name__ == '__main__':
    SimpleEqualizer.analyze_with_optimize(fileName='../data/rawData_mi_stereo.csv', lowerBound=300)
    SimpleEqualizer.white_noise_test()