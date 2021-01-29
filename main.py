#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import cgitb
import sys
from optparse import OptionParser

import gi
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MainWindow, restart
from ui.SplashScreen import SplashScreen
from utils.CommonHelper import CommonHelper
from utils.DetectTensorRT import GstServer

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst

if __name__ == "__main__":
    """program restart section"""
    parser = OptionParser(usage="usage:%prog [optinos] filepath")
    parser.add_option("-t", "--twice", type="int",
                      dest="twice", default=1, help="运行次数")
    options, _ = parser.parse_args()
    cgitb.enable(1, None, 5, '')

    """GStreamer remote video push"""
    GObject.threads_init()
    Gst.init(None)
    server = GstServer()

    """PyQt Application"""
    app = QApplication(sys.argv)
    splashScreenStyle = CommonHelper.readQss("./qss/splashScreen.qss")
    mainWindowStyle = CommonHelper.readQss("./qss/mainWindow.qss")
    splashScreen = SplashScreen()
    splashScreen.setStyleSheet(splashScreenStyle)
    splashScreen.show()


    def load_config():
        """
        Load application configuration.

        This is just a simulation.
        This part will be implemented in the future.

        :return: None
        """
        pass
        QTimer.singleShot(100, lambda: (splashScreen.progressBar.setValue(10),
                                        splashScreen.progressBarStatusLabel.setText("(2/5)正在读取配置 ...")))


    def load_model():
        """
        Load TensorRT model.

        This is just a simulation.
        This part will be implemented in the future.

        :return: None
        """
        pass
        QTimer.singleShot(200, lambda: (splashScreen.progressBar.setValue(30),
                                        splashScreen.progressBarStatusLabel.setText("(3/5)正在加载模型 ...")))


    def load_camera():
        """
        Load camera.

        This is just a simulation.
        This part will be implemented in the future.

        :return: None
        """
        pass
        QTimer.singleShot(300, lambda: (splashScreen.progressBar.setValue(80),
                                        splashScreen.progressBarStatusLabel.setText("(4/5)正在打开相机 ...")))


    def create_window():
        """
        Create PyQt MainWindow.

        This is just a simulation.
        This part will be implemented in the future.

        :return: None
        """
        app.w = MainWindow("appsettings.xml")
        QTimer.singleShot(400, lambda: (splashScreen.progressBar.setValue(100),
                                        splashScreen.progressBarStatusLabel.setText("(5/5)加载完毕"),
                                        splashScreen.finish(app.w),
                                        app.setStyleSheet(mainWindowStyle),
                                        app.w.show()))


    splashScreen.progressBarStatusLabel.setText("(1/5)正在创建界面 ...")

    load_config()
    load_model()
    load_camera()
    create_window()

    """
    Finally, enter the main loop of the program.
    Event processing starts from this line code, 
    and the main loop receives the event message and distributes it to each control of the program.
    If exit() is called or the main control is destroyed, the main loop ends.
    Use sys.exit () method exit ensures that the program ends completely,
    In this case, the system environment variable records how the program exited.
    """
    app.exec_()

    """whether the program can be restarted"""
    from ui.MainWindow import canRestart

    if canRestart:
        restart(str(options.twice + 1))
