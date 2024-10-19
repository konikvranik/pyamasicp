import binascii

from pyamasicp.client import Client

CMD_SET_POWER_STATE = b'\x18'
CMD_GET_POWER_STATE = b'\x19'
CMD_SET_VOLUME = b'\x44'
CMD_GET_VOLUME = b'\x45'
CMD_SET_INPUT_SOURCE = b'\xAC'
CMD_GET_INPUT_SOURCE = b'\xAD'
CMD_IR = b'\xDB'

VAL_POWER_OFF = b'\x01'
VAL_POWER_ON = b'\x02'

IR_POWER = b'\xA0'
IR_MENU = b'\xA1'
IR_INPUT = b'\xA2'
IR_VOL_UP = b'\xA3'
IR_VOL_DOWN = b'\xA4'
IR_MUTE = b'\xA5'
IR_CURSOR_UP = b'\xA6'
IR_CURSOR_DOWN = b'\xA7'
IR_CURSOR_LEFT = b'\xA8'
IR_CURSOR_RIGHT = b'\xA9'
IR_OK = b'\xB1'
IR_RETURN = b'\xB2'
IR_RED = b'\xC1'
IR_GREEN = b'\xC2'
IR_YELLOW = b'\xC3'
IR_BLUE = b'\xC4'
IR_FORMAT = b'\xD1'
IR_INFO = b'\xD2'
IR_BTN_0 = b'\x00'
IR_BTN_1 = b'\x01'
IR_BTN_2 = b'\x02'
IR_BTN_3 = b'\x03'
IR_BTN_4 = b'\x04'
IR_BTN_5 = b'\x05'
IR_BTN_6 = b'\x06'
IR_BTN_7 = b'\x07'
IR_BTN_8 = b'\x08'
IR_BTN_9 = b'\x09'

INPUT_SOURCES = {
    "VIDEO": b'\x00',
    "Display Port": b'\x01',
    "S-VIDEO": b'\x02',
    "COMPONENT": b'\x03',
    "VGA": b'\x05',
    "HDMI 2": b'\x06',
    "Display Port 2": b'\x07',
    "USB 2": b'\x08',
    "Card DVI-D": b'\x09',
    "Display Port 1": b'\x0A',
    "Card OPS": b'\x0B',
    "USB 1": b'\x0C',
    "HDMI 1": b'\x0D',
    "DVI-D": b'\x0E',
    "HDMI 3": b'\x0F',
    "BROWSER": b'\x10',
    "SMARTCMS": b'\x11',
    "DMS (Digital Media Server)": b'\x12',
    "INTERNAL STORAGE": b'\x13',
    "Reserved": b'\x14',
    "Media Player": b'\x16',
    "PDF Player": b'\x17',
    "Custom": b'\x18',
    "HDMI 4": b'\x19',
}


class Commands:

    def __init__(self, client: Client, id=b'\x01'):
        self._client = client
        self._id = id

    def get_power_state(self):
        result = self._client.send(self._id, CMD_GET_POWER_STATE)
        match result:
            case b'\x01':
                return False
            case b'\x02':
                return True
            case _:
                raise CommandException("Unknown power state: %s" % binascii.hexlify(result))

    def set_power_state(self, state: bool):
        self._client.send(self._id, CMD_SET_POWER_STATE, VAL_POWER_ON if state else VAL_POWER_OFF)

    def get_volume(self):
        result = [b for b in self._client.send(self._id, CMD_GET_VOLUME)]
        result.reverse()
        return result

    def set_volume(self, volume=0, output_volume=0):
        self._client.send(self._id, CMD_SET_VOLUME, bytearray([volume, output_volume, 0, 0]))

    def get_input_source(self):
        return [b for b in self._client.send(self._id, CMD_GET_INPUT_SOURCE)]

    def set_input_source(self, input_type=0, input_number=0, osd_style=0, reserved=0):
        self._client.send(self._id, CMD_SET_INPUT_SOURCE, bytearray([input_type, input_number, osd_style, reserved]))

    def ir_command(self, code):
        self._client.send(self._id, CMD_IR, code)


class CommandException(Exception):
    pass
