import pygatt
from binascii import hexlify
import time
adapter = pygatt.GATTToolBackend()

def handle_data(handle,value):
    print("data:%s",hexlify(value))

try:
    adapter.start()
    device = adapter.connect('54:b7:e5:79:f4:49')
    device.subscribe("0000fff1-0000-1000-8000-00805f9b34fb",callback=handle_data)
    #value = device.char_read("a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b")
    while True:
        time.sleep(10)
finally:
    adapter.stop()
