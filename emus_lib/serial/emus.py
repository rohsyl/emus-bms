import serial
import serial.tools.list_ports
import threading
from library.byteutil import *
from config.config import *
from emus_lib.helpers import *
from emus_lib.sentence.builder import Builder

'''
This class will provide a interface to communicate with an EMUS BMS through Serial
'''


class EmusSerial:
    '''
    Constructor
    :param port_name The name of the port. Eg: /dev/ttyUSB1
    :param filter_response Fetch only the sentence in this list
    :param sentence_response_definition Define the length of response
    '''

    def __init__(self, port_name=None, filter_response=None, sentence_response_definition=None):
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

    def get_port_name(self):
        vid = EMUS_SERIAL_VID
        pid = EMUS_SERIAL_PID

        device_list = serial.tools.list_ports.comports()

        port = None
        for device in device_list:
            if (device.vid != None or device.pid != None):
                if ('{:04X}'.format(device.vid) == vid and
                        '{:04X}'.format(device.pid) == pid):
                    port = device.device
                    if self.logger is not None:
                        self.logger.info('Port found %s with vid and %s pid %s', port, vid, pid)
                    break
                port = None

        if port is None:
            if self.logger is not None:
                self.logger.info('Port not found with vid and %s pid %s', vid, pid)

        return port

    def set_logger(self, name):
        self.logger = get_logger(name)

    def set_queue(self, q):
        self.q = q

    def open(self):

        if self.port_name is None:
            self.port_name = self.get_port_name()

        if self.logger is not None:
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
        if self.logger is not None:
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

            if self.logger is not None:
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
                    if self.logger is not None:
                        self.logger.log(LOG_LEVEL_DEBUG_DEEPER, 'Bytes red : ' + value + " " + str(raw))

                except serial.SerialException as e:
                    # no new data
                    if self.logger is not None:
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
                                    if self.logger is not None:
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
            if self.logger is not None:
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

            if self.logger is not None:
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
                    if self.logger is not None:
                        self.logger.log(LOG_LEVEL_DEBUG_DEEPER, 'Bytes red : ' + value + " " + str(raw))

                except serial.SerialException as e:
                    # no new data
                    if self.logger is not None:
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
                                    if self.logger is not None:
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
                                # sometimes the package is corrupted and we get more field than expected
                                # is this case an exception is thrown when we try to convert
                                # the CSR from char array to int
                                # so we catch this error, log it and ignore this package
                                try:
                                    builder.setCsr(int(''.join(map(chr, _csr)), 16))
                                    sm = builder.getSentenceManager()
                                    thread = threading.Thread(target=self.__handle, args=[sm])
                                    thread.start()
                                except Exception as e:
                                    if self.logger is not None:
                                        self.logger.exception('invalid package, ignored')
                                        self.logger.exception(e)

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
            if self.logger is not None:
                self.logger.exception('Error occurred')

    def write(self, sentence):
        if self.logger is not None:
            self.logger.info('Serial write %s', sentence)
        request = sentence + ',?,'
        request += int_to_hex_string(crc_checksum(request))
        head = self.__get_head()
        out = bytearray(head + char_to_bytes(request) + head)
        self.serial.write(out)
        if self.logger is not None:
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
                label = sm.getFieldLabel(i)
                v = None
                if words[i] is not None:
                    v = sm.getFieldFormat(i).formatValue(words[i])
                formatted_values[label] = v

            out = {
                'name': sm.getSentenceName(),
                'values': formatted_values
            }

            if self.logger is not None:
                self.logger.info('Package red %s', sm.getSentenceName())
                self.logger.debug('Package red content %s', out)

            # i have to do something with this values formattedValues
            # if blocking:
            #    return out

            if self.q is not None:
                self.q.put(sm.getSentenceName(), out)

        else:
            if self.logger is not None:
                self.logger.warning('Invalid package %s, Wrong CSR', sm.getSentenceName())
                self.logger.debug('Package string : %s', s_string)
                self.logger.debug('CSR from package : %s', sm.getCsr())
                self.logger.debug('CSR computed : %s', csr)
