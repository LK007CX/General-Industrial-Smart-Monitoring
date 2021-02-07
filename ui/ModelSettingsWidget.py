#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QLineEdit, \
    QComboBox, QSlider, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFileDialog, QApplication

from ui.DragListWidget import DragListWidget


class ModelSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(ModelSettingsWidget, self).__init__(*args, **kwargs)

        self.modelLabel = QLabel("选择模型")
        self.modelLineEdit = QLineEdit()
        self.modelToolButton = QToolButton()

        self.sizeLabel = QLabel("模型输入尺度")
        self.sizeComboBox = QComboBox()

        self.namesLabel = QLabel("标签文件")
        self.namesLineEdit = QLineEdit()
        self.namesToolButton = QToolButton()

        self.namesLabel_ = QLabel("检测标签")
        self.namesLineEdit_ = QLineEdit()

        self.threshLabel = QLabel("调节置信度")
        self.threshSlider = QSlider()

        self.threshToolButton = QToolButton()

        self.dragListWidget = DragListWidget()
        self.savePushButton = QPushButton("保存")

        self.config_path = config_path
        self.model_path = None
        self.names_path = None
        self.thresh = None
        self.category_num = None

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """fixed size"""
        self.modelLabel.setFixedWidth(100)
        self.sizeLabel.setFixedWidth(100)
        self.namesLabel.setFixedWidth(100)
        self.namesLabel_.setFixedWidth(100)
        self.threshLabel.setFixedWidth(100)
        self.savePushButton.setFixedWidth(100)

        size_list = ["288*288", "416*416", "608*608"]
        self.sizeComboBox.addItems(size_list)
        self.namesLineEdit_.setReadOnly(True)
        self.threshToolButton.setText("%")

        self.modelToolButton.setText('...')
        self.namesToolButton.setText('...')

        self.modelLineEdit.setReadOnly(True)
        self.namesLineEdit.setReadOnly(True)

        self.threshSlider.setMinimum(0)
        self.threshSlider.setMaximum(100)

        self.modelToolButton.clicked.connect(self.modelAction)
        self.namesToolButton.clicked.connect(self.namesAction)

        self.threshSlider.setOrientation(Qt.Horizontal)
        self.threshSlider.valueChanged.connect(self.threshAction)

        self.savePushButton.clicked.connect(self.saveAction)

        """layout"""
        layout = QVBoxLayout()
        modelLayout = QHBoxLayout()
        modelLayout.addWidget(self.modelLabel)
        modelLayout.addWidget(self.modelLineEdit)
        modelLayout.addWidget(self.modelToolButton)

        """sizeLayout"""
        sizeLayout = QHBoxLayout()
        sizeLayout.addWidget(self.sizeLabel)
        sizeLayout.addWidget(self.sizeComboBox)

        """namesLayout"""
        namesLayout = QHBoxLayout()
        namesLayout.addWidget(self.namesLabel)
        namesLayout.addWidget(self.namesLineEdit)
        namesLayout.addWidget(self.namesToolButton)

        """namesLayout_"""
        namesLayout_ = QHBoxLayout()
        namesLayout_.addWidget(self.namesLabel_)
        namesLayout_.addWidget(self.namesLineEdit_)

        """threshLayout"""
        threshLayout = QHBoxLayout()
        threshLayout.addWidget(self.threshLabel)
        threshLayout.addWidget(self.threshSlider)
        threshLayout.addWidget(self.threshToolButton)

        """layout"""
        layout.addLayout(modelLayout)
        layout.addLayout(sizeLayout)
        layout.addLayout(namesLayout)
        layout.addLayout(threshLayout)
        layout.addLayout(namesLayout_)
        layout.addWidget(self.dragListWidget)
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        self.setLayout(layout)

    def threshAction(self, val):
        """
        Change thresh.
        :param val: thresh
        :return: None
        """
        self.threshToolButton.setText(str(val) + "%")
        self.thresh = self.threshSlider.value() / 100

    def modelAction(self):
        """
        Change model.
        :return: None
        """
        # openfile_name = QFileDialog.getOpenFileName(self, '选择模型文件', './',
        #                                             'TensorRT model(*.trt)')
    
        openfile_name = QFileDialog.getOpenFileName(self, '选择模型文件', './',
                                                    'TensorRT model(*.*)')

        if openfile_name[0] != '':
            self.modelLineEdit.setText(str(openfile_name[0]).split('/')[-1])
            self.model_path = openfile_name[0]

    def namesAction(self):
        """
        Change names file.
        :return: None
        """
        CUSTOM_CLASSES_LIST = []
        openfile_name = QFileDialog.getOpenFileName(self, '选择标签文件', './',
                                                    '标签文件(*.names *.labels)')
        if openfile_name[0] != '':
            self.namesLineEdit.setText(str(openfile_name[0]).split('/')[-1])
            self.names_path = openfile_name[0]
        # try:
        with open(openfile_name[0]) as f:
            for line in f.readlines():
                if line != '':
                    CUSTOM_CLASSES_LIST.append(line.rstrip('\n'))
        # except Exception as e:
        #     print(e)
        temp = ''
        for val in CUSTOM_CLASSES_LIST:
            temp += val
            temp += '、'
        temp = temp[0:-1]
        self.namesLineEdit_.setText(temp)
        self.dragListWidget.initItems(CUSTOM_CLASSES_LIST)
        self.category_num = len(CUSTOM_CLASSES_LIST)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        modelpath = root.find('model').find('modelpath').text
        labelsfile = root.find('model').find('labelsfile').text
        thresh = root.find('model').find('thresh').text
        size = root.find('model').find('size').text

        CUSTOM_CLASSES_LIST = []
        # try:
        with open(labelsfile) as f:
            for line in f.readlines():
                if line != '':
                    CUSTOM_CLASSES_LIST.append(line.rstrip('\n'))
        # except Exception as e:
        #     print(e)
        temp = ''
        for val in CUSTOM_CLASSES_LIST:
            temp += val
            temp += '、'
        temp = temp[0:-1]

        self.dragListWidget.initItems(CUSTOM_CLASSES_LIST)
        self.modelLineEdit.setText(modelpath.split('/')[-1])
        self.namesLineEdit.setText(labelsfile.split('/')[-1])
        self.namesLineEdit_.setText(temp)
        self.threshSlider.setValue(float(thresh) * 100)
        self.sizeComboBox.setCurrentText(size)

        self.model_path = modelpath
        self.names_path = labelsfile
        self.thresh = thresh
        self.category_num = len(CUSTOM_CLASSES_LIST)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            root.find('model').find('modelpath').text = self.model_path
            root.find('model').find('labelsfile').text = self.names_path
            root.find('model').find('thresh').text = str(self.thresh)
            root.find('model').find('size').text = self.sizeComboBox.currentText()
            root.find('model').find('category_num').text = str(self.category_num)
            tree.write(self.config_path)
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
    app = QApplication(sys.argv)
    win = ModelSettingsWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
