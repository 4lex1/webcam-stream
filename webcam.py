import time
import signal
import sys
from camera_stream import CameraStreamClient
from control import ControllerClient

def on_resize_handler(width, height):
    camera_stream.width = width
    camera_stream.height = height

def on_framerate_handler(framerate):
    camera_stream.framerate = framerate

def on_quality_handler(quality):
    camera_stream.quality = quality

camera_stream = CameraStreamClient("pipoulets.internet-box.ch", 1935)
control_client = ControllerClient("pipoulets.internet-box.ch", 1936, on_resize=on_resize_handler, on_framerate=on_framerate_handler)

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
