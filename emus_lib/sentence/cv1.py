from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class CV1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'TOTAL VOLTAGE',
                                  'format': HexDec(0, 0.01, 'V')
                              },
                              {
                                  'label': 'CURRENT',
                                  'format': HexDec(0, 0.1, 'A', signed=True)
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                          ])