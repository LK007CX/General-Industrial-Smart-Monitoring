#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QComboBox, QDoubleSpinBox, \
    QSpinBox, QToolButton, QHBoxLayout, QApplication


class ItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, class_list, output_pin_list, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self.class_list = class_list
        self.output_pin_list = output_pin_list
        self.output_mode_list = ["低脉冲", "高脉冲"]
        self._item = item  # keep a reference to the list item object

        self.classComboBox = QComboBox(objectName='classComboBox')  # 检测类别
        self.confirmFramesSpinBox = QSpinBox(objectName='confirmFrames')  # 确认帧数
        self.threshDoubleSpinBox = QDoubleSpinBox(objectName='threshDoubleSpinBox')  # 置信度
        self.outputPinComboBox = QComboBox(objectName='outputPinComboBox')  # 输出引脚
        self.outputTimeDoubleSpinBox = QDoubleSpinBox(objectName='outputTimeDoubleSpinBox')  # 输出时间
        self.outputModeComboBox = QComboBox(objectName='outputModeComboBox')  # 输出方式
        self.editToolButton = QToolButton(objectName='editPushButton')  # 编辑按钮
        self.saveToolButton = QToolButton(objectName='savePushButton')  # 保存按钮
        self.deleteToolButton = QToolButton(objectName='deletePushButton')  # 删除按钮
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """initialize data"""
        self.classComboBox.addItems(self.class_list)
        self.outputPinComboBox.addItems(self.output_pin_list)
        self.outputModeComboBox.addItems(self.output_mode_list)
        """set icon for button"""
        self.editToolButton.setIcon(QIcon(QPixmap('icon/edit.png')))
        self.saveToolButton.setIcon(QIcon(QPixmap('icon/save.png')))
        self.deleteToolButton.setIcon(QIcon(QPixmap('icon/delete.png')))
        """icon size"""
        self.editToolButton.setIconSize(QSize(20, 20))
        self.saveToolButton.setIconSize(QSize(20, 20))
        self.deleteToolButton.setIconSize(QSize(20, 20))
        """slots"""
        self.deleteToolButton.clicked.connect(self.doDeleteItem)
        self.editToolButton.clicked.connect(lambda: self.setReadOnly(False))
        self.saveToolButton.clicked.connect(lambda: self.setReadOnly(True))
        """fixed size"""
        self.classComboBox.setFixedWidth(100)
        self.confirmFramesSpinBox.setFixedWidth(100)
        self.threshDoubleSpinBox.setFixedWidth(100)
        self.outputPinComboBox.setFixedWidth(100)
        self.outputTimeDoubleSpinBox.setFixedWidth(100)
        self.outputModeComboBox.setFixedWidth(100)
        self.editToolButton.setMaximumWidth(50)
        self.saveToolButton.setMaximumWidth(50)
        self.deleteToolButton.setMaximumWidth(50)
        """data limit"""
        self.confirmFramesSpinBox.setMinimum(1)
        self.confirmFramesSpinBox.setMaximum(30)
        self.threshDoubleSpinBox.setMinimum(0.1)
        self.threshDoubleSpinBox.setMaximum(1.0)
        self.threshDoubleSpinBox.setSingleStep(0.05)
        self.outputTimeDoubleSpinBox.setMinimum(0.05)
        self.outputTimeDoubleSpinBox.setMaximum(0.2)
        self.outputTimeDoubleSpinBox.setSingleStep(0.05)
        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.classComboBox)
        layout.addWidget(self.confirmFramesSpinBox)
        layout.addWidget(self.threshDoubleSpinBox)
        layout.addWidget(self.outputPinComboBox)
        layout.addWidget(self.outputTimeDoubleSpinBox)
        layout.addWidget(self.outputModeComboBox)
        layout.addWidget(self.editToolButton)
        layout.addWidget(self.saveToolButton)
        layout.addWidget(self.deleteToolButton)
        self.setLayout(layout)

    def doDeleteItem(self):
        """
        Slot function for delete item.
        :return: None
        """
        self.itemDeleted.emit(self._item)

    def sizeHint(self):
        """
        Determine the height of the item.
        :return: None
        """
        return QSize(200, 40)

    def setReadOnly(self, if_read_only):
        """
        Set widgets read only.
        :param if_read_only: True or False
        :return: None
        """
        self.classComboBox.setDisabled(if_read_only)
        self.confirmFramesSpinBox.setDisabled(if_read_only)
        self.threshDoubleSpinBox.setDisabled(if_read_only)
        self.outputPinComboBox.setDisabled(if_read_only)
        self.outputTimeDoubleSpinBox.setDisabled(if_read_only)
        self.outputModeComboBox.setDisabled(if_read_only)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_list_ = ['person', 'ok', 'ng']
    output_pin_list_ = ['12', '14', '16', '18']
    item_ = QListWidgetItem()
    win = ItemWidget(class_list_, output_pin_list_, item_)
    win.show()
    sys.exit(app.exec_())
