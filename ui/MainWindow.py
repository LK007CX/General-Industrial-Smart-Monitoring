#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QWidget, QDesktopWidget, QMessageBox, QApplication, QStatusBar

from ui.AlarmWidget import AlarmWidget
from ui.ErrorWidget import ErrorWidget
from ui.HeaderWidget import HeaderWidget
from ui.HistoryListView import HistoryListView
from ui.VideoWidget import VideoWidget
from utils.ArgsHelper import ArgsHelper
from utils.DataUploadThread import EdgeAgentWorker
from utils.DeleteFileThread import DeleteFileThread
from utils.DetectTensorRT import DetectTensorRT
from utils.GPIOThread import GPIOThread
from utils.Item import Item

canRestart = True


def restart(twice):
    """
    Restart the PyQt Application.
    :param twice:
    :return: None
    """
    os.execl(sys.executable, sys.executable, *[sys.argv[0], "-t", twice])


class MainWindow(QMainWindow):

    def __init__(self, config_path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.headerWidget = HeaderWidget(config_path, "异常带片智能监控")
        self.videoWidget = VideoWidget()
        self.errorWidget = ErrorWidget()
        self.historyWidget = HistoryListView()
        self.alarmWidget = AlarmWidget(config_path)
        self.statusBar = QStatusBar()

        self.config_path = config_path
        self.args = self.load_config()

        self.thread = None
        self.gpio_thread = None
        self.delete_file_thread = None
        self.edge_agent_worker = None

        self.init_thread()
        self.init_ui()

    def init_ui(self):
        self.statusBar.addPermanentWidget(QLabel("MS00A0 自动化效率推进部"))

        """signal"""
        self.headerWidget.restartPushButton.clicked.connect(self.restartApplication)

        """leftBottomLayout"""
        leftBottomLayout = QHBoxLayout(spacing=0)
        leftBottomLayout.setContentsMargins(0, 0, 0, 0)
        leftBottomLayout.addWidget(self.errorWidget)
        leftBottomLayout.addWidget(self.alarmWidget)

        """leftLayout"""
        leftLayout = QVBoxLayout(spacing=0)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.addWidget(self.videoWidget)
        leftLayout.addLayout(leftBottomLayout)

        """rightLayout"""
        rightLayout = QHBoxLayout(spacing=0)
        rightLayout.setContentsMargins(0, 0, 0, 0)
        rightLayout.addWidget(self.historyWidget)

        """bottomLayout"""
        bottomLayout = QHBoxLayout(spacing=0)
        bottomLayout.setContentsMargins(0, 0, 0, 0)
        bottomLayout.addLayout(leftLayout)
        bottomLayout.addLayout(rightLayout)

        """layout"""
        layout = QVBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.headerWidget, 0, Qt.AlignTop)
        layout.addLayout(bottomLayout)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        """status bar"""
        self.setStatusBar(self.statusBar)

        """self..."""
        self.resize(QSize(1280, 720))
        self.setWindowTitle("GISM2020 MainUI")
        self.setWindowIcon(QIcon(QPixmap('icon/logo.png')))
        self.setObjectName("MainWindow")

        self.center()

    def resizeEvent(self, QResizeEvent):
        """
        Keep video widget at a 16:9 ratio.
        :param QResizeEvent:
        :return: None
        """
        base = self.width() // 25
        self.videoWidget.setFixedSize(QSize(16 * base, 9 * base))

    def center(self):
        """
        Make the window show in the middle of the screen.
        :return: None
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def load_config(self):
        """
        Load application configuration.
        :return: parameter
        """
        args = None
        try:
            tree = ET.parse(self.config_path)
            root = tree.getroot()

            camera_mode = root.find('camera').find('mode').text
            cameraID = int(root.find('camera').find('camera_id').text)
            ip = root.find('camera').find('ip').text
            width = int(root.find('camera').find('width').text)
            height = int(root.find('camera').find('height').text)
            detecttime = int(root.find('input').find('detecttime').text)
            input_pin = int(root.find('input').find('inputpin').text)
            trigger_mode = root.find('input').find('triggermode').text
            detect_mode = root.find('input').find('mode').text
            time_delay = int(root.find('input').find('timedelay').text)

            modelpath = root.find('model').find('modelpath').text
            labelsfile = root.find('model').find('labelsfile').text
            thresh = float(root.find('model').find('thresh').text)
            size = root.find('model').find('size').text

            category_num = int(root.find('model').find('category_num').text)

            minimum_storage_interval = int(root.find('image').find('minimumstorageinterval').text)

            maximum_storage_quantity = int(root.find('image').find('maximumstoragequantity').text)

            enable_save_image = bool(int(root.find('image').find('enable').text))

            enable_remote_cv = bool(int(root.find('remotecv').find('enable').text))

            enable_data_upload = bool(int(root.find('dataupload').find('enable').text))

            server_address = root.find('dataupload').find('server_address').text
            host_name = root.find('dataupload').find('host_name').text
            conn_timeout = float(root.find('dataupload').find('conn_timeout').text)
            post_timeout = float(root.find('dataupload').find('post_timeout').text)
            project_id = root.find('dataupload').find('project_id').text
            project_name = root.find('dataupload').find('project_name').text
            image_file_suffix = root.find('dataupload').find('image_file_suffix').text
            site = root.find('dataupload').find('site').text
            line_id = root.find('dataupload').find('line_id').text
            eqp_id = root.find('dataupload').find('eqp_id').text
            station_id = root.find('dataupload').find('station_id').text
            op_id = root.find('dataupload').find('op_id').text
            process_stage = root.find('dataupload').find('process_stage').text
            model_name = root.find('dataupload').find('model_name').text
            model_version = root.find('dataupload').find('model_version').text
            model_iteration = root.find('dataupload').find('model_iteration').text
            model_labels = root.find('dataupload').find('model_labels').text
            model_type = root.find('dataupload').find('model_type').text.split('.')[0]
            predict_type = root.find('dataupload').find('predict_type').text.split('.')[0]

            application_title = root.find('app').find('application_title').text
            self.headerWidget.titleLabel.setText(application_title)

            item_list = []
            for action in root.find('detect_items').findall('item'):
                category = action.find('category').text
                confirm_frames = int(action.find('frames').text)
                thresh = float(action.find('thresh').text)
                pin = int(action.find('pin').text)
                time = float(action.find('time').text)
                mode = int(action.find('mode').text)

                item = Item(category=category, confirm_frames=confirm_frames, thresh=thresh, pin=pin, time=time,
                            mode=mode)
                item_list.append(item)

            if camera_mode == 'USB':
                args = ArgsHelper(image=None,
                                  video=None,
                                  video_looping=False,
                                  rtsp=None,
                                  rtsp_latency=200,
                                  usb=cameraID,
                                  onboard=None,
                                  copy_frame=False,
                                  do_resize=False,
                                  width=width,
                                  height=height,
                                  category_num=category_num,
                                  model=modelpath,
                                  detect_time=detecttime,
                                  input_pin=input_pin,
                                  trigger_mode=trigger_mode,
                                  time_delay=time_delay,
                                  detect_mode=detect_mode,
                                  yolo_dim=size,
                                  labelsfile=labelsfile,
                                  thresh=thresh,
                                  item_list=item_list,
                                  minimum_storage_interval=minimum_storage_interval,
                                  maximum_storage_quantity=maximum_storage_quantity,
                                  enable_save_image=enable_save_image,
                                  enable_remote_cv=enable_remote_cv,
                                  enable_data_upload=enable_data_upload,
                                  server_address=server_address,
                                  host_name=host_name,
                                  conn_timeout=conn_timeout,
                                  post_timeout=post_timeout,
                                  project_id=project_id,
                                  project_name=project_name,
                                  image_file_suffix=image_file_suffix,
                                  site=site,
                                  line_id=line_id,
                                  eqp_id=eqp_id,
                                  station_id=station_id,
                                  op_id=op_id,
                                  process_stage=process_stage,
                                  model_name=model_name,
                                  model_version=model_version,
                                  model_iteration=model_iteration,
                                  model_labels=model_labels,
                                  model_type=model_type,
                                  predict_type=predict_type
                                  )
            elif camera_mode == 'RTSP':
                args = ArgsHelper(image=None,
                                  video=None,
                                  video_looping=False,
                                  rtsp=ip,
                                  rtsp_latency=200,
                                  usb=None,
                                  onboard=None,
                                  copy_frame=False,
                                  do_resize=False,
                                  width=width,
                                  height=height,
                                  category_num=category_num,
                                  model=modelpath,
                                  detect_time=detecttime,
                                  input_pin=input_pin,
                                  trigger_mode=trigger_mode,
                                  time_delay=time_delay,
                                  detect_mode=detect_mode,
                                  yolo_dim=size,
                                  labelsfile=labelsfile,
                                  thresh=thresh,
                                  item_list=item_list,
                                  minimum_storage_interval=minimum_storage_interval,
                                  maximum_storage_quantity=maximum_storage_quantity,
                                  enable_save_image=enable_save_image,
                                  enable_remote_cv=enable_remote_cv,
                                  enable_data_upload=enable_data_upload,
                                  server_address=server_address,
                                  host_name=host_name,
                                  conn_timeout=conn_timeout,
                                  post_timeout=post_timeout,
                                  project_id=project_id,
                                  project_name=project_name,
                                  image_file_suffix=image_file_suffix,
                                  site=site,
                                  line_id=line_id,
                                  eqp_id=eqp_id,
                                  station_id=station_id,
                                  op_id=op_id,
                                  process_stage=process_stage,
                                  model_name=model_name,
                                  model_version=model_version,
                                  model_iteration=model_iteration,
                                  model_labels=model_labels,
                                  model_type=model_type,
                                  predict_type=predict_type
                                  )
        except Exception as e:
            print(e)
        return args

    def init_thread(self):
        """
        Initialize thread.
        Binding signal and slot function.
        :return: None
        """
        try:
            self.thread = DetectTensorRT(self.args)
            self.gpio_thread = GPIOThread(self.args)
            pwd = os.getcwd() + "/image"
            max_save_num = self.args.maximum_storage_quantity
            self.delete_file_thread = DeleteFileThread(pwd, max_save_num)

            self.thread.image_Signal.connect(self.videoWidget.handleDisplay)
            self.thread.history_Signal.connect(self.historyWidget.addItem)
            self.thread.num_Signal.connect(self.alarmWidget.alarmTableWidget.changeResult)
            self.thread.info_Signal.connect(self.showMessage)
            self.thread.gpio_Signal.connect(self.gpio_thread.custom_output)
            self.gpio_thread.flag_Signal.connect(self.thread.callback)

            self.edge_agent_worker = EdgeAgentWorker(self.args)
            self.thread.upload_Signal.connect(self.edge_agent_worker.send)
            self.edge_agent_worker.remote_server_status_signal.connect(self.headerWidget.changeRemoteServerStatus)
            self.thread.start()
            self.delete_file_thread.start()
        except Exception as e:
            self.thread.cam.release()
            self.thread.quit()
            self.gpio_thread.quit()
            self.delete_file_thread.quit()
            self.edge_agent_worker.quit()
            print(e)

    def showMessage(self, string):
        """
        Show message.
        :param string: string
        :return: None
        """
        self.statusBar.showMessage(string)

    def closeEvent(self, event):
        """
        Close event.
        :param event: event
        :return: None
        """
        global canRestart
        canRestart = False
        try:
            self.thread.cam.release()
            self.thread.quit()
            self.gpio_thread.quit()
            self.delete_file_thread.quit()
            self.edge_agent_worker.quit()

        except Exception as e:
            print(e)

    def restartApplication(self):
        """
        Restart application.
        :return: None
        """
        result = QMessageBox.question(self, "提示", "是否重新启动程式?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            try:
                self.thread.cam.release()
                self.thread.quit()
            except Exception as e:
                print(e)
            time.sleep(1)
            self.close()
            global canRestart
            canRestart = True
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow("../appconfig/appconfig.xml")
    win.show()
    sys.exit(app.exec_())
