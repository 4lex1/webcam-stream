import cv2
import socket
import numpy as np

UDP_IP = "0.0.0.0" 
UDP_PORT = 1935

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"listening on {UDP_PORT}...")

while True:
    encoded_image_bytes, addr = sock.recvfrom(65535) 

    image_decoded = cv2.imdecode(np.frombuffer(encoded_image_bytes, np.uint8), cv2.IMREAD_COLOR)

    if image_decoded is not None:
        cv2.imshow('Received Webcam Stream', image_decoded)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
sock.close()
