from getmac import get_mac_address as gma

from pyama import client
from pyama.commands import Commands

HOST = 'iiyama.home'

print("MAC: %a" % gma(ip=HOST, hostname=HOST))


c = Commands( client.Client(HOST))
c.set_power_state(True)


# c.send(b'\x01', b'\x18', b'\x01')

# send(b'\x01', b'\xA2', b'\x01')
# send(b'\x01', b'\xAC', b'\x00\x18\x01\x00')

# send(b'\x01', b'\x44', b'\100\20')
