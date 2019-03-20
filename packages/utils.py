from PyQt5.QtGui import QImage

import numpy as np


class CVQImage(QImage):
    def __init__(self, cvImage: np.ndarray):
        self.cvImage = cvImage
        data = self.cvImage.data
        width = self.cvImage.shape[1]
        height = self.cvImage.shape[0]
        bytesPerLine = self.cvImage.strides[0]
        format_ = QImage.Format_RGB888
        super().__init__(
            QImage(data, width, height, bytesPerLine, format_).rgbSwapped())
