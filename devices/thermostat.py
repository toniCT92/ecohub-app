from devices.base import SmartDevice
import random


class SmartThermostat(SmartDevice):
    def __init__(self, device_id: str, name: str, location: str):
        super().__init__(device_id, name, location)
        self._device_type = "THERMOSTAT"
        self._current_temp = random.uniform(18.0, 25.0)
        self._target_temp = 24.0
        self._humidity = random.uniform(30.0, 60.0)
    @property
    def current_temp(self):
        return self._current_temp

    @property
    def target_temp(self):
        return self._target_temp

    @target_temp.setter
    def target_temp(self, value: float):
        if not 10.0 <= value <= 30.0:
            raise ValueError("Target temperature must be between 10 and 30")
        self._target_temp = value

    @property
    def humidity(self):
        return self._humidity

    def send_update(self) -> dict:
        self._current_temp += random.uniform(1.0, 1.5)
        # (-0.5, 0.5)
        self._humidity += random.uniform(-2.0, 2.0)

        update = super().send_update()
        update["payload"] = {
            "current_temp": self._current_temp,
            "target_temp": self._target_temp,
            "humidity": self._humidity
        }
        return update

    def execute_command(self, command: dict):
        """
        Supported commands:
        - {"action": "SET_TARGET_TEMP", "value": float}
        """
        action = command.get("action")

        if action == "SET_TARGET_TEMP":
            self.target_temp = command.get("value", self._target_temp)
            print(f"{self.name}: target temperature set to {self._target_temp:.1f}°C")
        else:
            print(f"{self.name}: unknown command")
