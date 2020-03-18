from emus_lib.format.format import Str, HexDec
import math

class Sentence:

    def __init__(self, sentence_description):
        self.sentence_description = sentence_description
        self.length = len(self.sentence_description)
        self.csr = None
        self.words = [None] * self.length

    def setSentenceName(self, sentence_name):
        self.sentence_name = sentence_name

    def getSentenceName(self):
        return self.sentence_name

    def getNumberOfFields(self):
        return self.length

    def getFieldFormat(self, fieldNumber):
        return self.sentence_description[fieldNumber]['format']

    def getFieldLabel(self, fieldNumber):
        return self.sentence_description[fieldNumber]['label']


    def appendByteToWord(self, fieldNumber, byte):
        if self.words[fieldNumber] is None:
            self.words[fieldNumber] = []

        self.words[fieldNumber].append(byte)

    def isEnd(self, count):
        return count == self.length

    def setCsr(self, csr):
        self.csr = csr

    def getCsr(self):
        return self.csr

    def getSentence(self):
        return self.words

    def getSentenceString(self):
        sentenceString = ''

        for part in self.words:

            if part is not None:
                for char in part:
                    sentenceString += chr(char)

            sentenceString += ','

        return self.sentence_name + ',' + sentenceString

    def getWordsAsciiToHex(self):
        #print(self.words)
        formated = []

        i = 0
        for word in self.words:
            if word is not None:
                string = ''.join(map(chr, word))
                if isinstance(self.getFieldFormat(i), HexDec):
                    if self.getFieldFormat(i).signed:
                        uintval = int(string, 16)
                        bits = 8 * (len(string) - 2)
                        if uintval >= math.pow(2, bits - 1):
                            uintval = int(0 - (math.pow(2, bits) - uintval))
                        formated.append(uintval)
                    else :
                        formated.append(int(string, 16))
                else:
                    formated.append(string)

            else:
                formated.append(None)
            i += 1

        return formated
