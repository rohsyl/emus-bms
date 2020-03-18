from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class BV1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'NUMBER OF CELLS',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'MIN CELL VOLTAGE',
                                  'format': HexDec(200, 0.01, 'V')
                              },
                              {
                                  'label': 'MAX CELL VOLTAGE',
                                  'format': HexDec(200, 0.01, 'V')
                              },
                              {
                                  'label': 'AVERAGE CELL VOLTAGE',
                                  'format': HexDec(200, 0.01, 'V')
                              },
                              {
                                  'label': 'TOTAL VOLTAGE',
                                  'format': HexDec(0, 0.01, 'V')
                              },
                              {
                                  'label': 'Empty field',
                                  'format': Format()
                              },
                          ])