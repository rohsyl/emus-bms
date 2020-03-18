import serial
import threading
from library.byteutil import *
from emus_lib.constants import *
from emus_lib.helpers import *
from emus_lib.sentence.builder import Builder

class EmusSerial:

    def __init__(self, port_name, filter_response=None, sentence_response_definition=None):
        self.serial = None
        self.port_name = port_name
        self.baudrate = 57600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.timeout = 1
        self.connected = False

        self.filter_response = filter_response
        self.sentence_response_definition = sentence_response_definition
        self.q = None

        self.logger = None

    def set_logger(self, name):
        self.logger = get_logger(name)

    def set_queue(self, q):
        self.q = q

    def open(self):
        self.logger.info('Open serial to %s', self.port_name)
        self.serial = serial.Serial(
            port=self.port_name,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=self.timeout
        )
        self.connected = True
        return self.serial.isOpen()

    def close(self):
        self.connected = False
        self.serial.close()
        self.logger.info('Close serial to %s', self.port_name)

    def read(self, blocking=True):
        try:
            # init variables for sentence reading
            sentence_name = []
            _csr = []
            is_cr = False
            is_lf = False
            is_sentence_name = False
            is_package = False
            is_package_reading = False
            is_csr = False
            builder = None
            length = 0

            self.logger.info('Listening...')
            while self.connected:
                try:
                    # read input byte by byte
                    debug = False
                    if debug:
                        print(sentence_name)
                        print(_csr)
                        print(is_cr)
                        print(is_lf)
                        print(is_sentence_name)
                        print(is_package)
                        print(is_package_reading)
                        print(is_csr)
                        print(builder)
                    raw = self.serial.read()

                    value = bytes_to_hexstring(raw)
                    self.logger.log(LOG_LEVEL_DEBUG_DEEPER, 'Bytes red : ' + value + " " + str(raw))

                except serial.SerialException as e:
                    # no new data
                    self.logger.exception('Error occurred')
                    self.serial.close()
                    exit()
                else:
                    # convert raw input to byte
                    byte = int.from_bytes(raw, byteorder='big')

                    if is_sentence_name is False:
                        if length == 0:
                            sentence_name = []
                            length = LEN_SENTENCE_NAME
                        if length > 0:
                            length -= 1
                            sentence_name.append(byte)
                            if length == 0:
                                sentence_name_string = bytes_to_string(sentence_name)
                                is_sentence_name = True
                                # get only sentences that are in the SEN_ONLY array
                                if self.filter_response is not None \
                                        and sentence_name_string not in self.filter_response:
                                    self.logger.debug('Sentence %s is not in SEN_ONLY -> sentence ignored.',
                                                 sentence_name_string)
                                    # reset
                                    sentence_name = []
                                    _csr = []
                                    is_cr = False
                                    is_lf = False
                                    is_sentence_name = False
                                    is_package = False
                                    is_package_reading = False
                                    is_csr = False
                                    builder = None
                                    length = 0

                    elif is_package is False:
                        if is_package_reading is False:
                            builder = Builder(bytes_to_string(sentence_name))
                            is_package_reading = True

                        if is_package_reading:
                            # read byte per byte the sentence
                            result = builder.readByte(byte)

                            # if we are at the end of the sentence
                            if result:
                                is_package_reading = False
                                is_package = True

                    elif is_csr is False:
                        if length == 0:
                            _csr = []
                            length = LEN_CSR
                        if length > 0:
                            length -= 1
                            _csr.append(byte)
                            if length == 0:
                                is_csr = True
                                builder.setCsr(int(''.join(map(chr, _csr)), 16))

                    if is_cr is False:
                        if byte == CR:
                            is_cr = True

                    elif is_lf is False:
                        if byte == LF:
                            sm = builder.getSentenceManager()
                            thread = threading.Thread(target=self.__handle, args=[sm])
                            thread.start()

                            sentence_name = []
                            _csr = []
                            is_cr = False
                            is_lf = False
                            is_sentence_name = False
                            is_package = False
                            is_package_reading = False
                            is_csr = False
                            builder = None
                            length = 0

        except Exception as e:
            self.logger.exception('Error occurred')

    def read_broadcast(self, blocking=True):
        try:
            # init variables for sentence reading
            sentence_name = []
            _csr = []
            is_cr = False
            is_lf = False
            is_sentence_name = False
            is_package = False
            is_package_reading = False
            is_csr = False
            builder = None
            length = 0
            wait_for_eol = False

            self.logger.info('Listening...')
            while self.connected:
                try:
                    # read input byte by byte
                    debug = False
                    if debug:
                        print(sentence_name)
                        print(_csr)
                        print(is_cr)
                        print(is_lf)
                        print(is_sentence_name)
                        print(is_package)
                        print(is_package_reading)
                        print(is_csr)
                        print(builder)
                    raw = self.serial.read()

                    value = bytes_to_hexstring(raw)
                    self.logger.log(LOG_LEVEL_DEBUG_DEEPER, 'Bytes red : ' + value + " " + str(raw))

                except serial.SerialException as e:
                    # no new data
                    self.logger.exception('Error occurred')
                    self.serial.close()
                    exit()
                else:
                    # convert raw input to byte
                    byte = int.from_bytes(raw, byteorder='big')
                    if is_cr is False:
                        if byte == CR:
                            is_cr = True

                    elif is_lf is False:
                        if byte == LF:
                            is_lf = True

                    elif is_sentence_name is False:
                        if length == 0:
                            sentence_name = []
                            length = LEN_SENTENCE_NAME
                        if length > 0:
                            length -= 1
                            sentence_name.append(byte)
                            if length == 0:
                                sentence_name_string = bytes_to_string(sentence_name)
                                is_sentence_name = True
                                # get only sentences that are in the SEN_ONLY array
                                if self.filter_response is not None \
                                        and sentence_name_string not in self.filter_response:
                                    self.logger.debug('Sentence %s is not in SEN_ONLY -> sentence ignored.', sentence_name_string)

                                    # reset
                                    sentence_name = []
                                    _csr = []
                                    is_cr = False
                                    is_lf = False
                                    is_sentence_name = False
                                    is_package = False
                                    is_package_reading = False
                                    is_csr = False
                                    builder = None
                                    length = 0

                    elif is_package is False:
                        if is_package_reading is False:
                            builder = Builder(bytes_to_string(sentence_name))
                            is_package_reading = True

                        if is_package_reading:
                            # read byte per byte the sentence
                            result = builder.readByte(byte)

                            # if we are at the end of the sentence
                            if result:
                                is_package_reading = False
                                is_package = True

                    elif is_csr is False:
                        if length == 0:
                            _csr = []
                            length = LEN_CSR
                        if length > 0:
                            length -= 1
                            _csr.append(byte)
                            if length == 0:
                                is_csr = True
                                builder.setCsr(int(''.join(map(chr, _csr)), 16))
                                print(builder.getSentenceManager().getSentenceString())
                                sm = builder.getSentenceManager()

                                thread = threading.Thread(target=self.__handle, args=[sm])
                                thread.start()

                                sentence_name = []
                                _csr = []
                                is_cr = False
                                is_lf = False
                                is_sentence_name = False
                                is_package = False
                                is_package_reading = False
                                is_csr = False
                                builder = None
                                length = 0


        except Exception as e:
            self.logger.exception('Error occurred')

    def write(self, sentence):
        self.logger.info('Serial write %s', sentence)
        request = sentence + ',?,'
        request += int_to_hex_string(crc_checksum(request))
        head = self.__get_head()
        out = bytearray(head + char_to_bytes(request) + head)
        self.serial.write(out)
        self.logger.debug('Package sent %s', out)

    def __get_head(self):
        return [CR, LF]

    def __handle(self, sm):
        words = sm.getWordsAsciiToHex()
        s_string = sm.getSentenceString()
        csr = crc_checksum(s_string)

        if csr == sm.getCsr():

            sentence_length = len(sm.words)
            formatted_values = {}

            for i in range(0, sentence_length):
                v = sm.getFieldFormat(i).formatValue(words[i])
                label = sm.getFieldLabel(i)
                formatted_values[label] = v

            out = {
                'name': sm.getSentenceName(),
                'values': formatted_values
            }

            self.logger.info('Package red %s', sm.getSentenceName())
            self.logger.debug('Package red content %s', out)

            # i have to do something with this values formattedValues
            # if blocking:
            #    return out

            if self.q is not None:
                self.q.put(sm.getSentenceName(), out)

        else:
            self.logger.warning('Invalid package %s, Wrong CSR', sm.getSentenceName())
            self.logger.debug('Package string : %s', s_string)
            self.logger.debug('CSR from package : %s', sm.getCsr())
            self.logger.debug('CSR computed : %s', csr)