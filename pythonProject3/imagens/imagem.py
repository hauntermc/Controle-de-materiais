from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.init_ui(image_path)

    def init_ui(self, image_path):
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        pixmap = QPixmap(image_path)

        # Redimensiona o pixmap para o tamanho desejado
        desired_width = 400
        desired_height = 300
        scaled_pixmap = pixmap.scaled(desired_width, desired_height, Qt.KeepAspectRatio)

        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.image_label)
        self.setLayout(layout)
