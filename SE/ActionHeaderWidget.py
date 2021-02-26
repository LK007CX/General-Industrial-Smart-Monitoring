#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication


class ActionHeaderWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(ActionHeaderWidget, self).__init__(*args, **kwargs)

        self.indexLabel = QLabel("序号")
        self.classLabel = QLabel("检测类别")
        self.framesLabel = QLabel("确认帧数")
        self.timeLabel = QLabel("确认时间")
        self.threshLabel = QLabel("置信度")
        self.coordinateLabel = QLabel("ROI信息")
        self.ROILabel = QLabel("ROI")
        self.deleteLabel = QLabel("删除")

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """

        """fixed size"""
        self.indexLabel.setFixedWidth(50)
        self.classLabel.setFixedWidth(100)
        self.framesLabel.setFixedWidth(100)
        self.timeLabel.setFixedWidth(100)
        self.threshLabel.setFixedWidth(100)
        self.coordinateLabel.setFixedWidth(200)
        self.ROILabel.setFixedWidth(50)
        self.deleteLabel.setFixedWidth(50)

        """Set labels center"""
        self.indexLabel.setAlignment(Qt.AlignCenter)
        self.classLabel.setAlignment(Qt.AlignCenter)
        self.framesLabel.setAlignment(Qt.AlignCenter)
        self.timeLabel.setAlignment(Qt.AlignCenter)
        self.threshLabel.setAlignment(Qt.AlignCenter)
        self.coordinateLabel.setAlignment(Qt.AlignCenter)
        self.ROILabel.setAlignment(Qt.AlignCenter)
        self.deleteLabel.setAlignment(Qt.AlignCenter)

        """layout"""
        layout = QHBoxLayout()
        layout.addWidget(self.indexLabel)
        layout.addWidget(self.classLabel)
        layout.addWidget(self.framesLabel)
        layout.addWidget(self.timeLabel)

        layout.addWidget(self.threshLabel)
        layout.addWidget(self.coordinateLabel)
        layout.addWidget(self.ROILabel)
        layout.addWidget(self.deleteLabel)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ActionHeaderWidget()
    win.show()
    sys.exit(app.exec_())
