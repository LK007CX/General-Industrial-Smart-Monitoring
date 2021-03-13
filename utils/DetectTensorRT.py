#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgitb
import copy
import datetime
import os
import random
import sys
import time

import cv2
import gi
import numpy as np
import pycuda.autoinit  # This is needed for initializing CUDA driver
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# from ui.MainWindow import restart
from utils.ArgsHelper import ArgsHelper
from utils.Item import Item
from utils.ModelOutputItem import ModelOutputItem
from utils.camera import Camera
from utils.custom_classes import get_cls_dict
from utils.display import show_fps
from utils.edgeAgent import edgeeye_ld_prediction, inference_box_info, cv2_img_info
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer

sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO

from optparse import OptionParser

_width = '1280'
_height = '720'
global_image = np.ndarray(())


class SensorFactory(GstRtspServer.RTSPMediaFactory):
    # global camera
    def __init__(self, **properties):
        super(SensorFactory, self).__init__(**properties)
        self.number_frames = 0
        self.fps = 30
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=' + _width + ',height=' + _height + ',framerate={}/1 ' \
                                                                                                    '! videoconvert ! video/x-raw,format=I420 ' \
                                                                                                    '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                                                                                                    '! rtph264pay config-interval=1 name=pay0 pt=96'.format(
            self.fps)

    def on_need_data(self, src, lenght):
        global global_image
        data = global_image.tostring()
        buf = Gst.Buffer.new_allocate(None, len(data), None)
        buf.fill(0, data)
        buf.duration = self.duration
        timestamp = self.number_frames * self.duration
        buf.pts = buf.dts = int(timestamp)
        buf.offset = timestamp
        self.number_frames += 1
        retval = src.emit('push-buffer', buf)

        if retval != Gst.FlowReturn.OK:
            print(retval)

    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.set_address = '0.0.0.0'
        self.set_service = '8554'
        self.factory = SensorFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/test", self.factory)
        self.attach(None)


