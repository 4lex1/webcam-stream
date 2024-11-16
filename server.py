import time
import signal
import sys
import cv2
from camera_stream import CameraStreamServer
from control import ControllerServer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.camera_stream = CameraStreamServer(1935, on_image=self.display_image)
        self.control_server = ControllerServer(1936)

        # Initialisation de la fenêtre
        self.setWindowTitle('Changer la taille de la fenêtre')
        self.setGeometry(100, 100, 640, 480)

        # Layout vertical pour les boutons
        layout = QVBoxLayout()

        # Création des boutons
        button_640x480 = QPushButton("640x480")
        button_800x600 = QPushButton("800x600")
        button_1024x768 = QPushButton("1024x768")

        # Connecter les boutons aux actions
        button_640x480.clicked.connect(lambda: self.change_size(640, 480))
        button_800x600.clicked.connect(lambda: self.change_size(800, 600))
        button_1024x768.clicked.connect(lambda: self.change_size(1024, 768))

        # Ajouter les boutons au layout
        layout.addWidget(button_640x480)
        layout.addWidget(button_800x600)
        layout.addWidget(button_1024x768)

        self.image_label = QLabel(self)
        self.image_label.setText("Aucune image chargée")
        layout.addWidget(self.image_label)

        # Définir le layout de la fenêtre
        self.setLayout(layout)

        self.camera_stream.start()
        self.control_server.start()

    def change_size(self, width, height):
        self.resize(width, height)
        self.control_server.queue_command(f"resize_{width}_{height}")

    def display_image(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        bytes_per_line = c * w
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))

    def closeEvent(self, event):
        self.camera_stream.stop()
        self.control_server.stop()
        event.accept()

app = QApplication([])
window = MainWindow()
window.show()    
sys.exit(app.exec_())
