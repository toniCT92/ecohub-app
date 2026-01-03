import asyncio
import random

from analytics.pipeline import (
    map_to_event,
    handle_automation,
    average_temperature
)


EVENT_BUFFER = []


async def device_loop(device, devices_map, data_queue):
    """
    Async loop for a single device with analytics + storage integration.
    """
    while True:
        await asyncio.sleep(random.uniform(1, 5))

        raw_update = device.send_update()

        event = map_to_event(raw_update)
        EVENT_BUFFER.append(event)

        if len(EVENT_BUFFER) > 20:
            EVENT_BUFFER.pop(0)

        handle_automation(event, devices_map)

        avg_temp = average_temperature(EVENT_BUFFER)
        if avg_temp is not None:
            print(f"📊 Average house temperature: {avg_temp:.2f}°C")

        data_queue.put(raw_update)

        print(raw_update)
