from pyama import client

HOST = 'iiyama.home'

c = client.Client(HOST)

c.send(b'\x01', b'\x18', b'\x01')

# send(b'\x01', b'\xA2', b'\x01')
# send(b'\x01', b'\xAC', b'\x00\x18\x01\x00')

# send(b'\x01', b'\x44', b'\100\20')
