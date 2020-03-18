from .sentence import Sentence
from emus_lib.format.format import HexDec, Format, HexBitBool


class OT1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'CHARGER',
                                  'format': HexBitBool()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              },
                              {
                                  'label': 'HEATER',
                                  'format': HexBitBool()
                              },
                              {
                                  'label': 'Reserved',
                                  'format': Format()
                              }
                          ])
