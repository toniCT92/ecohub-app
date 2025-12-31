from devices.base import SmartDevice
import random
import time


class SmartCamera(SmartDevice):
    def __init__(self, device_id: str, name: str, location: str):
        super().__init__(device_id, name, location)
        self._device_type = "CAMERA"
        self._motion_detected = False
        self._battery_level = random.uniform(30.0, 100.0)
        self._last_snapshot = None

    @property
    def motion_detected(self):
        return self._motion_detected

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def last_snapshot(self):
        return self._last_snapshot

    def send_update(self) -> dict:

        self._motion_detected = random.choice([True, False])

        if self._motion_detected:
            self._last_snapshot = time.time()
            self._battery_level -= random.uniform(0.5, 2.0)
        else:
            self._battery_level -= random.uniform(0.1, 0.3)

        # Protect battery bounds
        self._battery_level = max(0.0, min(100.0, self._battery_level))

        update = super().send_update()
        update["payload"] = {
            "motion_detected": self._motion_detected,
            "last_snapshot": self._last_snapshot,
            "battery_level": self._battery_level
        }
        return update

    def execute_command(self, command: dict):
        """
        Supported commands:
        - {"action": "TAKE_SNAPSHOT"}
        """
        action = command.get("action")

        if action == "TAKE_SNAPSHOT":
            self._last_snapshot = time.time()
            self._battery_level = max(0.0, self._battery_level - 1.0)
            print(f"{self.name}: snapshot taken")
        else:
            print(f"{self.name}: unknown command")
