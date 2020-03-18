from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class BB1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'NUMBER OF CELLS',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'MIN CELL BALACING RATE',
                                  'format': HexDec(0, 100/255, '%')
                              },
                              {
                                  'label': 'MAX CELL BALANCING RATE',
                                  'format': HexDec(0, 100/255, '%')
                              },
                              {
                                  'label': 'AVERAGE CELL BALANCING RATE',
                                  'format': HexDec(0, 100/255, '%')
                              },
                              {
                                  'label': 'Empty field',
                                  'format': Format()
                              },
                              {
                                  'label': 'BALANCING VOLTAGE THRESHOLF',
                                  'format': HexDec(200, 0.01, 'V')
                              },
                          ])