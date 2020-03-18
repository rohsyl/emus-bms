def bytes_to_int(bytes, reverse=True):
    result = 0
    if reverse:
        bytes.reverse()
    for b in bytes:
        result = result * 256 + int(b)

    return result


def int_to_bytes(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    # result.reverse()
    return result

def char_to_bytes(value):
    result = []

    for char in value:
        result.append(ord(char))

    return result

def bytes_to_hexstring(bytes):
    strhex = ""
    for val in bytes:
        strhex += " 0x" + format(val, 'x').zfill(2)
    return strhex


def int_to_hex_string(int):
    return format(int, 'X').zfill(2)

def byte_to_binstring(byte):
    return "0b" + format(byte, 'b').zfill(8)


def bytes_to_string(bytes):
    return "".join(map(chr, bytes))


def checksum(data):
    a = 0xFF
    b = 0
    for byte in data:
        a = (a + byte) % 0x100
        b = (b + a) % 0x100
    return [a, b]