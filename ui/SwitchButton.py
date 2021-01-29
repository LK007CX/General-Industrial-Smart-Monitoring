#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import pyqtSignal, QTimer, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication


class SwitchButton(QPushButton):
    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(SwitchButton, self).__init__(parent)

        self.checked = False
        self.bgColorOff = QColor(233, 233, 235)
        self.bgColorOn = QColor(86, 200, 94)

        self.sliderColorOff = QColor(255, 255, 255)
        self.sliderColorOn = QColor(255, 255, 255)

        self.textColorOff = QColor(143, 143, 143)
        self.textColorOn = QColor(255, 255, 255)

        self.textOff = "OFF"
        self.textOn = "ON"

        self.space = 3
        self.rectRadius = 5

        self.step = self.width() / 50
        self.startX = 0
        self.endX = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateValue)

        self.setFont(QFont("Microsoft Yahei", 10))

    def updateValue(self):
        """
        Update value.
        :return: None
        """
        if self.checked:
            if self.startX < self.endX:
                self.startX = self.startX + self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        else:
            if self.startX > self.endX:
                self.startX = self.startX - self.step
            else:
                self.startX = self.endX
                self.timer.stop()
        self.update()

    def mousePressEvent(self, event):
        """
        Mouse press event.
        :param event: event
        :return: None
        """
        self.checked = not self.checked
        self.checkedChanged.emit(self.checked)
        self.step = self.width() / 50
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def setChecked(self, boolean):
        """
        Set self checked or unchecked.
        :param boolean: checked?
        :return: None
        """
        if self.checked == boolean:
            return
        self.checked = not self.checked
        self.checkedChanged.emit(self.checked)
        self.step = self.width() / 50
        if self.checked:
            self.endX = self.width() - self.height()
        else:
            self.endX = 0
        self.timer.start(5)

    def paintEvent(self, event):
        """
        Paint event.
        :param event: event
        :return: None
        """
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawBg(event, painter)
        self.drawSlider(event, painter)
        painter.end()

    def drawText(self, event, painter):
        """
        Draw text.
        :param event: event
        :param painter: painter
        :return: None
        """
        painter.save()
        if self.checked:
            painter.setPen(self.textColorOn)
            painter.drawText(0, 0, self.width() / 2 + self.space * 2, self.height(), Qt.AlignCenter, self.textOn)
        else:
            painter.setPen(self.textColorOff)
            painter.drawText(self.width() / 2, 0, self.width() / 2 - self.space, self.height(), Qt.AlignCenter,
                             self.textOff)
        painter.restore()

    def drawBg(self, event, painter):
        """
        Draw background.
        :param event: event
        :param painter: painter
        :return: None
        """
        painter.save()
        painter.setPen(Qt.NoPen)

        if self.checked:
            painter.setBrush(self.bgColorOn)
        else:
            painter.setBrush(self.bgColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        radius = rect.height() / 2
        circleWidth = rect.height()

        path = QPainterPath()
        path.moveTo(radius, rect.left())
        path.arcTo(QRectF(rect.left(), rect.top(), circleWidth, circleWidth), 90, 180)
        path.lineTo(rect.width() - radius, rect.height())
        path.arcTo(QRectF(rect.width() - rect.height(), rect.top(), circleWidth, circleWidth), 270, 180)
        path.lineTo(radius, rect.top())

        painter.drawPath(path)
        painter.restore()

    def drawSlider(self, event, painter):
        """
        Draw slider.
        :param event: event
        :param painter: painter
        :return: None
        """
        painter.save()

        if self.checked:
            painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
            painter.setBrush(self.sliderColorOn)
        else:
            painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
            painter.setBrush(self.sliderColorOff)

        rect = QRect(0, 0, self.width(), self.height())
        sliderWidth = rect.height() - self.space * 2
        sliderRect = QRect(self.startX + self.space, self.space, sliderWidth, sliderWidth)
        painter.drawEllipse(sliderRect)

        painter.restore()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.switchBtn = SwitchButton(self)
        self.switchBtn.resize(QSize(50, 30))
        self.switchBtn.checkedChanged.connect(self.getState)

        self.setStyleSheet('''background-color: white;''')

    def getState(self, checked):
        print("checked=", checked)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
