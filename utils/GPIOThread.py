#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import sys
import time
import threading
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

        self._lock = threading.RLock()

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

    """This function is abandoned."""
    def __custom_output(self, item):
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

    def output(self, item):
        self._lock.acquire()  # acquire the lock
        pre = time.time()
        try:
            print(str(self.index) + " " + "output mode: " + str(item.get_mode()) + " " + "output pin: " +
                  str(item.get_pin()) + " " + "output time: " + str(item.get_time()))
            if item.get_mode() == 1:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                GPIO.output(item.get_pin(), GPIO.HIGH)
            else:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                GPIO.output(item.get_pin(), GPIO.LOW)
            # replace the time.sleep()
            while True:
                if time.time() - pre > item.get_time():
                    break
            if item.get_mode() == 1:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                GPIO.output(item.get_pin(), GPIO.LOW)
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                self.index += 1
            else:
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                GPIO.output(item.get_pin(), GPIO.HIGH)
                print(str(self.index) + " " + str(datetime.datetime.now()) + " " + str(GPIO.input(item.get_pin())))
                self.index += 1
            print()
        finally:
            pass
            self._lock.release()  # release the lock

    def custom_output(self, item):
        # prevent thread blocking the program
        threading.Thread(target=self.output, args=(item, )).start()

    def run(self):
        pass

    def __del__(self):
        GPIO.cleanup()
