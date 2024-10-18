import binascii
import functools
import logging
import socket
import sys

TCP_IP = 'iiyama.home'
TCP_PORT = 5000
BUFFER_SIZE = 1024

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handlers
stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

# Set levels for handlers
stdout_handler.setLevel(logging.INFO)
stderr_handler.setLevel(logging.WARNING)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)

# Create a socket with a timeout
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)  # Timeout after 5 seconds

try:
    s.connect((TCP_IP, TCP_PORT))
except socket.error as e:
    logger.error(f"Connection error: {e}")
    s.close()
    exit(1)


def send(id: bytes, command: bytes, data: bytes):
    HEADER = b'\xA6'
    CATEGORY = b'\x00'
    CODE0 = b'\x00'
    CODE1 = b'\x00'
    DATA_CONTROL = b'\x01'

    data = command + data
    length = (len(data) + 2).to_bytes(1, byteorder='big')  # Převést délku na jeden byte
    message = b''.join([HEADER, id, CATEGORY, CODE0, CODE1, length, DATA_CONTROL, data])
    checksum = calculate_checksum(message)
    message += checksum

    try:
        logger.debug("id: %s" % binascii.hexlify(id))
        logger.debug("function: %s" % binascii.hexlify(CODE1))
        logger.debug("length: %s" % binascii.hexlify(length))
        logger.debug("data: %s" % binascii.hexlify(data))
        logger.debug("checksum: %s" % binascii.hexlify(checksum))
        logger.debug(" request: %s" % binascii.hexlify(message))

        s.sendall(message)
        response_data = s.recv(
            BUFFER_SIZE)  # This will raise a timeout exception if no data is received within 5 seconds
        logger.debug("     response: %s" % binascii.hexlify(response_data))

        length = len(response_data)

        checksum_data = response_data[:-1]
        logger.debug("checksum data: %s" % binascii.hexlify(checksum_data))
        checksum = calculate_checksum(checksum_data)

        header = response_data[0]
        response_data = response_data[1:]
        response_id = response_data[0]
        response_data = response_data[1:]
        category = response_data[0]
        response_data = response_data[1:]
        page = response_data[0]
        response_data = response_data[1:]
        response_length = response_data[0] - 2
        response_data = response_data[1:]
        control = response_data[0]
        response_data = response_data[1:]
        response_command = response_data[0]
        response_data = response_data[1:]

        logger.debug("header: 0x%02x" % header)
        logger.debug("id: 0x%02x" % response_id)
        logger.debug("category: 0x%02x" % category)
        logger.debug("code0: 0x%02x" % page)
        logger.debug("length: %d / %d" % (response_length, length))
        logger.debug("control: 0x%02x" % control)

        result = response_data[0:response_length - 1]
        response_data = response_data[response_length - 1:]

        response_checksum = response_data[0]

        logger.debug("command: 0x%02x" % response_command)

        assert header == 0x21
        assert id[0] == response_id
        assert category == 0x00
        assert page == 0x00
        assert control == 0x01

        if response_command == 0x00:
            match result:
                case b'\x00':
                    pass
                case b'\x01':
                    logger.error("Limit Over; The packets was received normally, but the data value was; over the upper limit.")
                case b'\x02':
                    logger.error("Limit Over; The packets was received normally, but the data value was; over the lower limit.")
                case b'\x03':
                    logger.error("Command canceled; The packet is received normally but either the value of data is; incorrect or request is not permitted for the current host; value.")
                case b'\x04':
                    logger.error("Parse Error; Received not defined format data or check sum Error.")
                case _:
                    logger.error("Unexpected Error; Received unexpected error %s." % binascii.hexlify(result))
        else:
            assert response_command == command[0], "Command doesn't match. Expected 0x%02x, got 0x%02x" % (
                command[0], response_command)

            logger.info("data: %s -> %s" % (binascii.hexlify(result), result.decode('utf-8') if result else ""))

        logger.debug("checksum: 0x%02x / %s" % (response_checksum, binascii.hexlify(checksum)))

        assert checksum[0] == response_checksum



    except socket.timeout:
        logger.error("Socket timeout, no response received from the server.")
    except socket.error as e:
        logger.error(f"Socket error: {e}")
    finally:
        s.close()

def calculate_checksum(message):
    return bytes([functools.reduce(lambda a, b: a ^ b, list(message))])


send(b'\x01', b'\x18', b'\x01')


# send(b'\x01', b'\xA2', b'\x01')
#send(b'\x01', b'\xAC', b'\x00\x18\x01\x00')

#send(b'\x01', b'\x44', b'\100\20')
