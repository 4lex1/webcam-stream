import threading
import time
import cv2
import socket
import numpy as np
import time

class CameraStreamServer:
    def __init__(self, port, width = 640, height = 480, on_image=None):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.width = width
        self.height = height
        self.on_image = on_image

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            encoded_image_bytes, _ = self.sock.recvfrom(65535) 

            image_decoded = cv2.imdecode(np.frombuffer(encoded_image_bytes, np.uint8), cv2.IMREAD_COLOR)
            image_decoded = cv2.resize(image_decoded, (self.width, self.height))
            
            if self.on_image and image_decoded is not None:
                self.on_image(image_decoded)


class CameraStreamClient:
    def __init__(self, ip, port, width = 640, height = 480, quality = 50, framerate = 15):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cap = cv2.VideoCapture(0)
        self.quality = quality
        self.width = width
        self.height = height
        self.framerate = framerate

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            try:
                _, frame = self.cap.read()
                image = cv2.resize(frame, (self.width, self.height))
                cv2.putText(image, f"{self.width}*{self.height} | quality {self.quality}% | {self.framerate} FPS", (30, 30), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 0), 1, cv2.LINE_AA)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
                _, image = cv2.imencode('.jpg', image, encode_param)
                encoded_image_bytes = image.tobytes()
                self.sock.sendto(encoded_image_bytes, (self.ip, self.port))
            except Exception as e:
                print(e)
                pass

            time.sleep(1 / self.framerate)
