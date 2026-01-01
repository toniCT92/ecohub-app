import asyncio

from devices.bulb import SmartBulb
from devices.thermostat import SmartThermostat
from devices.camera import SmartCamera
from controller import run_controller


def main():
    devices = [
        SmartBulb("bulb_01", "Mysterious Smart Bulb", "Living Room"),
        SmartThermostat("thermo_01", "Famous Smart Thermostat", "Bedroom"),
        SmartCamera("cam_01", "Gorgeous Smart Camera", "Entrance")
    ]

    asyncio.run(run_controller(devices))


if __name__ == "__main__":
    main()
