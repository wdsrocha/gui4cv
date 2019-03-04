from PyQt5.QtWidgets import QApplication
from packages.models import Camera
from packages.views import StartWindow


if __name__ == "__main__":
    camera = Camera(0)
    camera.initialize()
    app = QApplication([])
    window = StartWindow(camera)
    window.show()
    app.exit(app.exec_())
