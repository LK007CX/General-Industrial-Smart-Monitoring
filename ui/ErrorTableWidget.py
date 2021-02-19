#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, \
    QAbstractItemView, QTableWidgetItem


class ErrorTableWidget(QTableWidget):
    def __init__(self, row_count=20, column_count=3, *args, **kwargs):
        super(ErrorTableWidget, self).__init__(*args, **kwargs)
        self.setRowCount(row_count)
        self.setColumnCount(column_count)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(["编号", "异常描述", "时间"])
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAlternatingRowColors(True)

    def append_history(self, column, start_time, result=None):
        """
        Append history.
        :param column: column index
        :param start_time: start time
        :param result: result
        :return: None
        """
        item0 = QTableWidgetItem(start_time)
        item0.setTextAlignment(Qt.AlignHCenter)
        item1 = QTableWidgetItem(result)
        item1.setTextAlignment(Qt.AlignHCenter)
        self.setItem(column, 0, item0)
        self.setItem(column, 1, item1)
