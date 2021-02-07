#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QPushButton, \
    QVBoxLayout, QHBoxLayout, QSplitter, QApplication

from ui.SwitchButton import SwitchButton


class ImageSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(ImageSettingsWidget, self).__init__(*args, **kwargs)
        self.config_path = config_path

        self.enableLabel = QLabel("启用NG图片保存")
        self.enableSwitchButton = SwitchButton()
        self.saveImageLabel = QLabel("NG图片本地存储")
        self.minimumStorageIntervalLabel = QLabel("最小存储间隔(秒)")
        self.maximumStorageQuantityLabel = QLabel("最大存储数量(张)")
        self.minimumStorageIntervalSpinBox = QSpinBox()
        self.maximumStorageQuantitySpinBox = QSpinBox()
        self.savePushButton = QPushButton("保存")

        self.splitterLabel1 = QLabel(objectName='splitterLabel1')
        self.splitterLabel2 = QLabel(objectName='splitterLabel2')

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """fixed size"""
        self.enableSwitchButton.setFixedSize(QSize(40, 24))
        self.enableLabel.setFixedWidth(200)
        self.minimumStorageIntervalLabel.setFixedWidth(200)
        self.minimumStorageIntervalSpinBox.setFixedWidth(200)
        self.maximumStorageQuantityLabel.setFixedWidth(200)
        self.maximumStorageQuantitySpinBox.setFixedWidth(200)
        self.splitterLabel1.setMaximumHeight(1)
        self.splitterLabel1.setMaximumWidth(self.width())
        self.splitterLabel2.setMaximumHeight(1)
        self.splitterLabel2.setMaximumWidth(self.width())
        """data limit"""
        self.minimumStorageIntervalSpinBox.setMinimum(1)
        self.minimumStorageIntervalSpinBox.setMaximum(10)
        self.minimumStorageIntervalSpinBox.setSingleStep(1)
        self.maximumStorageQuantitySpinBox.setMinimum(100)
        self.maximumStorageQuantitySpinBox.setMaximum(2500)
        self.maximumStorageQuantitySpinBox.setSingleStep(100)

        """slots"""
        self.savePushButton.clicked.connect(self.saveAction)

        """leftLayout"""
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.enableLabel)
        # leftLayout.addWidget(QLabel())
        leftLayout.addWidget(self.minimumStorageIntervalLabel)
        leftLayout.addWidget(self.maximumStorageQuantityLabel)

        """rightLayout"""
        rightLayout = QVBoxLayout()
        # rightLayout.addWidget(QLabel())
        rightLayout.addWidget(self.enableSwitchButton, 0, Qt.AlignRight)
        rightLayout.addWidget(self.minimumStorageIntervalSpinBox)
        rightLayout.addWidget(self.maximumStorageQuantitySpinBox)

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
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        enable = bool(int(root.find('image').find('enable').text))
        self.enableSwitchButton.setChecked(enable)

        minimumstorageinterval = root.find('image').find('minimumstorageinterval').text
        self.minimumStorageIntervalSpinBox.setValue(int(minimumstorageinterval))

        maximumstoragequantity = root.find('image').find('maximumstoragequantity').text
        self.maximumStorageQuantitySpinBox.setValue(int(maximumstoragequantity))

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        minimumstorageinterval = self.minimumStorageIntervalSpinBox.value()
        root.find('image').find('minimumstorageinterval').text = str(minimumstorageinterval)

        maximumstoragequantity = self.maximumStorageQuantitySpinBox.value()
        root.find('image').find('maximumstoragequantity').text = str(maximumstoragequantity)

        enable = self.enableSwitchButton.checked
        root.find('image').find('enable').text = "1" if enable else "0"

        tree.write(self.config_path)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: event
        :return: None
        """
        self.load_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ImageSettingsWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
