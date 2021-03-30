#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import pyqtSignal


class Item(object):
    __slots__ = '_category', '_confirm_frames', '_thresh', '_pin', '_time', '_mode', '_label_list'
    GPIO_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            self._label_list = []

    def get_category(self):
        return self._category

    def get_mode(self):
        return self._mode

    def get_pin(self):
        return self._pin

    def get_time(self):
        return self._time

    def reset(self):
        """
        Reset.
        :return: None
        """
        self._label_list.clear()

    def allow_alarm(self, label, conf):
        """
        Allow alarm ?
        :param label: label
        :param conf: bool
        :return:
        """
        assert self._category is not None or self._category != ''

        if conf < self._thresh:  # 置信度没达到
            return False

        if len(self._label_list) == self._confirm_frames:  # 达到确认帧数
            self._label_list.clear()  # 清空label_list
            return True  # 直接返回

        if label == self._category:
            self._label_list.append(label)
