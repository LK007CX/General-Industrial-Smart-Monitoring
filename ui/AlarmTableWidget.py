#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView, \
    QTableWidgetItem


class AlarmTableWidget(QTableWidget):
    def __init__(self, config_path, row_count=10, column_count=2, *args, **kwargs):
        super(AlarmTableWidget, self).__init__(*args, **kwargs)

        self.setColumnCount(column_count)
        self.setRowCount(row_count)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeaderLabels(["报警类名", "报警次数"])
        self.category_list = []
        self.configPath = config_path
        self.test_data()
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAlternatingRowColors(True)

    def append_history(self, column, start_time, result=None):
        """
        Append history.
        :param column: column
        :param start_time: start time
        :param result: result
        :return: None
        """
        item0 = QTableWidgetItem(start_time)
        item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item1 = QTableWidgetItem(result)
        item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setItem(column, 0, item0)
        self.setItem(column, 1, item1)

    def test_data(self):
        """
        Test data.
        :return: None
        """
        tree = ET.parse(self.configPath)
        root = tree.getroot()
        for action in root.find('detect_items').findall('item'):
            category = action.find('category').text
            self.category_list.append(category)
        self.setRowCount(len(self.category_list))
        for i in range(len(self.category_list)):
            item0 = QTableWidgetItem(self.category_list[i])
            item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(i, 0, item0)
            item1 = QTableWidgetItem(str(0))
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(i, 1, item1)

    def changeResult(self, category):
        """
        Change result.
        :param category:
        :return: None
        """
        if category in self.category_list:
            index = self.category_list.index(category)
            num = int(self.item(index, 1).text())
            num += 1
            item = QTableWidgetItem(str(num))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 1, item)
