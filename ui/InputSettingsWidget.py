#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QComboBox, \
    QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, \
    QSplitter, QApplication


class InputSettingsWidget(QWidget):

    def __init__(self, config_path, input_pin_list, *args, **kwargs):
        super(InputSettingsWidget, self).__init__(*args, **kwargs)
        self.inputPinList = input_pin_list

        self.output_mode_list = ["低脉冲", "高脉冲"]
        self.input_mode_label = QLabel("触发类型")

        self.continuousDetectRadioButton = QRadioButton("持续检测")
        self.levelTriggerRadioButton = QRadioButton("电平触发检测")
        self.levelTriggerSettingsLabel = QLabel("电平触发设置：")
        self.inputPinLabel = QLabel("触发引脚")
        self.inputPinComboBox = QComboBox()
        self.triggerModeLabel = QLabel("触发电平")
        self.triggerModeComboBox = QComboBox()
        self.timeDelayLabel = QLabel("触发时延(ms)")
        self.timeDelaySpinBox = QSpinBox()
        self.detectTimeLabel = QLabel("检测时间(ms)")
        self.detectTimeSpinBox = QSpinBox()
        self.savePushButton = QPushButton("保存")
        self.spacer = QLabel()

        self.configPath = config_path

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.inputPinComboBox.addItems(self.inputPinList)
        self.triggerModeComboBox.addItems(self.output_mode_list)

        """data limit"""
        self.timeDelaySpinBox.setMinimum(10)
        self.timeDelaySpinBox.setMaximum(10000)
        self.timeDelaySpinBox.setSingleStep(10)
        self.detectTimeSpinBox.setMinimum(0)
        self.detectTimeSpinBox.setMaximum(60)
        self.detectTimeSpinBox.setSingleStep(1)

        """size"""
        self.spacer.setFixedWidth(100)
        self.continuousDetectRadioButton.setFixedWidth(100)
        self.levelTriggerRadioButton.setFixedWidth(100)
        self.inputPinLabel.setFixedWidth(100)
        self.triggerModeLabel.setFixedWidth(100)
        self.timeDelayLabel.setFixedWidth(100)
        self.detectTimeLabel.setFixedWidth(100)
        self.inputPinComboBox.setFixedWidth(100)
        self.triggerModeComboBox.setFixedWidth(100)
        self.timeDelaySpinBox.setFixedWidth(100)
        self.detectTimeSpinBox.setFixedWidth(100)

        """alignment"""
        self.inputPinLabel.setAlignment(Qt.AlignCenter)
        self.triggerModeLabel.setAlignment(Qt.AlignCenter)
        self.timeDelayLabel.setAlignment(Qt.AlignCenter)
        self.detectTimeLabel.setAlignment(Qt.AlignCenter)

        """slots"""
        self.savePushButton.clicked.connect(self.saveAction)

        """modeLayout"""
        modeLayout = QHBoxLayout()
        modeLayout.addWidget(self.continuousDetectRadioButton)
        modeLayout.addWidget(self.spacer)
        modeLayout.addWidget(self.levelTriggerRadioButton)
        modeLayout.addWidget(self.spacer)

        """modeLayout"""
        levelTriggerLabelLayout = QHBoxLayout()
        levelTriggerLabelLayout.addWidget(self.inputPinLabel)
        levelTriggerLabelLayout.addWidget(self.triggerModeLabel)
        levelTriggerLabelLayout.addWidget(self.timeDelayLabel)
        levelTriggerLabelLayout.addWidget(self.detectTimeLabel)

        """levelTriggerLayout"""
        levelTriggerLayout = QHBoxLayout()
        levelTriggerLayout.addWidget(self.inputPinComboBox)
        levelTriggerLayout.addWidget(self.triggerModeComboBox)
        levelTriggerLayout.addWidget(self.timeDelaySpinBox)
        levelTriggerLayout.addWidget(self.detectTimeSpinBox)

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(modeLayout)
        layout.addWidget(QLabel())
        layout.addLayout(levelTriggerLabelLayout)
        layout.addLayout(levelTriggerLayout)
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
            tree = ET.parse(self.configPath)
            root = tree.getroot()

            mode = root.find('input').find('mode').text
            if mode == "continuous detect":
                self.continuousDetectRadioButton.setChecked(True)
                self.levelTriggerRadioButton.setChecked(False)
            elif mode == "level trigger":
                self.continuousDetectRadioButton.setChecked(False)
                self.levelTriggerRadioButton.setChecked(True)

            inputpin = root.find('input').find('inputpin').text
            self.inputPinComboBox.setCurrentText(inputpin)

            triggermode = root.find('input').find('triggermode').text
            if triggermode == "low pulse":
                triggermode = "低脉冲"
            elif triggermode == "high pulse":
                triggermode = "高脉冲"
            self.triggerModeComboBox.setCurrentText(triggermode)

            timedelay = root.find('input').find('timedelay').text
            self.timeDelaySpinBox.setValue(int(timedelay))

            detecttime = root.find('input').find('detecttime').text
            self.detectTimeSpinBox.setValue(int(detecttime))
        except Exception as e:
            print(e)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        try:
            tree = ET.parse(self.configPath)
            root = tree.getroot()

            mode = "continuous detect" if self.continuousDetectRadioButton.isChecked() else "level trigger"
            root.find('input').find('mode').text = mode

            inputpin = self.inputPinComboBox.currentText()
            root.find('input').find('inputpin').text = inputpin

            triggermode = self.triggerModeComboBox.currentText()
            if triggermode == "低脉冲":
                triggermode = "low pulse"
            elif triggermode == "高脉冲":
                triggermode = "high pulse"
            root.find('input').find('triggermode').text = triggermode

            timedelay = self.timeDelaySpinBox.value()
            root.find('input').find('timedelay').text = str(timedelay)

            detecttime = self.detectTimeSpinBox.value()
            root.find('input').find('detecttime').text = str(detecttime)

            tree.write(self.configPath)
        except Exception as e:
            print(e)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: event
        :return: None
        """
        self.load_config()


if __name__ == '__main__':
    output_pin_list_ = ['12', '14', '16', '18']
    app = QApplication(sys.argv)
    win = InputSettingsWidget("../appconfig/appconfig.xml", output_pin_list_)
    win.show()
    sys.exit(app.exec_())
