#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

import cv2
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QComboBox, QDoubleSpinBox, \
    QSpinBox, QToolButton, QHBoxLayout, QApplication, QLabel


class ItemWidget(QWidget):
    itemDeleted = pyqtSignal(QListWidgetItem)

    def __init__(self, class_list, item, *args, **kwargs):
        super(ItemWidget, self).__init__(*args, **kwargs)
        self.class_list = class_list
        self._item = item  # keep a reference to the list item object
        self.img = cv2.imread("../icon/back.png", cv2.IMREAD_ANYCOLOR)

        self.indexLabel = QLabel("0")
        self.classComboBox = QComboBox(objectName='classComboBox')  # 检测类别
        self.framesSpinBox = QSpinBox(objectName='confirmFrames')  # 确认帧数
        self.timeSpinBox = QSpinBox(objectName='confirmTime')  # 确认时间
        self.threshDoubleSpinBox = QDoubleSpinBox(objectName='threshDoubleSpinBox')  # 置信度
        self.coordinateLabel = QLabel("(100, 100) (100, 100)", objectName="coordinateLabel")
        self.ROIToolButton = QToolButton(objectName="ROIToolButton")
        self.deleteToolButton = QToolButton(objectName='deleteToolButton')  # 删除按钮
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """initialize data"""
        self.classComboBox.addItems(self.class_list)
        """set icon for button"""
        self.ROIToolButton.setIcon(QIcon(QPixmap('icon/roi.png')))
        self.deleteToolButton.setIcon(QIcon(QPixmap('icon/delete.png')))
        """icon size"""
        self.ROIToolButton.setIconSize(QSize(20, 20))
        self.deleteToolButton.setIconSize(QSize(20, 20))
        """slots"""
        self.deleteToolButton.clicked.connect(self.doDeleteItem)
        """fixed size"""
        self.indexLabel.setFixedWidth(50)
        self.classComboBox.setFixedWidth(100)
        self.framesSpinBox.setFixedWidth(100)
        self.timeSpinBox.setFixedWidth(100)
        self.threshDoubleSpinBox.setFixedWidth(100)
        self.coordinateLabel.setFixedWidth(200)
        self.ROIToolButton.setFixedWidth(50)
        self.deleteToolButton.setFixedWidth(50)
        """data limit"""
        self.framesSpinBox.setMinimum(1)
        self.framesSpinBox.setMaximum(30)
        self.threshDoubleSpinBox.setMinimum(0.1)
        self.threshDoubleSpinBox.setMaximum(1.0)
        self.threshDoubleSpinBox.setSingleStep(0.05)

        """alignment"""
        self.indexLabel.setAlignment(Qt.AlignCenter)

        self.coordinateLabel.setAlignment(Qt.AlignCenter)

        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.indexLabel)
        layout.addWidget(self.classComboBox)
        layout.addWidget(self.framesSpinBox)
        layout.addWidget(self.timeSpinBox)
        layout.addWidget(self.threshDoubleSpinBox)
        layout.addWidget(self.coordinateLabel)
        layout.addWidget(self.ROIToolButton)
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

    def editROI(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.onMouseAction)
        cv2.imshow('image', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def onMouseAction(self, event, x, y, flags, param):
        position1, position2 = None, None

        image = self.img.copy()

        if event == cv2.EVENT_LBUTTONDOWN:  # 按下左键
            position1 = (x, y)  # 获取鼠标的坐标(起始位置)

        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  # 按住左键拖曳不放开
            cv2.rectangle(image, position1, (x, y), (0, 255, 0), 3)  # 画出矩形选定框
            cv2.imshow('image', image)

        elif event == cv2.EVENT_LBUTTONUP:  # 放开左键
            position2 = (x, y)  # 获取鼠标的最终位置
            cv2.rectangle(image, position1, position2, (0, 0, 255), 3)  # 画出最终的矩形
            cv2.imshow('image', image)

            min_x = min(position1[0], position2[0])  # 获得最小的坐标，因为可以由下往上拖动选定框
            min_y = min(position1[1], position2[1])
            width = abs(position1[0] - position2[0])  # 切割坐标
            height = abs(position1[1] - position2[1])

            cut_img = img[min_y:min_y + height, min_x:min_x + width]
            cv2.imshow('Cut', cut_img)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    class_list_ = ['person', 'ok', 'ng']
    output_pin_list_ = ['12', '14', '16', '18']
    item_ = QListWidgetItem()
    win = ItemWidget(class_list_, item_)
    win.show()
    sys.exit(app.exec_())
