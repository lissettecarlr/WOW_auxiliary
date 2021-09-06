"""
Connect by BLEDevice
"""

import asyncio
import platform
import sys

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError


ADDRESS = (
    "54:B7:E5:79:F4:49"
    if platform.system() != "Darwin"
    else "0000fff0-0000-1000-8000-00805f9b34fb"
)
if len(sys.argv) == 2:
    ADDRESS = sys.argv[1]


async def print_services(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        # 这里将打印该设备的所以服务
        for service in svcs:
            print(service)

loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(ADDRESS))
