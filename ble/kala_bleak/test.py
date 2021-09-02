import sys
import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger


CHARACTERISTIC_UUID_1 = "0000FFF1-0000-1000-8000-00805f9b34fb"  # <--- Change to the characteristic you want to enable notifications from.
CHARACTERISTIC_UUID_2 = "0000F102-0000-1000-8000-00805f9b34fb"  # <--- Change to the characteristic you want to enable notifications from.
ADDRESS = (
    "54:B7:E5:79:F4:49"  # <--- Change to your device's address here if you are using Windows or Linux
    if platform.system() != "Darwin"
    else "B9EA5233-37EF-4DD6-87A8-2A875E821C46"  # <--- Change to your device's address here if you are using macOS
)


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(address, debug=False):
    if debug:
        import sys

        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        await client.start_notify(CHARACTERISTIC_UUID_1, notification_handler)
        await client.start_notify(CHARACTERISTIC_UUID_2, notification_handler)
        await asyncio.sleep(30.0)
        await client.stop_notify(CHARACTERISTIC_UUID_1)
        await client.stop_notify(CHARACTERISTIC_UUID_2)


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(run(ADDRESS, True))
   