import cv2
import socket
import numpy as np

UDP_IP = "pipoulets.internet-box.ch" 
UDP_PORT = 1935    

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur d'ouverture de la webcam")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Erreur lors de la capture de l'image")
        break
    
    _, encoded_image = cv2.imencode('.jpg', frame)
    encoded_image_bytes = encoded_image.tobytes()
    sock.sendto(encoded_image_bytes, (UDP_IP, UDP_PORT))
    cv2.imshow('Webcam Stream', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
