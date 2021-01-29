#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import QTimer, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QHBoxLayout, \
    QSplitter, QApplication

from ui.SystemSettingsTabWidget import SystemSettingsTabWidget


class HeaderWidget(QWidget):
    def __init__(self, config_path, title, *args, **kwargs):
        super(HeaderWidget, self).__init__(*args, **kwargs)

        self.logoLabel = QLabel(objectName="logoLabel")
        self.titleLabel = QLabel(title, objectName="titleLabel")
        self.cameraStatusLabel = QLabel(objectName="cameraStatusLabel")
        self.cameraLabel = QLabel("相机连接", objectName="cameraLabel")
        self.remoteServerStatusLabel = QLabel(objectName="remoteServerStatusLabel")
        self.remoteServerLabel = QLabel("远程Server", objectName="remoteServerLabel")
        self.settingsPushButton = QPushButton("设置", objectName="settingsPushButton")
        self.settingsPushButton2 = QPushButton("设置", objectName="settingsPushButton2")
        self.settingsPushButton3 = QPushButton(objectName="settingsPushButton3")
        self.systemSettingsTabWidget = SystemSettingsTabWidget(config_path)
        self.restartPushButton = QPushButton("重启程式", objectName="restartPushButton")

        self.timerRun = QTimer()
        self.timerError = QTimer()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """fixed size"""
        self.cameraStatusLabel.setFixedSize(QSize(30, 30))
        self.remoteServerStatusLabel.setFixedSize(QSize(30, 30))
        self.logoLabel.setMaximumSize(QSize(60, 60))

        """icon"""
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setPixmap(QPixmap('icon/logo.png'))
        self.settingsPushButton3.setIcon(QIcon(QPixmap('icon/settings.png')))

        """slots"""
        self.settingsPushButton2.clicked.connect(self.systemSettingsTabWidget.show)

        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.logoLabel)
        layout.addWidget(self.titleLabel)
        splitter = QSplitter(objectName="splitter")
        layout.addWidget(splitter)
        layout.addWidget(self.cameraStatusLabel)
        layout.addWidget(self.cameraLabel)
        layout.addWidget(self.remoteServerStatusLabel)
        layout.addWidget(self.remoteServerLabel)
        layout.addWidget(self.settingsPushButton2)
        layout.addWidget(self.restartPushButton)
        self.setLayout(layout)

        """self"""
        self.test_data()
        self.setAttribute(Qt.WA_StyledBackground)

    def test_data(self):
        """
        Test data.
        :return: None
        """
        self.timerRun.timeout.connect(lambda: self.changeState(1))
        self.timerRun.timeout.connect(lambda: self.timerError.singleShot(500, lambda: self.changeState(0)))
        self.timerRun.start(1000)

    def changeState(self, val):
        """
        Slot function that change the system state.
        :param val: val
        :return: None
        """
        if val == 0:
            self.cameraStatusLabel.setStyleSheet("""background-color: red;""")
            self.remoteServerStatusLabel.setStyleSheet("""background-color: red;""")
        elif val == 1:
            self.cameraStatusLabel.setStyleSheet("""background-color: green;""")
            self.remoteServerStatusLabel.setStyleSheet("""background-color: green;""")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = HeaderWidget("../appsettings.xml", "异常带片智能监控")
    win.show()
    sys.exit(app.exec_())
