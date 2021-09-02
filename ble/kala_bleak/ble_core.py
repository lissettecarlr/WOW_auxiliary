
import sys
import time
import platform
import asyncio
from loguru import logger

from bleak import BleakClient

bleAddr = "54:B7:E5:79:F4:49"

#特征
NOTIFICATION_UUID = "0000FFF1-0000-1000-8000-00805f9b34fb"
CMD_UUID = "0000F102-0000-1000-8000-00805f9b34fb"
 
async def callback_handler(sender, data):
    await queue.put((time.time(), data))

def cmd_callback_handler(sender,data):
    print(data)

async def run_ble_client(address):

    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")
        await client.start_notify(NOTIFICATION_UUID, callback_handler)
        await client.start_notify(CMD_UUID,callback_handler)

        await asyncio.sleep(30.0)
        await client.stop_notify(CMD_UUID)
        await client.stop_notify(NOTIFICATION_UUID)
        # Send an "exit command to the consumer" 
        #await queue.put((time.time(), None))


async def run_queue_consumer(queue: asyncio.Queue):
    while True:
        # Use await asyncio.wait_for(queue.get(), timeout=1.0) if you want a timeout for getting data.
        epoch, data = await queue.get()
        #另一个进程在等待之后会往队列中存入一个空
        if data is None:
            logger.info(
                "Got message from client about disconnection. Exiting consumer loop..."
            )
            break
        else:
            logger.info(f"Received callback data via async queue at {epoch}: {data}")


async def main(address: str):
    global queue
    queue = asyncio.Queue()
    client_task = run_ble_client(address)
    consumer_task = run_queue_consumer(queue)
    await asyncio.gather(client_task, consumer_task)
    logger.info("Main method done.")

if __name__ == "__main__":
    asyncio.run(main(bleAddr))