class DetectTensorRT(QThread):
    image_Signal = pyqtSignal(np.ndarray)
    history_Signal = pyqtSignal(np.ndarray, str, str, str)
    num_Signal = pyqtSignal(str)
    info_Signal = pyqtSignal(str)
    gpio_Signal = pyqtSignal(Item)

    upload_Signal = pyqtSignal(edgeeye_ld_prediction)

    def __init__(self, args, parent=None):
        super(DetectTensorRT, self).__init__(parent)
        self.args = args
        self.cam = None
        self.trt_yolo = None
        self.conf_th = args.thresh
        self.vis = None

        self.item_list = args.item_list
        self.item_dict = {item.category: item for item in self.item_list}

        self.cls_dict = None
        self.gpio_flag = False

        self.detect_start_time = None

        self.save_start_time = time.time()

        self.enable_save_image = args.enable_save_image
        self.enable_remote_cv = args.enable_remote_cv
        self.enable_data_upload = args.enable_data_upload

        # data upload
        self.edgeeye_ld_prediction = None
        self.inference_box_info = None
        self.load_edge_eye()
        self.inference_info_array = []
        self.img_arr = []

    def setStatus(self, boolean):
        """
        Set GPIO status.
        :param boolean: status
        :return: None
        """
        self.gpio_flag = boolean

    def callback(self):
        """
        GPIO callback.
        :return: None
        """
        if self.args.detect_mode == "continuous detect":
            return
        if not self.gpio_flag:
            self.gpio_flag = True
            self.detect_start_time = time.time()

    def load_edge_eye(self):
        if not self.enable_data_upload:
            return
        self.edgeeye_ld_prediction = edgeeye_ld_prediction('',
                                                           '',
                                                           '',
                                                           self.args.line_id,
                                                           self.args.eqp_id,
                                                           self.args.station_id,
                                                           self.args.op_id,
                                                           self.args.host_name,
                                                           self.args.site,
                                                           self.args.process_stage,
                                                           '',
                                                           self.args.image_file_suffix,
                                                           self.args.project_id,
                                                           self.args.project_name,
                                                           self.args.model_name,
                                                           self.args.model_version,
                                                           self.args.model_iteration,
                                                           self.args.model_labels,
                                                           self.args.model_type,
                                                           self.args.predict_type,
                                                           '',
                                                           '',
                                                           '',
                                                           '',
                                                           '',
                                                           )
        self.inference_box_info = inference_box_info('',
                                                     '',
                                                     '',
                                                     '',
                                                     '',
                                                     '',
                                                     '',
                                                     '', )

    def generate_info(self, current_time, label, box, cls, history_image, img):
        """
        Generate EdgeEye information.
        :param current_time:
        :param label:
        :param box:
        :param cls:
        :param history_image:
        :param img:
        :return: None
        """
        image_name = current_time + "_" + str(random.randint(1000, 9999)) + '.jpg'
        self.inference_box_info = self.inference_box_info._replace(image_name=image_name)
        self.inference_box_info = self.inference_box_info._replace(box_seq="0")
        self.inference_box_info = self.inference_box_info._replace(box_label=label)
        self.inference_box_info = self.inference_box_info._replace(box_x_min=str(box[0]))
        self.inference_box_info = self.inference_box_info._replace(box_y_min=str(box[1]))
        self.inference_box_info = self.inference_box_info._replace(box_x_max=str(box[2]))
        self.inference_box_info = self.inference_box_info._replace(box_y_max=str(box[3]))
        self.inference_box_info = self.inference_box_info._replace(
            box_confidence=str(round(cls, 2)))
        self.inference_info_array.append(copy.deepcopy(self.inference_box_info))
        self.edgeeye_ld_prediction = self.edgeeye_ld_prediction._replace(
            inference_info_array=self.inference_info_array)
        self.edgeeye_ld_prediction = self.edgeeye_ld_prediction._replace(
            img_array=[cv2_img_info(image_name, '.jpg', history_image)])
        self.edgeeye_ld_prediction = self.edgeeye_ld_prediction._replace(
            img_raw_array=[cv2_img_info(image_name, '.jpg', img)])
        self.upload_Signal.emit(self.edgeeye_ld_prediction)

    def output(self, history_image, label, current_time, box, conf):
        """
        Model output.
        :param history_image:
        :param label:
        :param current_time:
        :param box:
        :param conf:
        :return: None
        """
        self.history_Signal.emit(history_image, label, current_time, str(box))
        self.num_Signal.emit(label)
        self.info_Signal.emit(str(box) + '\t' + str(conf) + '\t' + str(label))
        if self.enable_save_image and time.time() - self.save_start_time > self.args.minimum_storage_interval:
            cv2.imwrite('./image/' + current_time + '.jpg', history_image)
            self.save_start_time = time.time()  # update last-save-image time
        self.gpio_Signal.emit(self.item_dict[label])

    def load_model(self):
        if self.args.category_num <= 0:
            raise SystemExit('ERROR: bad category_num (%d)!' % self.args.category_num)
        if not os.path.isfile(self.args.model):
            raise SystemExit('ERROR: file (model/%s.trt) not found!' % self.args.model)
        self.cam = Camera(self.args)
        if not self.cam.isOpened():
            """program restart section"""
            parser = OptionParser(usage="usage:%prog [optinos] filepath")
            parser.add_option("-t", "--twice", type="int",
                              dest="twice", default=1, help="运行次数")
            options, _ = parser.parse_args()
            cgitb.enable(1, None, 5, '')

            restart(str(options.twice + 1))
            # raise SystemExit('ERROR: failed to open camera!')

        self.cls_dict = get_cls_dict(self.args.labelsfile)
        yolo_dim = self.args.yolo_dim.split('*')[-1]
        if 'x' in yolo_dim:
            dim_split = yolo_dim.split('x')
            if len(dim_split) != 2:
                raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
            w, h = int(dim_split[0]), int(dim_split[1])
        else:
            h = w = int(yolo_dim)
        if h % 32 != 0 or w % 32 != 0:
            raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
        self.trt_yolo = TrtYOLO(self.args.model, (h, w), self.args.category_num, cuda_ctx=pycuda.autoinit.context)
        self.vis = BBoxVisualization(self.cls_dict)

    def loop_and_detect(self):
        detect_labels = [item.category for item in self.item_list]  # 所有需要检测的标签
        fps = 0.0
        tic = time.time()
        while True:
            img = self.cam.read()
            if img is None:
                break
            # if img is None:
            #     self.cam = None
            #     self.cam = Camera(self.args)
            #     if not self.cam.isOpened():
            #         print('ERROR: failed to open camera!')
            boxes, confs, clss = self.trt_yolo.detect(img, self.conf_th)  # 模型输出结果

            # 过滤标签
            if len(boxes) > 0:
                current_labels = [self.cls_dict[i] for i in clss]  # 当前所有标签，str
                index = [i for i in range(len(current_labels)) if current_labels[i] in detect_labels]
                boxes = [list(boxes[i]) for i in index]
                confs = [confs[i] for i in index]
                clss = [clss[i] for i in index]

            # 转换为ModelOutputItem
            model_output_list = [
                ModelOutputItem(box=boxes[i], confidence=confs[i], cls=clss[i], cls_dict=self.cls_dict)
                for i in range(len(boxes))]

            # 在此假设检测标签不重复，模型输出标签可以重复
            for modelOutputItem in model_output_list:
                label = modelOutputItem.label
                box = modelOutputItem.box
                conf = modelOutputItem.confidence
                cls = modelOutputItem.cls
                if label in self.item_dict.keys():  # 检测出来的标签
                    # 持续检测模式
                    if self.args.detect_mode == "continuous detect":
                        # 在此假设检测标签不重复（事实上也是如此），模型输出标签可以重复
                        if self.item_dict[label].allow_alarm(label, conf):
                            history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                            if self.enable_data_upload:
                                self.generate_info(current_time, label, box, cls, history_image, img)  # 数据上报
                            self.output(history_image, label, current_time, box, conf)  # 输出
                    # GPIO触发模式
                    else:
                        if self.gpio_flag:
                            # 在此假设检测标签不重复（事实上也是如此），模型输出标签可以重复
                            if self.item_dict[label].allow_alarm(label, conf):
                                history_image = self.vis.draw_bboxes(img, [box], [conf], [cls])
                                current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                                if self.enable_data_upload:
                                    self.generate_info(current_time, label, box, cls, history_image, img)  # 数据上报
                                self.output(history_image, label, current_time, box, conf)  # 输出
                            if time.time() - self.detect_start_time > self.args.detect_time:
                                self.gpio_flag = False
                        else:
                            for item in self.item_list:
                                item.reset()

            img = self.vis.draw_bboxes(img, boxes, confs, clss)
            img = show_fps(img, fps)
            self.image_Signal.emit(img)
            if self.enable_remote_cv:
                global global_image
                global_image = copy.deepcopy(img)
            toc = time.time()
            curr_fps = 1.0 / (toc - tic)
            # 计算fps数的指数衰减平均值
            fps = curr_fps if fps == 0.0 else (fps * 0.95 + curr_fps * 0.05)
            tic = toc
            # time.sleep(0.005)

    def run(self):
        try:
            self.load_model()
            self.loop_and_detect()
        finally:
            self.cam.release()
            GPIO.cleanup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    args = ArgsHelper(image=None, video=None, video_looping=False, rtsp=None, rtsp_latency=200, usb=1, onboard=None,
                      copy_frame=False, do_resize=False, width=640, height=480, category_num=80,
                      model='yolov4-tiny-416')
    thread1 = DetectTensorRT(args)
    thread1.start()
    sys.exit(app.exec_())
