#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as ET

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
        self.enableWidget = QWidget()
        self.config_path = config_path
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

        """slot"""
        self.savePushButton.clicked.connect(self.saveAction)

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

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            auto_start = root.find('app').find('auto_start').text
            application_title = root.find('app').find('application_title').text

            enable = bool(int(auto_start))
            self.autoStartSwitchButton.setChecked(enable)

            self.applicationTitleLineEdit.setText(application_title)
        except Exception as e:
            """Here will emit a signal."""
            print(e)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: ignore this
        :return: None
        """
        self.load_config()

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            auto_start = self.autoStartSwitchButton.checked
            root.find('app').find('auto_start').text = "1" if auto_start else "0"
            root.find('app').find('application_title').text = self.applicationTitleLineEdit.text()
            tree.write(self.config_path)
        except Exception as e:
            """Here will emit a signal."""
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ApplicationSettingWidget("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
