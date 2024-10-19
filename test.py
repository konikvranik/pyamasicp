import logging

from pyamasicp import client
from pyamasicp.commands import Commands, IR_VOL_UP, IR_VOL_DOWN, IR_OK
import getmac

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

HOST = 'iiyama.home'

logger.debug("MAC: %a" % getmac.get_mac_address(ip=HOST, hostname=HOST))

c = Commands(client.Client(HOST, mac="DC:62:94:25:02:B3"))
# c.set_power_state(True)

# c.set_volume(22)
# c.ir_command(IR_OK)
logger.info("Current volume level: %s" % (c.get_volume()))
input_source = c.get_input_source()
logger.info("Current input source: 0x%02X[%d]" % (input_source[0], input_source[1]))

c.set_input_source(0x18)
# c.get_power_state()


# c.send(b'\x01', b'\x18', b'\x01')

# send(b'\x01', b'\xA2', b'\x01')
# send(b'\x01', b'\xAC', b'\x00\x18\x01\x00')

# send(b'\x01', b'\x44', b'\100\20')


# HDMI1:    0x0d[0]
# HDMI2:    0x06[0]
# HDMI3:    0x0F[0]
# Browser:  0x10[0]
# CMS:      0x11[0]
# Files:    0x13[0]
# Media:    0x16[0]
# PDF:      0x17[0]
# Custom:   0x18[0]
