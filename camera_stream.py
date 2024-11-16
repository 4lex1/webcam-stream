import threading
import time
import cv2
import socket
import numpy as np
import time

class CameraStream:
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
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
                _, image = cv2.imencode('.jpg', image, encode_param)
                encoded_image_bytes = image.tobytes()
                self.sock.sendto(encoded_image_bytes, (self.ip, self.port))
            except:
                pass
            
            time.sleep(1 / self.framerate)  



        
    