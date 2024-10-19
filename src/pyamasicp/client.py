import binascii
import functools
import logging
import socket
import threading
from time import sleep

import getmac
import wakeonlan

HEADER = b'\xA6'
CATEGORY = b'\x00'
CODE0 = b'\x00'
CODE1 = b'\x00'
DATA_CONTROL = b'\x01'


def calculate_checksum(message):
    return bytes([functools.reduce(lambda a, b: a ^ b, list(message))])


def _prepare_message(id, command, data):
    data = command + data
    length = (len(data) + 2).to_bytes(1, byteorder='big')
    message = b''.join([HEADER, id, CATEGORY, CODE0, CODE1, length, DATA_CONTROL, data])
    checksum = calculate_checksum(message)
    return message + checksum


class Client:

    def __init__(self, host, port=5000, timeout=.5, wake_delay=7, retries=20, buffer_size=1024, mac=None,
                 wol_target=None):
        self._lock = threading.Lock()
        self._wake_delay = wake_delay
        self._retries = retries
        self._timeout = timeout
        self._wol_target = wol_target
        self._host = host
        self._port = port
        self._mac = mac if mac else getmac.get_mac_address(ip=self._host, hostname=self._host)
        self._logger = logging.getLogger(self.__class__.__qualname__)
        self._buffer_size = buffer_size  # Timeout after 5 seconds
        self._logger.debug(
            'host: %s:%d, mac: %s, wol_target: %s' % (self._host, self._port, self._mac, self._wol_target))

    def wake_on_lan(self):
        target_ip = wakeonlan.BROADCAST_IP if self._wol_target is None else self._wol_target
        self._logger.debug('Waking on LAN %s using %s' % (self._mac, target_ip))
        wakeonlan.send_magic_packet(self._mac, ip_address=target_ip)

    def send(self, id: bytes, command: bytes, data: bytes = b''):
        with self._lock:
            _socket = self._create_and_connect_socket()
            if _socket:
                try:
                    message = _prepare_message(id, command, data)
                    self._log_debug_request(id, message, data)
                    recv = self._call_remote(_socket, message)
                    return self._process_response(id, command, recv)
                except socket.timeout:
                    self._logger.error("Socket timeout, no response received from the server.")
                except socket.error as e:
                    self._logger.error(f"Socket error: {e}")
                finally:
                    _socket.close()

    def _call_remote(self, _socket, message):
        _socket.sendall(message)
        recv = _socket.recv(self._buffer_size)
        return recv

    def _create_and_connect_socket(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(self._timeout)
        for _ in range(self._retries):
            try:
                _socket.connect((self._host, self._port))
                return _socket
            except socket.error:
                self.wake_on_lan()
                sleep(self._wake_delay)
        self._logger.error("Connection error")
        _socket.close()
        return None

    def _process_response(self, id, command, response_data):

        length = len(response_data)
        checksum_data = response_data[:-1]
        checksum = calculate_checksum(checksum_data)
        header = response_data[0]
        response_id = response_data[1]
        category = response_data[2]
        page = response_data[3]
        response_length = response_data[4] - 2
        control = response_data[5]
        response_command = response_data[6]
        result = response_data[7:7 + response_length - 1]
        response_checksum = response_data[7 + response_length - 1]
        self._log_debug_response(category, checksum, control, header, length, page, response_checksum, response_command,
                                 response_id, response_length, response_data)

        assert header == 0x21
        assert id[0] == response_id
        assert category == 0x00
        assert page == 0x00
        assert control == 0x01
        assert checksum[0] == response_checksum

        if response_command == 0x00:
            response_map = {
                b'\x00': None,
                b'\x01': "Limit Over; The packet was received normally, but the data value was over the upper limit.",
                b'\x02': "Limit Over; The packet was received normally, but the data value was over the lower limit.",
                b'\x03': "Command canceled; The packet was received normally but either the value of data is incorrect or request is not permitted for the current host value.",
                b'\x04': "Parse Error; Received not defined format data or checksum Error."
            }
            error_message = response_map.get(result,
                                             "Unexpected Error; Received unexpected error %s." % binascii.hexlify(
                                                 result))
            if error_message:
                self._logger.error(error_message)
            return result if result == b'\x00' else None
        else:
            assert response_command == command[0], "Command doesn't match. Expected 0x%02x, got 0x%02x" % (
                command[0], response_command)
            self._logger.info("data: %s -> %s" % (binascii.hexlify(result), result.decode('utf-8') if result else ""))
            return result

    def _log_debug_response(self, category, checksum, control, header, length, page, response_checksum,
                            response_command, response_id, response_length, response_data):
        self._logger.debug("     response: %s" % binascii.hexlify(response_data))
        self._logger.debug("header: 0x%02x" % header)
        self._logger.debug("id: 0x%02x" % response_id)
        self._logger.debug("category: 0x%02x" % category)
        self._logger.debug("code0: 0x%02x" % page)
        self._logger.debug("length: %d / %d" % (response_length, length))
        self._logger.debug("control: 0x%02x" % control)
        self._logger.debug("command: 0x%02x" % response_command)
        self._logger.debug("checksum: 0x%02x / %s" % (response_checksum, binascii.hexlify(checksum)))

    def _log_debug_request(self, id, message, data):
        checksum = message[-1]
        self._logger.debug("id: %s" % binascii.hexlify(id))
        self._logger.debug("function: %s" % binascii.hexlify(CODE1))
        self._logger.debug("length: %s" % binascii.hexlify(data[:1]))
        self._logger.debug("data: %s" % binascii.hexlify(data))
        self._logger.debug("checksum: %s" % binascii.hexlify(bytes([checksum])))
        self._logger.debug(" request: %s" % binascii.hexlify(message))
