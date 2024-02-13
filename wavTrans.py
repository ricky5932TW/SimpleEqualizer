import sox


class WavTrans:
    def __init__(self, inputFile, outputFile, *args, **kwargs):
        super().__init__()
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.__args = args
        self.__kwargs = kwargs
        self.__tfm = sox.Transformer()
        self.__tfm.set_input_format(file_type='wav')
        self.__tfm.set_output_format(file_type='wav')
        self.__tfm.build(inputFile, outputFile)

if __name__ == '__main__':
    # test
    inputFile = 'audiocheck.net_whitenoisegaussian.wav'
    outputFile = 'audiocheck.net_whitenoisegaussian2.wav'
    WavTrans(inputFile, outputFile)
    print('done')


