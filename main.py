from devices.camera import SmartCamera

cam = SmartCamera("cam_01", "Gorgeous Smart Camera", "Entrance")
cam.connect()
print(cam.send_update())
cam.execute_command({"action": "TAKE_SNAPSHOT"})
print(cam.send_update())
