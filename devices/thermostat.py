from devices.base import SmartDevice
import random


class SmartThermostat(SmartDevice):
    def __init__(self, device_id: str, name: str, location: str):
        super().__init__(device_id, name, location)
        self._device_type = "THERMOSTAT"

        self._current_temp = random.uniform(22.0, 24.0)
        self._target_temp = 24.0
        self._humidity = random.uniform(40.0, 60.0)

        self._mode = "NORMAL"   
        self._stabilize_ticks = 0



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

        if self._mode == "NORMAL":
            self._current_temp += random.uniform(0.8, 1.3)

            if self._current_temp >= 30.0:
                self._mode = "OVERHEAT"

        elif self._mode == "OVERHEAT":
            self._mode = "COOLING"

        elif self._mode == "COOLING":
            self._current_temp -= random.uniform(2.5, 4.0)

            if self._current_temp <= self._target_temp + 0.3:
                self._mode = "STABILIZE"
                self._stabilize_ticks = random.randint(3, 5)

        elif self._mode == "STABILIZE":
            self._current_temp += random.uniform(-0.15, 0.15)
            self._stabilize_ticks -= 1

            if self._stabilize_ticks <= 0:
                self._mode = "NORMAL"

        self._current_temp = max(10.0, min(self._current_temp, 45.0))

        self._humidity += random.uniform(-1.5, 1.5)
        self._humidity = max(20.0, min(self._humidity, 70.0))

        update = super().send_update()
        update["payload"] = {
            "current_temp": round(self._current_temp, 2),
            "target_temp": self._target_temp,
            "humidity": round(self._humidity, 2)
        }
        return update



    def execute_command(self, command: dict):
        if command.get("action") == "SET_TARGET_TEMP":
            self.target_temp = command.get("value", self._target_temp)
            print(f"{self.name}: target temperature set to {self._target_temp:.1f}°C")
        else:
            print(f"{self.name}: unknown command")
