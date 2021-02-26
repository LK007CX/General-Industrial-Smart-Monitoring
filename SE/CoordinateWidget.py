#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class CoordinateWidget(QWidget):

    def __init__(self, minx="min_x", miny="min_y", maxx="max_x", maxy="max_y", *args, **kwargs):
        super(CoordinateWidget, self).__init__(*args, **kwargs)
        self.minXLabel = QLabel(minx)
        self.minYLabel = QLabel(miny)
        self.maxXLabel = QLabel(maxx)
        self.maxYLabel = QLabel(maxy)
        self.init_ui()

    def init_ui(self):
        width = 30
        self.minXLabel.setFixedWidth(width)
        self.minYLabel.setFixedWidth(width)
        self.maxXLabel.setFixedWidth(width)
        self.maxYLabel.setFixedWidth(width)

        self.minXLabel.setAlignment(Qt.AlignCenter)
        self.minYLabel.setAlignment(Qt.AlignCenter)
        self.maxXLabel.setAlignment(Qt.AlignCenter)
        self.maxYLabel.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout(spacing=0)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.minXLabel)
        layout.addWidget(self.minYLabel)
        layout.addWidget(self.maxXLabel)
        layout.addWidget(self.maxYLabel)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CoordinateWidget()
    win.show()
    sys.exit(app.exec_())
