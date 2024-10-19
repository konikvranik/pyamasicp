import logging
import socket
import unittest
from unittest.mock import patch

from pyamasicp import commands
from pyamasicp.client import Client

logging.basicConfig(level=logging.DEBUG)


def _mock_remote_call(self, _socket, message):
    return message


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
        result = cl.send(self._id, commands.GET_POWER_STATE_COMMAND)
        self.assertEqual(30, result)
        mocked_call_remote.assert_called_with(self._id, commands.GET_POWER_STATE_COMMAND)


if __name__ == "__main__":
    unittest.main()
