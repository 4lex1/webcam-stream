import cv2
import socket
import numpy as np
import time
import signal
import sys
from camera_stream import CameraStream

camera_stream = CameraStream("pipoulets.internet-box.ch", 1935)

def handle_signal(sig, frame):
    camera_stream.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

camera_stream.start()

while True:
    time.sleep(10)
    pass
