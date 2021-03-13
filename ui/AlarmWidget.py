#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget

from ui.AlarmTableWidget import AlarmTableWidget


class AlarmWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(AlarmWidget, self).__init__(*args, **kwargs)
        self.alarmTableWidget = AlarmTableWidget(config_path, objectName='errorTableWidget')
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(1, 0, 0, 0)
        layout.addWidget(self.alarmTableWidget)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = AlarmWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
