
from library.byteutil import *
import importlib
from emus_lib.constants import *
from emus_lib.helpers import util_class_instanciate

class Builder:

    def __init__(self, sentence):
        #print('Sentence name : ' + sentence)
        self.sentence = sentence
        self.sentenceManager = self.__instantiateSentenceManager()

        self.count = -1


    def __instantiateSentenceManager(self):
        # instantiate the corresponding sentence manager
        print(self.sentence)
        sentence_def = SENTENCES_DEFINITION.get(self.sentence)
        instance = util_class_instanciate(sentence_def)
        instance.setSentenceName(self.sentence)
        return instance


    def readByte(self, byte):

        if byte == SEPARATOR:
            self.count += 1
        else:
            self.sentenceManager.appendByteToWord(self.count, byte)

        # return true if all bytes are red
        # return false if there is more bytes to read
        return self.sentenceManager.isEnd(self.count)

    def setCsr(self, byte):
        self.sentenceManager.setCsr(byte)

    def getSentenceManager(self):
        return self.sentenceManager