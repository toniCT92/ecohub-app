from abc import ABC, abstractmethod
import time
import random


class SmartDevice(ABC):
    def __init__(self, device_id: str, name: str, location: str):
        self._device_id = device_id
        self._name = name
        self._location = location
        self._device_type = "GENERIC"
        self._is_connected = False

    @property
    def device_id(self):
        return self._device_id

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def device_type(self):
        return self._device_type

    @property
    def is_connected(self):
        return self._is_connected

    def connect(self):
        print(f"{self._name} is connecting...")
        time.sleep(random.uniform(0.5, 1.5))
        self._is_connected = True
        print(f"{self._name} connected successfully.")

    def send_update(self) -> dict:
        if not self._is_connected:
            raise RuntimeError("Device must be connected before sending updates")

        return {
            "device_id": self._device_id,
            "type": self._device_type,
            "timestamp": time.time(),
            "payload": {}
        }

    @abstractmethod
    def execute_command(self, command: dict):
        pass
