import cv2
import socket
import numpy as np

UDP_IP = "pipoulets.internet-box.ch"
UDP_PORT = 1935

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

print("opening cap")
if not cap.isOpened():
    print("could not open cap")
    exit()


encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
while True:
    ret, frame = cap.read()
    image = cv2.resize(image (640, 480))
    _, image = cv2.imencode('.jpg', image, encode_param)

    encoded_image_bytes = image.tobytes()
    print(f"length: {len(encoded_image_bytes)}")
    # sock.sendto(encoded_image_bytes, (UDP_IP, UDP_PORT))
    cv2.imshow('Webcam Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
