from devices.base import SmartDevice


class SmartBulb(SmartDevice):
    def __init__(self, device_id: str, name: str, location: str):
        super().__init__(device_id, name, location)
        self._device_type = "BULB"
        self._is_on = False
        self._brightness = 100 

    @property
    def is_on(self):
        return self._is_on

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError("Brightness must be between 0 and 100")
        self._brightness = value

    def send_update(self) -> dict:
        update = super().send_update()
        update["payload"] = {
            "is_on": self._is_on,
            "brightness": self._brightness
        }
        return update

    def execute_command(self, command: dict):
        """
        Supported commands:
        - {"action": "ON"}
        - {"action": "OFF"}
        - {"action": "SET_BRIGHTNESS", "value": int}
        """
        action = command.get("action")

        if action == "ON":
            self._is_on = True
            print(f"{self.name}: turned ON")

        elif action == "OFF":
            self._is_on = False
            print(f"{self.name}: turned OFF")

        elif action == "SET_BRIGHTNESS":
            self.brightness = command.get("value", self._brightness)
            print(f"{self.name}: brightness set to {self._brightness}")

        else:
            print(f"{self.name}: unknown command")
