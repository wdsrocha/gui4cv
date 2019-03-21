from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, \
    QApplication, QSlider, QLabel
from pyqtgraph import ImageView
from packages.utils import CVQImage
from PyQt5.QtGui import QImage, QPixmap


class StartWindow(QMainWindow):
    def __init__(self, camera=None):
        super().__init__()
        self.camera = camera

        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.screenLabel = QLabel()

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.screenLabel)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.setCentralWidget(self.central_widget)

        self.button_frame.clicked.connect(self.update_image)
        self.button_movie.clicked.connect(self.start_movie)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_movie)

    def update_image(self):
        frame = self.camera.get_frame()
        image = CVQImage(frame)
        pixmap = QPixmap.fromImage(image)
        self.screenLabel.setPixmap(pixmap)

    def update_movie(self):
        image = CVQImage(self.camera.last_frame)
        pixmap = QPixmap.fromImage(image)
        self.screenLabel.setPixmap(pixmap)

    def start_movie(self):
        self.movie_thread = MovieThread(self.camera)
        self.movie_thread.start()
        self.update_timer.start(30)


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)


if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())
