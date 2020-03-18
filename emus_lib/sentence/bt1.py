from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class BT1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'NUMBER OF CELLS',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'MIN CELL MODULE TEMPERATURE',
                                  'format': HexDec(-100, 1, '°C')
                              },
                              {
                                  'label': 'MAX CELL MODULE TEMPERATURE',
                                  'format': HexDec(-100, 1, '°C')
                              },
                              {
                                  'label': 'AVERAGE CELL MODULE TEMPERATURE',
                                  'format': HexDec(-100, 1, '°C')
                              },
                              {
                                  'label': 'Empty field',
                                  'format': Format()
                              },
                          ])