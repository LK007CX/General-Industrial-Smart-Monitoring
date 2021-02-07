#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QDoubleSpinBox, \
    QComboBox, QPushButton, QHBoxLayout, QVBoxLayout, \
    QSplitter, QApplication

from ui.SwitchButton import SwitchButton


class DataUploadSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(DataUploadSettingsWidget, self).__init__(*args, **kwargs)

        self.config_path = config_path

        self.enableLabel = QLabel("启用数据上报")
        self.enableSwitchButton = SwitchButton()

        self.serverAddressLabel = QLabel("服务器地址")
        self.serverAddressLineEdit = QLineEdit("服务器地址")

        self.connectTimeoutLabel = QLabel("连接超时时间(s)")
        self.connectTimeoutDoubleSpinBox = QDoubleSpinBox()

        self.postTimeoutLabel = QLabel("post超时时间(s)")
        self.postTimeoutDoubleSpinBox = QDoubleSpinBox()

        self.hostNameLabel = QLabel("Edge装置名称")  # host_name
        self.hostNameLineEdit = QLineEdit("Edge装置名称")

        self.lineIDLabel = QLabel("线别")  # line_id
        self.lineIDLineEdit = QLineEdit("线别")

        self.eqpIDLabel = QLabel("机台代码")  # eqp_id
        self.eqpIDLineEdit = QLineEdit("机台代码")

        self.stationIDLabel = QLabel("工作站")  # station_id
        self.stationIDLineEdit = QLineEdit("工作站")

        self.opIDLabel = QLabel("站点")  # op_id
        self.opIDLineEdit = QLineEdit("站点")

        self.siteLabel = QLabel("厂别")  # fab_id
        self.siteComboBox = QComboBox()

        self.processStageLabel = QLabel("制程区域")  # process_stage
        self.processStageLineEdit = QLineEdit("制程区域")

        self.projectIDLabel = QLabel("Project ID")  # project_id
        self.projectIDLineEdit = QLineEdit("Project ID")

        self.projectNameLabel = QLabel("Project Name")  # project_name
        self.projectNameLineEdit = QLineEdit("Project Name")

        self.imageFileSuffixLabel = QLabel("图片后缀名")  # image_ext_name
        self.imageFileSuffixLineEdit = QLineEdit("图片后缀名")

        self.modelNameLabel = QLabel("模型名称")  # model_name
        self.modelNameLineEdit = QLineEdit("模型名称")

        self.modelVersionLabel = QLabel("模型版本")  # model_version
        self.modelVersionLineEdit = QLineEdit("模型版本")

        self.modelIterationLabel = QLabel("模型训练次数")  # model_iter
        self.modelIterationLineEdit = QLineEdit("模型训练次数")

        self.modelLabelsLabel = QLabel("模型标签")
        self.modelLabelsLineEdit = QLineEdit("模型标签")

        self.modelTypeLabel = QLabel("模型类型")
        self.modelTypeComboBox = QComboBox()

        self.predictTypeLabel = QLabel("Predict Type")
        self.predictTypeComboBox = QComboBox()

        self.savePushButton = QPushButton("保存")

        self.spaceLabel1 = QLabel()

        self.spaceLabel2 = QLabel()

        self.spaceLabel3 = QLabel()

        self.spaceLabel4 = QLabel()

        self.enableWidget = QWidget()

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.connectTimeoutDoubleSpinBox.setMinimum(0.1)
        self.connectTimeoutDoubleSpinBox.setMaximum(5)
        self.connectTimeoutDoubleSpinBox.setSingleStep(0.1)
        self.postTimeoutDoubleSpinBox.setMinimum(0.1)
        self.postTimeoutDoubleSpinBox.setMaximum(5)
        self.postTimeoutDoubleSpinBox.setSingleStep(0.1)

        site_list = ["S01", "S02", "S06"]
        self.siteComboBox.addItems(site_list)

        model_type = ["1.YOLOv3.KS (M04)", "2.YOLOv3-Tiny (M06)", "3.YOLOv3", "4.YOLO4Y-Tiny", "5.YOLOv4 (M07)"]
        self.modelTypeComboBox.addItems(model_type)
        self.savePushButton.clicked.connect(self.saveAction)

        predict_type = ["0.N/A", "1.Electronic Fence", "2.Object Sequence", "3.Object Verify", "4.Work Area Sequence",
                        "5.Tracking Verify", ""]
        self.predictTypeComboBox.addItems(predict_type)

        width = 150
        self.enableLabel.setFixedWidth(width)
        self.enableSwitchButton.setFixedSize(QSize(40, 24))

        self.spaceLabel1.setFixedWidth(width)
        self.spaceLabel2.setFixedWidth(width)

        self.spaceLabel3.setFixedWidth(width)
        self.spaceLabel4.setFixedWidth(width)

        self.serverAddressLabel.setFixedWidth(width)
        self.serverAddressLineEdit.setFixedWidth(width)

        self.connectTimeoutLabel.setFixedWidth(width)
        self.connectTimeoutDoubleSpinBox.setFixedWidth(width)

        self.postTimeoutLabel.setFixedWidth(width)
        self.postTimeoutDoubleSpinBox.setFixedWidth(width)

        self.hostNameLabel.setFixedWidth(width)
        self.hostNameLineEdit.setFixedWidth(width)

        self.lineIDLabel.setFixedWidth(width)
        self.lineIDLineEdit.setFixedWidth(width)

        self.eqpIDLabel.setFixedWidth(width)
        self.eqpIDLineEdit.setFixedWidth(width)

        self.stationIDLabel.setFixedWidth(width)
        self.stationIDLineEdit.setFixedWidth(width)

        self.opIDLabel.setFixedWidth(width)
        self.opIDLineEdit.setFixedWidth(width)

        self.siteLabel.setFixedWidth(width)
        self.siteComboBox.setFixedWidth(width)

        self.processStageLabel.setFixedWidth(width)
        self.processStageLineEdit.setFixedWidth(width)

        self.projectIDLabel.setFixedWidth(width)
        self.projectIDLineEdit.setFixedWidth(width)

        self.projectNameLabel.setFixedWidth(width)
        self.projectNameLineEdit.setFixedWidth(width)

        self.imageFileSuffixLabel.setFixedWidth(width)
        self.imageFileSuffixLineEdit.setFixedWidth(width)

        self.modelNameLabel.setFixedWidth(width)
        self.modelNameLineEdit.setFixedWidth(width)

        self.modelVersionLabel.setFixedWidth(width)
        self.modelVersionLineEdit.setFixedWidth(width)

        self.modelIterationLabel.setFixedWidth(width)
        self.modelIterationLineEdit.setFixedWidth(width)

        self.modelLabelsLabel.setFixedWidth(width)
        self.modelLabelsLineEdit.setFixedWidth(width)

        self.modelTypeLabel.setFixedWidth(width)
        self.modelTypeComboBox.setFixedWidth(width)

        self.predictTypeLabel.setFixedWidth(width)
        self.predictTypeComboBox.setFixedWidth(width)

        enableLayout = QHBoxLayout(spacing=0)
        enableLayout.setContentsMargins(0, 0, 0, 0)
        enableLayout.addWidget(QLabel())
        enableLayout.addWidget(self.enableSwitchButton)

        self.enableWidget.setLayout(enableLayout)
        self.enableWidget.setFixedWidth(width)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.enableLabel)
        topLayout.addWidget(self.spaceLabel1)
        topLayout.addWidget(self.spaceLabel2)
        topLayout.addWidget(self.enableWidget)

        layout1 = QHBoxLayout()
        layout1.addWidget(self.serverAddressLabel)
        layout1.addWidget(self.serverAddressLineEdit)
        layout1.addWidget(self.hostNameLabel)
        layout1.addWidget(self.hostNameLineEdit)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.connectTimeoutLabel)
        layout2.addWidget(self.connectTimeoutDoubleSpinBox)
        layout2.addWidget(self.postTimeoutLabel)
        layout2.addWidget(self.postTimeoutDoubleSpinBox)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.projectIDLabel)
        layout3.addWidget(self.projectIDLineEdit)
        layout3.addWidget(self.projectNameLabel)
        layout3.addWidget(self.projectNameLineEdit)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.imageFileSuffixLabel)
        layout4.addWidget(self.imageFileSuffixLineEdit)
        layout4.addWidget(self.siteLabel)
        layout4.addWidget(self.siteComboBox)

        layout5 = QHBoxLayout()
        layout5.addWidget(self.lineIDLabel)
        layout5.addWidget(self.lineIDLineEdit)
        layout5.addWidget(self.eqpIDLabel)
        layout5.addWidget(self.eqpIDLineEdit)

        layout6 = QHBoxLayout()
        layout6.addWidget(self.stationIDLabel)
        layout6.addWidget(self.stationIDLineEdit)
        layout6.addWidget(self.opIDLabel)
        layout6.addWidget(self.opIDLineEdit)

        layout7 = QHBoxLayout()
        layout7.addWidget(self.processStageLabel)
        layout7.addWidget(self.processStageLineEdit)
        layout7.addWidget(self.modelNameLabel)
        layout7.addWidget(self.modelNameLineEdit)

        layout8 = QHBoxLayout()
        layout8.addWidget(self.modelVersionLabel)
        layout8.addWidget(self.modelVersionLineEdit)
        layout8.addWidget(self.modelIterationLabel)
        layout8.addWidget(self.modelIterationLineEdit)

        layout9 = QHBoxLayout()
        layout9.addWidget(self.modelLabelsLabel)
        layout9.addWidget(self.modelLabelsLineEdit)
        layout9.addWidget(self.modelTypeLabel)
        layout9.addWidget(self.modelTypeComboBox)

        layout10 = QHBoxLayout()
        layout10.addWidget(self.predictTypeLabel)
        layout10.addWidget(self.predictTypeComboBox)
        layout10.addWidget(self.spaceLabel3)
        layout10.addWidget(self.spaceLabel4)

        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(topLayout)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(layout6)
        layout.addLayout(layout7)
        layout.addLayout(layout8)
        layout.addLayout(layout9)
        layout.addLayout(layout10)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        enable = bool(int(root.find('dataupload').find('enable').text))
        self.enableSwitchButton.setChecked(enable)

        server_address = root.find('dataupload').find('server_address').text
        self.serverAddressLineEdit.setText(server_address)

        host_name = root.find('dataupload').find('host_name').text
        self.hostNameLineEdit.setText(host_name)

        conn_timeout = float(root.find('dataupload').find('conn_timeout').text)
        self.connectTimeoutDoubleSpinBox.setValue(conn_timeout)

        post_timeout = float(root.find('dataupload').find('post_timeout').text)
        self.postTimeoutDoubleSpinBox.setValue(post_timeout)

        project_id = root.find('dataupload').find('project_id').text
        self.projectIDLineEdit.setText(project_id)

        project_name = root.find('dataupload').find('project_name').text
        self.projectNameLineEdit.setText(project_name)

        image_file_suffix = root.find('dataupload').find('image_file_suffix').text
        self.imageFileSuffixLineEdit.setText(image_file_suffix)

        site = root.find('dataupload').find('site').text
        self.siteComboBox.setCurrentText(site)

        line_id = root.find('dataupload').find('line_id').text
        self.lineIDLineEdit.setText(line_id)

        eqp_id = root.find('dataupload').find('eqp_id').text
        self.eqpIDLineEdit.setText(eqp_id)

        station_id = root.find('dataupload').find('station_id').text
        self.stationIDLineEdit.setText(station_id)

        op_id = root.find('dataupload').find('op_id').text
        self.opIDLineEdit.setText(op_id)

        process_stage = root.find('dataupload').find('process_stage').text
        self.processStageLineEdit.setText(process_stage)

        model_name = root.find('dataupload').find('model_name').text
        self.modelNameLineEdit.setText(model_name)

        model_version = root.find('dataupload').find('model_version').text
        self.modelVersionLineEdit.setText(model_version)

        model_iteration = root.find('dataupload').find('model_iteration').text
        self.modelIterationLineEdit.setText(model_iteration)

        model_labels = root.find('dataupload').find('model_labels').text
        self.modelLabelsLineEdit.setText(model_labels)

        model_type = root.find('dataupload').find('model_type').text
        self.modelTypeComboBox.setCurrentText(model_type)

        predict_type = root.find('dataupload').find('predict_type').text
        self.predictTypeComboBox.setCurrentText(predict_type)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: ignore this
        :return: None
        """
        self.load_config()

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        tree = ET.parse(self.config_path)
        root = tree.getroot()

        enable = self.enableSwitchButton.checked
        root.find('dataupload').find('enable').text = "1" if enable else "0"

        server_address = self.serverAddressLineEdit.text()
        root.find('dataupload').find('server_address').text = server_address

        host_name = self.hostNameLineEdit.text()
        root.find('dataupload').find('host_name').text = host_name

        conn_timeout = self.connectTimeoutDoubleSpinBox.value()
        root.find('dataupload').find('conn_timeout').text = str(conn_timeout)

        post_timeout = self.postTimeoutDoubleSpinBox.value()
        root.find('dataupload').find('post_timeout').text = str(post_timeout)

        project_id = self.projectIDLineEdit.text()
        root.find('dataupload').find('project_id').text = project_id

        project_name = self.projectNameLineEdit.text()
        root.find('dataupload').find('project_name').text = project_name

        image_file_suffix = self.imageFileSuffixLineEdit.text()
        root.find('dataupload').find('image_file_suffix').text = image_file_suffix

        site = self.siteComboBox.currentText()
        root.find('dataupload').find('site').text = site

        line_id = self.lineIDLineEdit.text()
        root.find('dataupload').find('line_id').text = line_id

        eqp_id = self.eqpIDLineEdit.text()
        root.find('dataupload').find('eqp_id').text = eqp_id

        station_id = self.stationIDLineEdit.text()
        root.find('dataupload').find('station_id').text = station_id

        op_id = self.opIDLineEdit.text()
        root.find('dataupload').find('op_id').text = op_id

        process_stage = self.processStageLineEdit.text()
        root.find('dataupload').find('process_stage').text = process_stage

        model_name = self.modelNameLineEdit.text()
        root.find('dataupload').find('model_name').text = model_name

        model_version = self.modelVersionLineEdit.text()
        root.find('dataupload').find('model_version').text = model_version

        model_iteration = self.modelIterationLineEdit.text()
        root.find('dataupload').find('model_iteration').text = model_iteration

        model_labels = self.modelLabelsLineEdit.text()
        root.find('dataupload').find('model_labels').text = model_labels

        model_type = self.modelTypeComboBox.currentText()
        root.find('dataupload').find('model_type').text = model_type.split('.')[0]

        predict_type = self.predictTypeComboBox.currentText()
        root.find('dataupload').find('predict_type').text = predict_type.split('.')[0]

        tree.write(self.config_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DataUploadSettingsWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
