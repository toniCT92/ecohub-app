import asyncio
import random


async def device_loop(device):
    
    while True:
        await asyncio.sleep(random.uniform(1, 5))
        update = device.send_update()
        print(update)
