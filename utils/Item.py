#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import pyqtSignal


class Item(object):
    __slots__ = 'category', 'confirm_frames', 'thresh', 'pin', 'time', 'mode', 'label_list'
    GPIO_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.label_list = []

    def allow_alarm(self, label, conf):
        """
        Allow alarm?
        :param label: label
        :param conf: bool
        :return:
        """
        assert self.category is not None or self.category != ''
        if conf < self.thresh:  # 置信度没达到
            return False
        if len(self.label_list) == self.confirm_frames:  # 达到确认帧数
            self.label_list.clear()  # 清空label_list
            return True  # 直接返回
        if label == self.category:
            self.label_list.append(label)

    def reset(self):
        """
        Reset.
        :return: None
        """
        self.label_list.clear()
