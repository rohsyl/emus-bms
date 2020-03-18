from .sentence import Sentence
from emus_lib.format.format import HexDec, Format


class DT1(Sentence):

    def __init__(self):
        Sentence.__init__(self,
                          [
                              {
                                  'label': 'SPEED',
                                  'format': HexDec(0, 0.1)
                              },
                              {
                                  'label': 'DISTANCE SINCE CHARGE',
                                  'format': HexDec(0, 0.01)
                              },
                              {
                                  'label': 'MOMENTARY CONSUMPTION',
                                  'format': HexDec(0, 0.1)
                              },
                              {
                                  'label': 'ESTIMATED DISTANCE LEFT',
                                  'format': HexDec(0, 0.01)
                              },
                              {
                                  'label': 'LAST CHARGE ENERGY',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'LAST DISCHARGE ENERGY',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'LAST TRIP AVERAGE CONSUMPTION',
                                  'format': HexDec(0, 0.1)
                              },
                              {
                                  'label': 'ESTIMATED DISTANCE LEFT BASED ON LAST TRIP',
                                  'format': HexDec(0, 0.01)
                              },
                              {
                                  'label': 'AVERAGE DISCHARGE ENERGY',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'MAX DISCHARGE ENERGY',
                                  'format': HexDec(0, 1)
                              },
                              {
                                  'label': 'CURRENT TRIP AVERAGE CONSUMPTION',
                                  'format': HexDec(0, 0.1)
                              },
                              {
                                  'label': 'ESTIMATED DISTANCE LEFT BASED ON AVG CONSUMPTION',
                                  'format': HexDec(0, 0.01)
                              },
                          ])
