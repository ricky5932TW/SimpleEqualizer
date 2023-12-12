from SoundSynthesis import SoundSynthesis
from Target import Target


class SoundAnalyzer(SoundSynthesis, Target):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__stepResponse = None
        self.__frequencyResponse = None
        self.__filter = None
        self.__model = None
