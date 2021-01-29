#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication


class DetectHeaderWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(DetectHeaderWidget, self).__init__(*args, **kwargs)

        self.label1 = QLabel("检测类别")
        self.label2 = QLabel("确认帧数")
        self.label3 = QLabel("置信度")
        self.label4 = QLabel("输出引脚")
        self.label5 = QLabel("输出时间")
        self.label6 = QLabel("输出模式")
        self.label7 = QLabel("编辑")
        self.label8 = QLabel("锁定")
        self.label9 = QLabel("删除")

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """fixed size"""
        self.label1.setFixedWidth(100)
        self.label2.setFixedWidth(100)
        self.label3.setFixedWidth(100)
        self.label4.setFixedWidth(100)
        self.label5.setFixedWidth(100)
        self.label6.setFixedWidth(100)
        self.label7.setFixedWidth(50)
        self.label8.setFixedWidth(50)
        self.label9.setFixedWidth(50)

        """Set labels center"""
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label3.setAlignment(Qt.AlignCenter)
        self.label4.setAlignment(Qt.AlignCenter)
        self.label5.setAlignment(Qt.AlignCenter)
        self.label6.setAlignment(Qt.AlignCenter)
        self.label7.setAlignment(Qt.AlignCenter)
        self.label8.setAlignment(Qt.AlignCenter)
        self.label9.setAlignment(Qt.AlignCenter)

        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.label4)
        layout.addWidget(self.label5)
        layout.addWidget(self.label6)
        layout.addWidget(self.label7)
        layout.addWidget(self.label8)
        layout.addWidget(self.label9)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DetectHeaderWidget()
    win.show()
    sys.exit(app.exec_())
