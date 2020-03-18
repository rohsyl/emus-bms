from library.byteutil import *
import math


class Format:

    def __init__(self, unit=None):
        self.unit = unit

    def formatValue(self, value):
        return None

    def getUnit(self):
        return self.unit


class HexDec(Format):

    def __init__(self, offset, multiplier, unit=None, signed=False):
        Format.__init__(self, unit)
        self.offset = offset
        self.multiplier = multiplier
        self.signed = signed

    def formatValue(self, value):
        return (value + self.offset) * self.multiplier


class HexDecByteArray(Format):

    def __init__(self,  offset, multiplier, unit=None):
        Format.__init__(self, unit)
        self.offset = offset
        self.multiplier = multiplier

    def formatValue(self, value):
        array = []
        value = self.split(value, 2)
        if value is not None:

            for v in value:
                string = ''.join(v)
                intValue = int(string, 16)
                array.append((intValue + self.offset) * self.multiplier)
        return array

    def split(self, arr, size):
        arrs = []
        while len(arr) > size:
            pice = arr[:size]
            arrs.append(pice)
            arr = arr[size:]
        arrs.append(arr)
        return arrs


class Str(Format):

    def __init__(self):
        Format.__init__(self, None)

    def formatValue(self, value):
        return value


class HexBitBool(Format):

    def __init(self):
        Format.__init__(self, None)

    def formatValue(self, value):
        return value
