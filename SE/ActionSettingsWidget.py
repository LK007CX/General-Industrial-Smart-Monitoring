#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QPushButton, QVBoxLayout, \
    QHBoxLayout, QListWidgetItem, QMessageBox, QApplication, QAbstractItemView

from SE.ActionHeaderWidget import ActionHeaderWidget
from SE.ActionWidget import ItemWidget


class DetectSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(DetectSettingsWidget, self).__init__(*args, **kwargs)

        self.config_path = config_path
        self.class_list = self.load_class_list()

        self.headerWidget = ActionHeaderWidget()
        self.detectListWidget = QListWidget()
        self.detectListWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.addPushButton = QPushButton("添加类别")
        self.deleteAllPushButton = QPushButton("删除全部类别")
        self.saveAllPushButton = QPushButton("保存更改")

        # self.load_config()
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        """slots"""
        self.addPushButton.clicked.connect(self.addDetectItem)
        self.deleteAllPushButton.clicked.connect(self.doClearItem)
        self.saveAllPushButton.clicked.connect(self.doSaveItem)
        """hBoxLayout"""
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addStretch()
        hBoxLayout.addWidget(self.addPushButton)
        hBoxLayout.addStretch()
        hBoxLayout.addWidget(self.deleteAllPushButton)
        hBoxLayout.addStretch()
        hBoxLayout.addWidget(self.saveAllPushButton)
        hBoxLayout.addStretch()

        """layout"""
        layout = QVBoxLayout()
        layout.addWidget(self.headerWidget)
        layout.addWidget(self.detectListWidget)
        layout.addLayout(hBoxLayout)
        self.setLayout(layout)

        """self"""
        self.resize(QSize(600, 300))
        self.setAttribute(Qt.WA_StyledBackground)

    def addDetectItem(self):
        """
        Add detect item.
        :return: None
        """
        item = QListWidgetItem(self.detectListWidget)
        item.setSizeHint(QSize(200, 50))
        widget = ItemWidget(self.class_list, item)
        widget.itemDeleted.connect(self.doDeleteItem)
        widget.setIndex(self.detectListWidget.count())
        self.detectListWidget.setItemWidget(item, widget)

    def doDeleteItem(self, item):
        """
        Delete item by index.
        :param item: item
        :return: None
        """
        row = self.detectListWidget.indexFromItem(item).row()
        item = self.detectListWidget.takeItem(row)
        self.detectListWidget.removeItemWidget(item)
        del item

    def doClearItem(self):
        """
        Clear all item in the list widdet.
        :return: None
        """
        for _ in range(self.detectListWidget.count()):
            item = self.detectListWidget.takeItem(0)
            self.detectListWidget.removeItemWidget(item)
            del item

    def doSaveItem(self):
        """
        Save item to application configuration.
        :return: None
        """
        self.resetIndex()
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()

            """remove all action"""
            for detect in root.findall('detect_items'):
                for action in detect.findall('item'):
                    detect.remove(action)

            """check for duplicate settings(class and output pin)"""
            pass

            """add item to application configuration"""
            for _ in range(self.detectListWidget.count()):

                item = self.detectListWidget.item(_)
                widget = self.detectListWidget.itemWidget(item)

                index = str(widget.indexLabel.text())
                category = str(widget.classComboBox.currentText())
                frames = str(widget.framesSpinBox.value())
                time = str(widget.timeSpinBox.value())
                thresh = str(widget.threshDoubleSpinBox.value())
                coordinate = str(widget.coordinateLabel.text())

                action = ET.Element('item')
                index_node = ET.SubElement(action, 'index')
                index_node.text = index
                category_node = ET.SubElement(action, 'category')
                category_node.text = category
                frames_node = ET.SubElement(action, 'frames')
                frames_node.text = frames
                time_node = ET.SubElement(action, 'time')
                time_node.text = time
                thresh_node = ET.SubElement(action, 'thresh')
                thresh_node.text = thresh
                coordinate_node = ET.SubElement(action, 'coordinate')
                coordinate_node.text = coordinate
                detect = root.find('detect_items')
                detect.extend((action,))

            tree.write(self.config_path)
            self.pretty_xml(root, '\t', '\n')
            tree.write(self.config_path)
        except Exception as e:
            print(e)

    def pretty_xml(self, element, indent, newline, level=0):
        """
        Beautify XML file.
        :param element: Element class
        :param indent: indent
        :param newline: line feed
        :param level: level
        :return:
        """
        if element:
            if (element.text is None) or element.text.isspace():
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
        temp = list(element)
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):
                subelement.tail = newline + indent * (level + 1)
            else:
                subelement.tail = newline + indent * level
            self.pretty_xml(subelement, indent, newline, level=level + 1)

    def load_class_list(self):
        tree = ET.parse(self.config_path)
        root = tree.getroot()
        labelsfile = root.find('model').find('labelsfile').text
        CUSTOM_CLASSES_LIST = []
        with open(labelsfile) as f:
            for line in f.readlines():
                if line != '':
                    CUSTOM_CLASSES_LIST.append(line.rstrip('\n'))
        return CUSTOM_CLASSES_LIST

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        try:
            self.doClearItem()
            tree = ET.parse(self.config_path)
            root = tree.getroot()
            for action in root.find('detect_items').findall('item'):
                index = action.find('index').text
                category = action.find('category').text
                frames = int(action.find('frames').text)
                time = float(action.find('time').text)
                thresh = float(action.find('thresh').text)
                coordinate = action.find('coordinate').text
                item = QListWidgetItem(self.detectListWidget)
                item.setSizeHint(QSize(200, 50))
                widget = ItemWidget(self.class_list, item)
                widget.itemDeleted.connect(self.doDeleteItem)
                widget.indexLabel.setText(index)
                widget.classComboBox.setCurrentText(category)
                widget.framesSpinBox.setValue(frames)
                widget.timeSpinBox.setValue(time)
                widget.threshDoubleSpinBox.setValue(thresh)
                widget.coordinateLabel.setText(coordinate)
                self.detectListWidget.setItemWidget(item, widget)
        except Exception as e:
            print(e)

    # def showEvent(self, QShowEvent):
    #     """
    #     Reload application configuration when widget show again.
    #     :param QShowEvent: ignore this
    #     :return: None
    #     """
    #     self.load_config()

    def resetIndex(self):
        for i in range(self.detectListWidget.count()):
            item = self.detectListWidget.item(i)
            widget = self.detectListWidget.itemWidget(item)
            widget.setIndex(str(i+1))


if __name__ == '__main__':
    class_list_ = ['person', 'ok', 'ng']
    app = QApplication(sys.argv)
    win = DetectSettingsWidget('../appconfig/appconfig_se.xml')
    win.show()
    sys.exit(app.exec_())
