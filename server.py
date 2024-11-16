import sys
import cv2
from camera_stream import CameraStreamServer
from control import ControllerServer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage


class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Affichage de l'image")
        self.setGeometry(800, 100, 640, 480)

        self.image_label = QLabel(self)
        self.image_label.setText("Aucune image chargée")
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def display_image(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        bytes_per_line = c * w
        qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qimage))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.camera_stream = CameraStreamServer(1935, on_image=self.display_image)
        self.control_server = ControllerServer(1936)

        self.image_window = ImageWindow()
        self.image_window.show()

        self.setWindowTitle('Pipoubike')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Changer la résolution :"))
        resolution_layout = QHBoxLayout()

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Largeur (ex: 640)")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Hauteur (ex: 480)")

        update_resolution_button = QPushButton("Mettre à jour la résolution")
        update_resolution_button.clicked.connect(self.update_resolution)

        resolution_layout.addWidget(self.width_input)
        resolution_layout.addWidget(self.height_input)
        resolution_layout.addWidget(update_resolution_button)
        layout.addLayout(resolution_layout)

        layout.addWidget(QLabel("Changer le framerate :"))
        framerate_layout = QHBoxLayout()

        self.framerate_input = QLineEdit()
        self.framerate_input.setPlaceholderText("Framerate (ex: 30)")

        update_framerate_button = QPushButton("Mettre à jour le framerate")
        update_framerate_button.clicked.connect(self.update_framerate)

        framerate_layout.addWidget(self.framerate_input)
        framerate_layout.addWidget(update_framerate_button)
        layout.addLayout(framerate_layout)

        quality_layout = QHBoxLayout()
        self.quality_input = QLineEdit()
        self.quality_input.setPlaceholderText("Qualité (ex: 50)")
        quality_button = QPushButton("Mettre à jour la qualité")
        quality_button.clicked.connect(self.update_quality)

        quality_layout.addWidget(self.quality_input)
        quality_layout.addWidget(quality_button)
        layout.addLayout(quality_layout)

        self.setLayout(layout)

        self.camera_stream.start()
        self.control_server.start()

    def update_resolution(self):
        try:
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            self.camera_stream.width = width
            self.camera_stream.height = height
            self.control_server.queue_command(f"resize_{width}_{height}")
        except ValueError:
            print("Veuillez entrer des valeurs valides pour la largeur et la hauteur.")

    def update_framerate(self):
        try:
            framerate = int(self.framerate_input.text())
            self.control_server.queue_command(f"framerate_{framerate}")
        except ValueError:
            print("Veuillez entrer une valeur valide pour le framerate.")

    def update_quality(self):
        try:
            quality = int(self.quality_input.text())
            self.control_server.queue_command(f"quality_{quality}")
        except ValueError:
            print("Veuillez entrer une valeur valide pour la qualité.")

    def display_image(self, cv_img):
        self.image_window.display_image(cv_img)

    def closeEvent(self, event):
        self.camera_stream.stop()
        self.control_server.stop()
        self.image_window.close()
        event.accept()


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())
