import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from packages.utils import CVQImage


class Camera(QtCore.QThread):
    updateFrame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, device: int, parent=None):
        super().__init__(parent)
        self.device = device
        self.videoCapture = None

    def release(self):
        self.videoCapture.release()

    def run(self):
        self.videoCapture = cv2.VideoCapture(self.device)
        while self.videoCapture.isOpened():
            ret, frame = self.videoCapture.read()
            if ret:
                self.updateFrame.emit(frame)

    def __str__(self):
        return f"OpenCV Device {self.device}."


class CameraLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lastFrame = None
        self.isPaused = False

    def play(self):
        self.isPaused = False

    def pause(self):
        self.isPaused = True

    @QtCore.pyqtSlot(np.ndarray)
    def render(self, frame: np.ndarray):
        if self.isPaused:
            return
        self.lastFrame = frame
        self.setPixmap(QtGui.QPixmap.fromImage(CVQImage(self.lastFrame)))


def main():
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()

    cameraLabel = CameraLabel()
    camera = Camera(0)
    camera.updateFrame.connect(cameraLabel.render)
    camera.start()

    playPauseButton = QtWidgets.QPushButton("Pause")

    def playPause():
        if playPauseButton.text() == "Pause":
            cameraLabel.pause()
            playPauseButton.setText("Play")
        else:
            cameraLabel.play()
            playPauseButton.setText("Pause")

    playPauseButton.clicked.connect(playPause)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(cameraLabel)
    layout.addWidget(playPauseButton)

    centralWidget = QtWidgets.QWidget()
    centralWidget.setLayout(layout)

    window.setCentralWidget(centralWidget)

    window.setLayout(layout)
    window.show()

    app.exit(app.exec_())


if __name__ == "__main__":
    main()
