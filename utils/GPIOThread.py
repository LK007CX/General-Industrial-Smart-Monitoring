#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtCore import QThread, pyqtSignal

sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO


class GPIOThread(QThread):
    flag_Signal = pyqtSignal()

    is_alive = False

    def __init__(self, args):
        super(GPIOThread, self).__init__()
        self.args = args
        self.item_list = args.item_list
        self.init_GPIO()


    def init_GPIO(self):
        """
        Initialize GPIO.
        :return: None
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.args.input_pin, GPIO.IN)
        GPIO_mode = GPIO.RISING if self.args.trigger_mode == 'high pulse' else GPIO.FALLING
        GPIO.add_event_detect(self.args.input_pin, GPIO_mode, callback=self.callback, bouncetime=self.args.time_delay)

        for item in self.item_list:

            if item.mode == 1:
                print("高脉冲触发" + str(item.pin))
                GPIO.setup(item.pin, GPIO.OUT, initial=GPIO.LOW)
            else:
                print("低脉冲触发" + str(item.pin))
                GPIO.setup(item.pin, GPIO.OUT, initial=GPIO.HIGH)

    def callback(self, input_pin):
        """
        GPIO callback function.
        :param input_pin: input pin
        :return: None
        """
        self.flag_Signal.emit()

    def custom_output(self, item):
        if GPIOThread.is_alive:
            print("正在输出，方法返回")
            return
        GPIOThread.is_alive = True
        if item.mode == 1:
            print(GPIO.input(item.pin))
            GPIO.output(item.pin, GPIO.HIGH)
            print(GPIO.input(item.pin))
            self.sleep(item.time)
            GPIO.output(item.pin, GPIO.LOW)
            print(GPIO.input(item.pin))
        else:
            print(GPIO.input(item.pin))
            GPIO.output(item.pin, GPIO.LOW)
            print(GPIO.input(item.pin))
            self.sleep(item.time)
            GPIO.output(item.pin, GPIO.HIGH)
            print(GPIO.input(item.pin))
        GPIOThread.is_alive = False

    def run(self):
        pass

    def __del__(self):
        GPIO.cleanup()
