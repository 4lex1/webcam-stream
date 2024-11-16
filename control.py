import threading
import time
import socket
import time

class ControllerServer:
    def __init__(self, port):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.sock.settimeout(3)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            print("hello")
            message, client_address = self.sock.recvfrom(1024)
            decoded_message = message.decode()
            if (decoded_message == "ready_for_command"):
                self.sock.sendto(b"hello", client_address)
            else:
                print(f"Unknown command: {decoded_message}")

class ControllerClient:
    def __init__(self, ip, port):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(3)

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            try:
                print(f"sendind ready to {self.ip}:{self.port}")
                self.sock.sendto(b"ready_for_command", (self.ip, self.port))
                response, addr = self.sock.recvfrom(1024)
                print(f"Réponse reçue de {addr}: {response.decode()}")
            except Exception as e:
                print(e)
                pass

            time.sleep(1)
