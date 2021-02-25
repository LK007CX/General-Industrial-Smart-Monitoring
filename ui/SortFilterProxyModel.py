#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QSortFilterProxyModel, Qt


class SortFilterProxyModel(QSortFilterProxyModel):

    def lessThan(self, source_left, source_right):
        if not source_left.isValid() or not source_right.isValid():
            return False
        leftData = self.sourceModel().data(source_left)
        rightData = self.sourceModel().data(source_right)
        if self.sortOrder() == Qt.DescendingOrder:
            return leftData < rightData
        return super(SortFilterProxyModel, self).lessThan(source_left, source_right)