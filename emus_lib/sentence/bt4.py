from .sentence import Sentence
from emus_lib.format.format import HexDec, Format, HexDecByteArray


class BT4(Sentence):

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
                                  'label': 'INDIVIDUAL CELL TEMPERATURES',
                                  'format': HexDecByteArray(-100, 1, '°C')
                              },
                          ])