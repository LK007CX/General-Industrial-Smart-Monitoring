#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 13:44
# @Author  : Lee
# @Email   : 1317108121@qq.com
# @File    : ModelTransformationWidget.py
# @Software: PyCharm
import sys

from PyQt5.QtWidgets import *


class ModelTransformationWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(ModelTransformationWidget, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ModelTransformationWidget()
    win.show()
    sys.exit(app.exec_())
