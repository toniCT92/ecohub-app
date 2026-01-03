import asyncio
import threading
import queue

from network.simulator import device_loop
from storage.logger import storage_worker


async def run_controller(devices):
    print("Connecting devices...")

    for device in devices:
        device.connect()

    print("All devices connected!")

    data_queue = queue.Queue()
    stop_event = threading.Event()

    storage_thread = threading.Thread(
        target=storage_worker,
        args=(data_queue, stop_event),
        daemon=True
    )
    storage_thread.start()

    devices_map = {device.device_id: device for device in devices}

    tasks = []
    for device in devices:
        tasks.append(
            asyncio.create_task(
                device_loop(device, devices_map, data_queue)
            )
        )

    try:
        await asyncio.gather(*tasks)
    finally:
        stop_event.set()
