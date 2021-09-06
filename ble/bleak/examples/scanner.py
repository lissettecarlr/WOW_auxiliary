"""
Bleak Scanner
-------------



Updated on 2020-08-12 by hbldh <henrik.blidh@nedomkull.com>

"""

import asyncio
import platform
import sys

from bleak import BleakScanner


address = (
    "54:B7:E5:79:F4:49"  # <--- Change to your device's address here if you are using Windows or Linux
    if platform.system() != "Darwin"
    else "0000fff0-0000-1000-8000-00805f9b34fb"  # <--- Change to your device's address here if you are using macOS
)
if len(sys.argv) == 2:
    address = sys.argv[1]

async def run():
    device = await BleakScanner.find_device_by_address(address)
    print(device)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
