#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

from ui.ErrorTableWidget import ErrorTableWidget


class ErrorWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ErrorWidget, self).__init__(*args, **kwargs)
        self.errorTableWidget = ErrorTableWidget(objectName='errorTableWidget')
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return:
        """
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 1, 0)
        layout.addWidget(self.errorTableWidget)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ErrorWidget()
    win.show()
    sys.exit(app.exec_())
