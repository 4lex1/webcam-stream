import time
import signal
import sys
from camera_stream import CameraStreamServer
from control import ControllerServer

camera_stream = CameraStreamServer(1935)
control_server = ControllerServer(1936)

def handle_signal(sig, frame):
    camera_stream.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

camera_stream.start()
control_server.start()

while True:
    time.sleep(10)
    pass
