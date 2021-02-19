#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QApplication


class VideoWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(VideoWidget, self).__init__(*args, **kwargs)
        self.videoLabel = QLabel(objectName='videoLabel')
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.videoLabel.setScaledContents(True)
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoLabel)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)

    def handleDisplay(self, image):
        """
        Slot function that handle display.
        :param image: image
        :return: None
        """
        height, width, channel = image.shape
        bytePerLine = 3 * width
        self.qImg = QImage(image.data, width, height, bytePerLine,
                           QImage.Format_RGB888).rgbSwapped()
        self.videoLabel.setPixmap(QPixmap.fromImage(self.qImg))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = VideoWidget()
    win.resize(QSize(800, 480))
    win.show()
    sys.exit(app.exec_())
