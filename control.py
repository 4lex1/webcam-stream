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
    def __init__(self, ip, port, on_resize=None, on_framerate=None):
        self.thread = threading.Thread(target=self._start_thread)
        self.running = False
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(3)
        self.on_resize = on_resize
        self.on_framerate = on_framerate

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def _start_thread(self):
        while self.running:
            try:
                self.sock.sendto(b"ready_for_command", (self.ip, self.port))
                response, _ = self.sock.recvfrom(1024)
                decoded_response = response.decode()

                if self.on_resize and decoded_response.startswith("resize"):
                    _, width, height = decoded_response.split("_")
                    width = int(width)
                    height = int(height)
                    self.on_resize(width, height)
                elif self.on_framerate and decoded_response.startswith("framerate"):
                    _, framerate = decoded_response.split("_")
                    framerate = int(framerate)
                    self.on_framerate(framerate)
            except Exception as e:
                print(e)
                pass

            time.sleep(1)
