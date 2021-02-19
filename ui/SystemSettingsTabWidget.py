#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QTabWidget

from ui.ApplicationSettingsWidget import ApplicationSettingWidget
from ui.CameraSettingsWidget import CameraSettingsWidget
from ui.DataUploadSettingsWidget import DataUploadSettingsWidget
from ui.DetectSettingsWidget import DetectSettingsWidget
from ui.ImageSettingsWidget import ImageSettingsWidget
from ui.InputSettingsWidget import InputSettingsWidget
from ui.ModelSettingsWidget import ModelSettingsWidget
from ui.RemoteCVSettingsWidget import RemoteCVSettingsWidget


class SystemSettingsTabWidget(QTabWidget):
    def __init__(self, config_path, *args, **kwargs):
        super(SystemSettingsTabWidget, self).__init__(*args, **kwargs)

        input_pin_list_ = ['3', '5', '7', '8']
        output_pin_list_ = ['13', '15', '16', '18']

        self.cameraSettingsTab = CameraSettingsWidget(config_path)
        self.inputSettingsTab = InputSettingsWidget(config_path, input_pin_list_)
        self.outputSettingsTab = ImageSettingsWidget(config_path)
        self.detectSettingsTab = DetectSettingsWidget(config_path, output_pin_list_)
        self.modelSettinsTab = ModelSettingsWidget(config_path)
        self.dataUploadTab = DataUploadSettingsWidget(config_path)
        self.remoteCVTab = RemoteCVSettingsWidget(config_path)
        self.applicationSettingsTab = ApplicationSettingWidget(config_path)
        self.init_ui()
        self.center()

    def init_ui(self):
        """
        Initialize UI.
        :return:
        """
        self.addTab(self.cameraSettingsTab, "相机参数设置")
        self.addTab(self.inputSettingsTab, "输入模式设置")
        self.addTab(self.outputSettingsTab, "影像信息设置")
        self.addTab(self.detectSettingsTab, "检测项目设置")
        self.addTab(self.modelSettinsTab, "模型参数设置")
        self.addTab(self.dataUploadTab, "数据上报设置")
        self.addTab(self.remoteCVTab, "远程视频推送")
        self.addTab(self.applicationSettingsTab, "系统参数设置")
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(QPixmap('icon/logo.png')))
        self.setAttribute(Qt.WA_StyledBackground)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SystemSettingsTabWidget("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
