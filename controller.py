import asyncio
from network.simulator import device_loop


async def run_controller(devices):
    
    print("Connecting devices...")

    for device in devices:
        device.connect()

    print("All devices connected!")

    tasks = []
    for device in devices:
        task = asyncio.create_task(device_loop(device))
        tasks.append(task)

    await asyncio.gather(*tasks)
