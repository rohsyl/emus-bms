from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class BC1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'BATTERY_CHARGE',
                                  'format': HexDec(0, 1, 'C')
                              },
                              {
                                  'label': 'BATTERY CAPACITY',
                                  'format': HexDec(0, 1, 'C')
                              },
                              {
                                  'label': 'STATE OF CHARGE',
                                  'format': HexDec(0, 0.01, '%')
                              }
                          ])