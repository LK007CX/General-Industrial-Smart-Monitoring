#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QComboBox, \
    QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, \
    QSplitter, QApplication


class CameraSettingsWidget(QWidget):

    def __init__(self, config_path):
        super(CameraSettingsWidget, self).__init__()

        self.modeLabel = QLabel("相机类型")
        self.USBRadioButton = QRadioButton("USB相机")
        self.RTSPRadioButton = QRadioButton("RTSP相机")
        self.cameraIndexLabel = QLabel("USB相机编号")
        self.cameraIndexComboBox = QComboBox()
        self.cameraIPLabel = QLabel("RTSP相机地址")
        self.cameraIPLineEdit = QLineEdit()
        self.cameraPortLabel = QLabel("RTSP相机端口")
        self.cameraPortLineEdit = QLineEdit()
        self.resolutionLabel = QLabel("相机解析度")
        self.resolutionComboBox = QComboBox()
        self.cameraTestPushButton = QPushButton("取像测试")
        self.savePushButton = QPushButton("保存")

        self.config_path = config_path
        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """initialize data"""
        index = [str(i) for i in range(5)]
        self.cameraIndexComboBox.addItems(index)
        resolution = ["800*480", "960*540", "1280*720", "1920*1080"]
        self.resolutionComboBox.addItems(resolution)

        """keep widgets fixed size"""
        self.modeLabel.setFixedWidth(200)
        self.USBRadioButton.setFixedWidth(200)
        self.RTSPRadioButton.setFixedWidth(200)
        self.cameraIndexLabel.setFixedWidth(200)
        self.cameraIPLabel.setFixedWidth(200)
        self.cameraPortLabel.setFixedWidth(200)
        self.resolutionLabel.setFixedWidth(200)
        self.cameraIndexComboBox.setFixedWidth(400)
        self.cameraIPLineEdit.setFixedWidth(400)
        self.cameraPortLineEdit.setFixedWidth(200)
        self.resolutionComboBox.setFixedWidth(400)

        """slots"""
        self.savePushButton.clicked.connect(self.saveAction)

        """leftLayout"""
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.modeLabel)
        leftLayout.addWidget(self.cameraIndexLabel)
        leftLayout.addWidget(self.cameraIPLabel)
        leftLayout.addWidget(self.resolutionLabel)

        """modeLayout"""
        modeLayout = QHBoxLayout()
        modeLayout.addWidget(self.USBRadioButton)
        modeLayout.addWidget(self.RTSPRadioButton)

        """rightLayout"""
        rightLayout = QVBoxLayout()
        rightLayout.addLayout(modeLayout)
        rightLayout.addWidget(self.cameraIndexComboBox)
        rightLayout.addWidget(self.cameraIPLineEdit)
        rightLayout.addWidget(self.resolutionComboBox)

        """topLayout"""
        topLayout = QHBoxLayout()
        topLayout.addLayout(leftLayout)
        topLayout.addLayout(rightLayout)

        """bottomLayout"""
        bottomLayout = QHBoxLayout()
        # bottomLayout.addWidget(self.cameraTestPushButton, 0, Qt.AlignCenter)
        bottomLayout.addWidget(self.savePushButton, 0, Qt.AlignCenter)

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addWidget(QLabel())
        layout.addLayout(bottomLayout)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        mode = root.find('camera').find('mode').text
        if mode == 'USB':
            self.USBRadioButton.setChecked(True)
            self.RTSPRadioButton.setChecked(False)
        elif mode == 'RTSP':
            self.USBRadioButton.setChecked(False)
            self.RTSPRadioButton.setChecked(True)

        camera_id = root.find('camera').find('camera_id').text
        self.cameraIndexComboBox.setCurrentText(camera_id)

        ip = root.find('camera').find('ip').text
        self.cameraIPLineEdit.setText(ip)

        width = root.find('camera').find('width').text
        height = root.find('camera').find('height').text
        self.resolutionComboBox.setCurrentText(width + '*' + height)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        mode = "USB" if self.USBRadioButton.isChecked() else "RTSP"
        root.find('camera').find('mode').text = mode

        camera_id = self.cameraIndexComboBox.currentText()
        root.find('camera').find('camera_id').text = camera_id

        ip = self.cameraIPLineEdit.text()
        root.find('camera').find('ip').text = ip

        width = self.resolutionComboBox.currentText().split('*')[0]
        root.find('camera').find('width').text = width

        height = self.resolutionComboBox.currentText().split('*')[1]
        root.find('camera').find('height').text = height
        tree.write(self.config_path)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: ignore this
        :return: None
        """
        self.load_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = CameraSettingsWidget('../appsettings.xml')
    win.show()
    sys.exit(app.exec_())
