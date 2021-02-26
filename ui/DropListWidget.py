#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class DropListWidget(QListWidget):
    # 可以拖进来的QListWidget

    def __init__(self, *args, **kwargs):
        super(DropListWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(5)
        """Enable drag & drop ordering of items."""
        self.setDragDropMode(self.InternalMove)
        self.test_data()

    def makeItem(self, size, cname):
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)  # 把数据放进自定义的data里面
        item.setSizeHint(size)
        widget = QLabel(self)  # 自定义控件
        widget.setMargin(2)  # 往内缩进2
        widget.resize(size)
        widget.setText(cname)
        # widget.setStyleSheet('''background-color: orangered; color: white;border-radius: 5px;
        # ''')
        self.setItemWidget(item, widget)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if not mimeData.property('myItems'):
            event.ignore()
        else:
            event.acceptProposedAction()

    # def dragEnterEvent(self, event):
    #     mimeData = event.mimeData()
    #     if not mimeData.property('myItems'):
    #         items = self.selectedItems()
    #         mineData = self.mimeData(items)
    #         mineData.setProperty('myItems', items)
    #         event.mimeData() =
    #     else:
    #         event.acceptProposedAction()

    def dropEvent(self, event):
        # 获取拖放的items
        items = event.mimeData().property("myItems")
        print(items)
        print(dir(items))
        print(type(event.mimeData()))
        event.accept()
        for item in items:
            # 取出item里的data并生成item
            self.makeItem(QSize(100, 30), item.data(Qt.UserRole + 1))

    def test_data(self):
        for x in range(1, 11):
            self.addItem('Item {:02d}'.format(x))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DropListWidget()
    widget.show()

    sys.exit(app.exec_())
