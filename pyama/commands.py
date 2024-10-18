from pyama.client import Client

POWER_OFF = b'\x01'
POWER_ON = b'\x02'


class Commands:

    def __init__(self, client: Client, id=b'\x01'):
        self._client = client
        self._id = id

    def get_power_state(self):
        match self._client.send(self._id, b'\x19'):
            case b'\x01':
                return False
            case b'\x02':
                return True
            case _:
                raise CommandException("Unknown power state")

    def set_power_state(self, state: bool):
        self._client.send(self._id, b'\x18', POWER_ON if state else POWER_OFF)


class CommandException(Exception):
    pass
