from .sentence import Sentence
from emus_lib.format.format import HexDec, Str


class VR1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'HARDWARE TYPE',
                                  'format': Str()
                              },
                              {
                                  'label': 'SERIAL NUMBER',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'FIRMWARE VERSION',
                                  'format': Str()
                              },
                          ])