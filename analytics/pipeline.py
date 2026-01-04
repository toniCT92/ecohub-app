from dataclasses import dataclass
from typing import Any, Dict
from functools import reduce
from typing import Iterable, Optional

@dataclass
class DeviceEvent:
    device_id: str
    device_type: str
    timestamp: float
    payload: Dict[str, Any]

def map_to_event(raw_update: dict) -> DeviceEvent:
    
    return DeviceEvent(
        device_id=raw_update["device_id"],
        device_type=raw_update["type"],
        timestamp=raw_update["timestamp"],
        payload=raw_update["payload"]
    )
def is_high_temperature(event: DeviceEvent, threshold: float = 30.0) -> bool:
    
    if event.device_type != "THERMOSTAT":
        return False

    current_temp = event.payload.get("current_temp")
    return current_temp is not None and current_temp > threshold


def is_low_battery(event: DeviceEvent, threshold: float = 10.0) -> bool:
    
    if event.device_type != "CAMERA":
        return False

    battery = event.payload.get("battery_level")
    return battery is not None and battery < threshold

def average_temperature(events: Iterable[DeviceEvent]) -> Optional[float]:
   
    temps = list(
        map(
            lambda e: e.payload.get("current_temp"),
            filter(lambda e: e.device_type == "THERMOSTAT", events)
        )
    )

    if not temps:
        return None

    total = reduce(lambda a, b: a + b, temps)
    return total / len(temps)


def handle_automation(event: DeviceEvent, devices: dict):
    
    if is_high_temperature(event):
        print("⚠️ ALERT: High Temp detected! Triggering cooling...")

        thermostat = devices.get(event.device_id)
        if thermostat:
            thermostat.execute_command({
                "action": "SET_TARGET_TEMP",
                "value": 22.0
            })

    if is_low_battery(event):
        print(f"⚠️ ALERT: Low battery detected on {event.device_id}")