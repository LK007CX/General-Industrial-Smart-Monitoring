#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QTimer

sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO


class GPIOThread(QThread):
    flag_Signal = pyqtSignal()

    def __init__(self, args):
        super(GPIOThread, self).__init__()
        self.args = args
        self.item_list = args.item_list
        self.init_GPIO()
        self._mutex = QMutex()

        self.index = 0

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

            if item.get_mode() == 1:
                print("High pulse output: " + str(item.get_pin()) + ".")
                GPIO.setup(item.get_pin(), GPIO.OUT, initial=GPIO.LOW)
            else:
                print("Low pulse output: " + str(item.get_pin()) + ".")
                GPIO.setup(item.get_pin(), GPIO.OUT, initial=GPIO.HIGH)

    def callback(self, input_pin):
        """
        GPIO callback function.
        :param input_pin: input pin
        :return: None
        """
        self.flag_Signal.emit()

    def custom_output(self, item):
        self._mutex.lock()
        if item.get_mode() == 1:
            # print(str(self.index) + " " + str(item.time))
            # print(str(self.index) + " " + str(datetime.datetime.now()) + " high")
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))
            GPIO.output(item.get_pin(), GPIO.HIGH)
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))

            time.sleep(item.get_time())
            GPIO.output(item.get_pin(), GPIO.LOW)
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))
            # print(str(self.index) + " " + str(datetime.datetime.now()) + " high end\n")
            # self.index += 1
        else:
            # print(str(self.index) + " " + str(item.time))
            # print(str(self.index) + " " +str(datetime.datetime().now) + " low")
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))
            GPIO.output(item.get_pin(), GPIO.LOW)
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))
            time.sleep(item.get_time())
            GPIO.output(item.get_pin(), GPIO.HIGH)
            # print(str(self.index) + " " +str(GPIO.input(item.pin)))
            # print(str(self.index) + " " +str(datetime.datetime().now) + " low end\n")
            # self.index += 1
        self._mutex.unlock()
    #
    # QTimer.singleShot(400, lambda: (splashScreen.progressBar.setValue(100),
    #                                 splashScreen.progressBarStatusLabel.setText("(5/5)加载完毕"),
    #                                 splashScreen.finish(app.w),
    #                                 app.setStyleSheet(mainWindowStyle),
    #                                 app.w.show()))

    # def custom_output(self, item):
    #     self._mutex.lock()
    #     if item.get_mode() == 1:
    #         print(str(self.index) + " " + str(item.get_time()))
    #         print(str(self.index) + " " + str(datetime.datetime.now()) + " high")
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #         GPIO.output(item.get_pin(), GPIO.HIGH)
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #
    #         QTimer.singleShot(400, lambda: (GPIO.output(item.get_pin(), GPIO.LOW)))
    #
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #         print(str(self.index) + " " + str(datetime.datetime.now()) + " high end\n")
    #         self.index += 1
    #     else:
    #         print(str(self.index) + " " + str(item.get_time()))
    #         print(str(self.index) + " " +str(datetime.datetime().now) + " low")
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #         GPIO.output(item.get_pin(), GPIO.LOW)
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #         time.sleep(item.get_time())
    #         QTimer.singleShot(400, lambda: (GPIO.output(item.get_pin(), GPIO.HIGH)))
    #         print(str(self.index) + " " +str(GPIO.input(item.get_pin())))
    #         print(str(self.index) + " " +str(datetime.datetime().now) + " low end\n")
    #         self.index += 1
    #     self._mutex.unlock()

    def run(self):
        pass

    def __del__(self):
        GPIO.cleanup()
