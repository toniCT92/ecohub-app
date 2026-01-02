import asyncio
from network.simulator import device_loop


async def run_controller(devices):
    print("Connecting devices...")

    for device in devices:
        device.connect()

    print("All devices connected!")

    devices_map = {device.device_id: device for device in devices}

    tasks = []
    for device in devices:
        tasks.append(
            asyncio.create_task(device_loop(device, devices_map))
        )

    await asyncio.gather(*tasks)
