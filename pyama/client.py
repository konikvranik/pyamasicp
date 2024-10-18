import binascii
import functools
import logging
import socket

import wakeonlan
from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp

HEADER = b'\xA6'
CATEGORY = b'\x00'
CODE0 = b'\x00'
CODE1 = b'\x00'
DATA_CONTROL = b'\x01'


def calculate_checksum(message):
    return bytes([functools.reduce(lambda a, b: a ^ b, list(message))])


def get_mac_address(ip):
    # Create an ARP request frame
    arp_request = ARP(pdst=ip)

    # Create an Ethernet frame to broadcast the ARP request
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Stack them together (Ethernet frame + ARP request)
    arp_request_broadcast = broadcast / arp_request

    # Send the packet and capture the response
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    # Check if we received any response
    if answered_list:
        # The second element of the tuple is the response packet, "hwsrc" has the MAC address
        return answered_list[0][1].hwsrc
    else:
        return None


class Client:

    def __init__(self, host, port=5000, timeout=5, buffer_size=1024, mac=None, wol_target=None):
        self._wol_target = wol_target
        self._host = host
        self._port = port
        self._mac = get_mac_address(self._host) if mac is None else mac
        self._logger = logging.getLogger(self.__class__.__name__)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(timeout)
        self._buffer_size = buffer_size  # Timeout after 5 seconds

        try:
            self._socket.connect((host, port))
        except socket.error as e:
            self._logger.error(f"Connection error: {e}")
            self._socket.close()
            exit(1)

    def wake_on_lan(self):
        wakeonlan.send_magic_packet(self._mac,
                                    ip_address=self._wol_target if ':' in self._wol_target else wakeonlan.BROADCAST_IP)

    def send(self, id: bytes, command: bytes, data: bytes = b''):

        data = command + data
        length = (len(data) + 2).to_bytes(1, byteorder='big')  # Převést délku na jeden byte
        message = b''.join([HEADER, id, CATEGORY, CODE0, CODE1, length, DATA_CONTROL, data])
        checksum = calculate_checksum(message)
        message += checksum

        try:
            self._logger.debug("id: %s" % binascii.hexlify(id))
            self._logger.debug("function: %s" % binascii.hexlify(CODE1))
            self._logger.debug("length: %s" % binascii.hexlify(length))
            self._logger.debug("data: %s" % binascii.hexlify(data))
            self._logger.debug("checksum: %s" % binascii.hexlify(checksum))
            self._logger.debug(" request: %s" % binascii.hexlify(message))

            self._socket.sendall(message)
            response_data = self._socket.recv(self._buffer_size)
            self._logger.debug("     response: %s" % binascii.hexlify(response_data))

            length = len(response_data)

            checksum_data = response_data[:-1]
            self._logger.debug("checksum data: %s" % binascii.hexlify(checksum_data))
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

            self._logger.debug("header: 0x%02x" % header)
            self._logger.debug("id: 0x%02x" % response_id)
            self._logger.debug("category: 0x%02x" % category)
            self._logger.debug("code0: 0x%02x" % page)
            self._logger.debug("length: %d / %d" % (response_length, length))
            self._logger.debug("control: 0x%02x" % control)

            result = response_data[0:response_length - 1]
            response_data = response_data[response_length - 1:]

            response_checksum = response_data[0]

            self._logger.debug("command: 0x%02x" % response_command)
            self._logger.debug("checksum: 0x%02x / %s" % (response_checksum, binascii.hexlify(checksum)))

            assert header == 0x21
            assert id[0] == response_id
            assert category == 0x00
            assert page == 0x00
            assert control == 0x01
            assert checksum[0] == response_checksum

            if response_command == 0x00:
                match result:
                    case b'\x00':
                        return None
                    case b'\x01':
                        self._logger.error(
                            "Limit Over; The packets was received normally, but the data value was; over the upper limit.")
                    case b'\x02':
                        self._logger.error(
                            "Limit Over; The packets was received normally, but the data value was; over the lower limit.")
                    case b'\x03':
                        self._logger.error(
                            "Command canceled; The packet is received normally but either the value of data is; incorrect or request is not permitted for the current host; value.")
                    case b'\x04':
                        self._logger.error("Parse Error; Received not defined format data or check sum Error.")
                    case _:
                        self._logger.error("Unexpected Error; Received unexpected error %s." % binascii.hexlify(result))
            else:
                assert response_command == command[0], "Command doesn't match. Expected 0x%02x, got 0x%02x" % (
                    command[0], response_command)

                self._logger.info(
                    "data: %s -> %s" % (binascii.hexlify(result), result.decode('utf-8') if result else ""))
                return result

            return None

        except socket.timeout:
            self._logger.error("Socket timeout, no response received from the server.")
        except socket.error as e:
            self._logger.error(f"Socket error: {e}")
        finally:
            self._socket.close()
