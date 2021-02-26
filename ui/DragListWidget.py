#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QCursor
from PyQt5.QtWidgets import QRubberBand, QListWidget, QListWidgetItem, QLabel, \
    QGraphicsOpacityEffect


class DragListWidget(QListWidget):
    """QListWidget that can be dragged out."""

    def __init__(self, *args, **kwargs):
        super(DragListWidget, self).__init__(*args, **kwargs)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(self.NoEditTriggers)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragOnly)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setSelectionMode(self.ContiguousSelection)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(5)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        # self.setDragDropMode(self.InternalMove)

    def startDrag(self, supportedActions):
        """
        Preview renderings when dragging.
        Here is a demonstration of splicing all the screenshots of items.

        :param supportedActions:
        :return: None
        """
        items = self.selectedItems()
        drag = QDrag(self)
        mimeData = self.mimeData(items)
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        drag.exec_(supportedActions)

    def mousePressEvent(self, event):
        """
        The list box click event is used to set the start position of the box selection tool
        :param event: event
        :return: None
        """
        super(DragListWidget, self).mousePressEvent(event)
        if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        """
        Click release event in the list box to hide the box selection tool.
        :param event: event
        :return: None
        """
        super(DragListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        """
        List box mouse movement event, used to set the rectangular range of the box selection tool.
        :param event: event
        :return: None
        """
        super(DragListWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

    def makeItem(self, size, cname):
        """
        Make item.
        :param size: size
        :param cname: cname
        :return: None
        """
        item = QListWidgetItem(self)
        item.setData(Qt.UserRole + 1, cname)
        item.setSizeHint(size)
        label = QLabel(self)
        label.setMargin(2)
        label.resize(size)
        label.setText(cname)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('''background-color: #014A6F; color: white;border-radius: 5px;''')
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.75)
        label.setGraphicsEffect(op)
        label.setAutoFillBackground(True)
        self.setItemWidget(item, label)

    def initItems(self, name_list):
        """
        Initialize items.
        :param name_list: name list
        :return: None
        """
        self.clearItem()
        size = QSize(80, 30)
        for cname in name_list:
            self.makeItem(size, cname)

    def clearItem(self):
        """
        Clear all items.
        :return:
        """
        for _ in range(self.count()):
            item = self.takeItem(0)
            self.removeItemWidget(item)
            del item
