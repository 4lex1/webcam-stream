import time
import signal
import sys
from camera_stream import CameraStreamClient
from control import ControllerClient

camera_stream = CameraStreamClient("pipoulets.internet-box.ch", 1935)
control_client = ControllerClient("pipoulets.internet-box.ch", 1936)

def handle_signal(sig, frame):
    camera_stream.stop()
    control_client.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

camera_stream.start()
control_client.start()

while True:
    time.sleep(10)
    pass
