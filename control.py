import threading
import time
import socket
import time
import queue

class ControllerServer:
    def __init__(self, port):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port))
        self.sock.settimeout(5)
        self.q = queue.Queue()

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            try:
                message, client_address = self.sock.recvfrom(1024)
                decoded_message = message.decode()
                if (decoded_message == "ready_for_command"):
                    if self.q.empty():
                        self.sock.sendto(b"none", client_address)
                    else:
                        self.sock.sendto(self.q.get().encode(), client_address)
                    
                else:
                    print(f"Unknown command: {decoded_message}")
            except:
                pass

    def queue_command(self, command):
        self.q.put(command)

class ControllerClient:
    def __init__(self, ip, port, on_resize=None):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(3)
        self.on_resize = on_resize

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            try:
                self.sock.sendto(b"ready_for_command", (self.ip, self.port))
                response, addr = self.sock.recvfrom(1024)
                decoded_response = response.decode()
                if decoded_response == "resize_640_480":
                    self.on_resize(640, 480)
                elif decoded_response == "resize_800_600":
                    self.on_resize(800, 600)
                elif decoded_response == "resize_1024_768":
                    self.on_resize(1024, 768)
            except Exception as e:
                print(e)
                pass

            time.sleep(1)
