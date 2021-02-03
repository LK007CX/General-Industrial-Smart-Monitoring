#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, \
    QHBoxLayout, QVBoxLayout, QSplitter, QApplication

from ui.SwitchButton import SwitchButton


class ApplicationSettingWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(ApplicationSettingWidget, self).__init__(*args, **kwargs)

        self.applicationTitleLabel = QLabel("专案名称")
        self.applicationTitleLineEdit = QLineEdit()
        self.autoStartLabel = QLabel("开机启动")
        self.autoStartSwitchButton = SwitchButton()
        self.savePushButton = QPushButton("保存")

        self.config_path = config_path

        self.enableWidget = QWidget()

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        enableLayout = QHBoxLayout(spacing=0)
        enableLayout.setContentsMargins(0, 0, 0, 0)
        enableLayout.addWidget(QLabel())
        enableLayout.addWidget(self.autoStartSwitchButton)
        self.enableWidget.setLayout(enableLayout)

        """size"""
        self.applicationTitleLabel.setFixedWidth(200)
        self.applicationTitleLineEdit.setFixedWidth(200)
        self.autoStartSwitchButton.setFixedSize(QSize(40, 24))
        self.enableWidget.setFixedWidth(200)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.autoStartLabel)
        leftLayout.addWidget(self.applicationTitleLabel)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.enableWidget)
        rightLayout.addWidget(self.applicationTitleLineEdit)

        """topLayout"""
        topLayout = QHBoxLayout()
        topLayout.addLayout(leftLayout)
        topLayout.addLayout(rightLayout)

        # topLayout.addWidget(self.applicationTitleLabel)
        # topLayout.addWidget(self.applicationTitleLineEdit)

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ApplicationSettingWidget("../appsettings.xml")
    win.show()
    sys.exit(app.exec_())
