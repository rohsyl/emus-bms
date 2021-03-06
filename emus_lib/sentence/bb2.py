from .sentence import Sentence
from emus_lib.format.format import HexDec, Format, HexDecByteArray


class BB2(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'CELL STRING NUMBER',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'CELL NUMBER OF FIRST CELL IN GROUP',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'SIZE OF GROUP',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'INDIVIDUAL CELL MODULE BALANCING RATE',
                                  'format': HexDecByteArray(0, 100/255, '%')
                              },
                          ])