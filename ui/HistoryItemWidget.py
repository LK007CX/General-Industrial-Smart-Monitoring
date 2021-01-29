#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

import cv2
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QImage, QPixmap, QMouseEvent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QLabel, QVBoxLayout, \
    QHBoxLayout, QApplication


class HistoryItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, image, log, time, item, *args, **kwargs):
        super(HistoryItemWidget, self).__init__(*args, **kwargs)

        self.image = image
        self.label = log
        self.time = time
        self._item = item

        self.classLabel = QLabel(self.label, objectName="classLabel")
        self.timeLabel = QLabel(self.time, objectName="timeLabel")
        self.imageLabel = QLabel(objectName="imageLabel")

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setFixedSize(QSize(200, 120))
        self.imageLabel.setMouseTracking(True)

        height, width, channel = self.image.shape
        bytePerLine = 3 * width
        qImg = QImage(self.image.data, width, height, bytePerLine,
                      QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(qImg))

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.classLabel, 0, Qt.AlignBottom | Qt.AlignCenter)
        leftLayout.addWidget(self.timeLabel, 0, Qt.AlignTop | Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addWidget(self.imageLabel)

        self.setLayout(layout)
        self.setObjectName("historyItemWidget")
        self.setContentsMargins(0, 0, 0, 0)

    def doDeleteItem(self):
        """
        Delete item.
        :return: None
        """
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        """
        Determine the height of the item.
        :return: None
        """
        return QSize(200, 150)

    def mousePressEvent(self, a0: QMouseEvent):
        pass


if __name__ == '__main__':
    item_ = QListWidgetItem()
    app = QApplication(sys.argv)
    image = cv2.imread('../icon/back.png')
    win = HistoryItemWidget(image, 'ok', '2020', item_)
    win.show()
    sys.exit(app.exec_())
