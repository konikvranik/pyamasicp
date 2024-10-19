import logging
import socket
import unittest
from unittest.mock import patch

from pyamasicp import commands
from pyamasicp.client import Client
from pyamasicp.commands import Commands

logging.basicConfig(level=logging.DEBUG)

REQUESTS = {
    b'\xa6\x01\x00\x00\x00\x05\x01\x44\x00\x16\xf1': b'\x21\x01\x00\x00\x04\x01\x00\x00\x25',
    b'\xa6\x01\x00\x00\x00\x03\x01\x45\xe0': b'\x21\x01\x00\x00\x05\x01\x45\x16\x16\x61',
    b'\xa6\x01\x00\x00\x00\x03\x01\x19\xbc': b'\x21\x01\x00\x00\x04\x01\x19\x02\x3e',
}


def _mock_remote_call(self, _socket, message):
    return REQUESTS[message]


def _mock_socket(self):
    return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


class TestClient(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        # Test data
        self._id = b'\x01'

    @patch.object(Client, '_create_and_connect_socket', side_effect=_mock_socket, autospec=True)
    @patch.object(Client, '_call_remote', side_effect=_mock_remote_call, autospec=True)
    def test_client(self, mocked_create_and_connect_socket, mocked_call_remote):
        # Positive test case
        cl = Client('test.host', mac="00:00:00:00:00:00")
        result = cl.send(self._id, commands.CMD_GET_POWER_STATE)
        self.assertEqual(b'\x02', result)
        mocked_call_remote.assert_called_with(cl)


class TestCommand(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        # Test data
        self._id = b'\x01'

    @patch.object(Client, '_create_and_connect_socket', side_effect=_mock_socket, autospec=True)
    @patch.object(Client, '_call_remote', side_effect=_mock_remote_call, autospec=True)
    def test_get_power_state(self, mocked_create_and_connect_socket, mocked_call_remote):
        # Positive test case
        cmd = Commands(Client('test.host', mac="00:00:00:00:00:00"), self._id)
        result = cmd.get_power_state()
        self.assertEqual(True, result)


if __name__ == "__main__":
    unittest.main()
