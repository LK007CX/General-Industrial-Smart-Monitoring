#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import time
from collections import deque

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QWidget, QListView, QVBoxLayout, QApplication

from ui.HistoryItemWidget import HistoryItemWidget
from ui.SortFilterProxyModel import SortFilterProxyModel


class HistoryListView(QWidget):
    def __init__(self, *args, **kwargs):
        super(HistoryListView, self).__init__(*args, **kwargs)
        self.historyListView = QListView()
        self.historyItemDeque = deque(maxlen=50)
        self.dmodel = QStandardItemModel(self.historyListView)
        self.fmodel = SortFilterProxyModel(self.historyListView)

        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.fmodel.setSourceModel(self.dmodel)
        self.historyListView.setModel(self.fmodel)
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.historyListView)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_StyledBackground)

    def test_data(self):
        """
        Test data.
        :return: None
        """
        for i in range(5):
            times = time.time()
            value = '{}'.format(times)
            item = QStandardItem(value)
            self.dmodel.appendRow(item)
            index = self.fmodel.mapFromSource(item.index())
            image = cv2.imread('../icon/back.png')
            widget = HistoryItemWidget(image, str(times), str(times))
            widget.raise_()
            item.setSizeHint(widget.sizeHint())
            self.historyListView.setIndexWidget(index, widget)
            self.fmodel.sort(0, Qt.DescendingOrder)
            time.sleep(0.01)

    def addItem(self, image, label, time_, coordinate):
        """
        Add item to the history listview.
        :param image: image
        :param label: label
        :param time_: time
        :return:
        """
        if self.historyListView.model().rowCount() == 10:
            self.historyListView.model().removeRow(9)
        times = time.time()
        value = '{}'.format(times)
        item = QStandardItem(value)
        item.setForeground(QColor("#19232D"))
        self.dmodel.appendRow(item)
        index = self.fmodel.mapFromSource(item.index())
        widget = HistoryItemWidget(image, label, time_, coordinate, item)
        item.setSizeHint(widget.sizeHint())
        self.historyListView.setIndexWidget(index, widget)
        self.fmodel.sort(0, Qt.DescendingOrder)

    def doDeleteItem(self, item):
        """
        Delete item.
        :param item: item
        :return: None
        """
        row = self.listWidget.indexFromItem(item).row()
        item = self.listWidget.takeItem(row)
        self.listWidget.removeItemWidget(item)
        del item


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = HistoryListView()
    win.show()
    sys.exit(app.exec_())
