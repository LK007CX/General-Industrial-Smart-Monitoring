#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QSplashScreen, QLabel, QProgressBar, QHBoxLayout, \
    QVBoxLayout, QApplication, QWidget, QDesktopWidget


class SplashScreen(QSplashScreen):

    def __init__(self, *args, **kwargs):
        super(SplashScreen, self).__init__(*args, **kwargs)

        self.movie = QMovie('icon/cap.png')

        self.GIMSLabel = QLabel("GISM", objectName="GIMSLabel")
        self.versionLabel = QLabel("V1.0.0", objectName="versionLabel")
        self.fullNameLabel = QLabel("General Industrial Smart Monitor", objectName="fullNameLabel")
        self.logoLabel = QLabel(objectName="logoLabel")

        self.productFeaturesLabel = QLabel("PRODUCT FEATURES", objectName="productFeaturesLabel")

        self.splitLabel1 = QLabel()
        self.dotLabel1 = QLabel(objectName="dotLabel1")
        self.featureLabel1 = QLabel("High speed", objectName="featureLabel1")

        self.splitLabel2 = QLabel()
        self.dotLabel2 = QLabel(objectName="dotLabel2")
        self.featureLabel2 = QLabel("High precision", objectName="featureLabel2")

        self.splitLabel3 = QLabel()
        self.dotLabel3 = QLabel(objectName="dotLabel3")
        self.featureLabel3 = QLabel("Visual configuration", objectName="featureLabel3")

        self.splitLabel4 = QLabel()
        self.dotLabel4 = QLabel(objectName="dotLabel4")
        self.featureLabel4 = QLabel("Multiple output modes", objectName="featureLabel4")

        self.progressBar = QProgressBar(textVisible=False, objectName="progressBar")
        self.progressBarStatusLabel = QLabel('正在启动程式', objectName="progressBarStatusLabel")
        self.copyRightLabel = QLabel("@Copy Right Information", objectName="copyRightLabel")
        self.init_ui()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.movie.frameChanged.connect(self.on_frame_changed)
        self.movie.start()

        self.logoLabel.setPixmap(QPixmap("icon/logo.png"))

        self.versionLabel.setMaximumHeight(25)
        self.splitLabel1.setMaximumWidth(50)
        self.splitLabel2.setMaximumWidth(50)
        self.splitLabel3.setMaximumWidth(50)
        self.splitLabel4.setMaximumWidth(50)
        self.dotLabel1.setFixedSize(QSize(10, 10))
        self.dotLabel2.setFixedSize(QSize(10, 10))
        self.dotLabel3.setFixedSize(QSize(10, 10))
        self.dotLabel4.setFixedSize(QSize(10, 10))

        layout1 = QHBoxLayout()
        layout1.addWidget(self.GIMSLabel)
        layout1.addWidget(self.versionLabel, 0, Qt.AlignLeft)

        layout2 = QVBoxLayout()
        layout2.addLayout(layout1)
        layout2.addWidget(self.fullNameLabel)

        layout3 = QHBoxLayout()
        layout3.addLayout(layout2)
        layout3.addWidget(self.logoLabel, 0, Qt.AlignRight)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.splitLabel1)
        layout4.addWidget(self.dotLabel1)
        layout4.addWidget(self.featureLabel1)

        layout5 = QHBoxLayout()
        layout5.addWidget(self.splitLabel2)
        layout5.addWidget(self.dotLabel2)
        layout5.addWidget(self.featureLabel2)

        layout6 = QHBoxLayout()
        layout6.addWidget(self.splitLabel3)
        layout6.addWidget(self.dotLabel3)
        layout6.addWidget(self.featureLabel3)

        layout7 = QHBoxLayout()
        layout7.addWidget(self.splitLabel4)
        layout7.addWidget(self.dotLabel4)
        layout7.addWidget(self.featureLabel4)

        layout8 = QVBoxLayout()
        layout8.addWidget(self.productFeaturesLabel)
        layout8.addLayout(layout4)
        layout8.addLayout(layout5)
        layout8.addLayout(layout6)
        layout8.addLayout(layout7)

        layout9 = QVBoxLayout()
        layout9.addWidget(self.progressBar)
        layout9.addWidget(self.progressBarStatusLabel, 0, Qt.AlignCenter)
        layout9.addWidget(self.copyRightLabel)

        """layout"""
        layout = QVBoxLayout()
        layout.addLayout(layout3)
        layout.addLayout(layout8)
        layout.addLayout(layout9)
        self.setLayout(layout)

        self.setContentsMargins(20, 20, 20, 20)
        self.setFixedSize(QSize(600, 400))

    def center(self):
        """
        Make the window show in the middle of the screen.
        :return: None
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def handle_status(self, text, value):
        """
        Slot function of the progress bar and the status label state change.
        :param text: The text to be displayed on the status label.
        :param value: The value to be displayed on the process bar.
        :return: None
        """
        self.progressBarStatusLabel.setText(text)
        self.progressBar.setValue(value)

    def on_frame_changed(self):
        """
        Slot function of movie's frameChanged.
        :return: None
        """
        self.setPixmap(self.movie.currentPixmap())

    def finish(self, widget):
        """
        The event when the splash screen finish.
        :param widget: The widget that you want to open when the splash screen finished.
        :return: None
        """
        self.movie.stop()
        super(SplashScreen, self).finish(widget)

    def mousePressEvent(self, event):
        """
        Mouse press event.
        :param event:
        :return: None
        """
        event.ignore()


if __name__ == '__main__':
    import sys
    import cgitb

    cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    splash.raise_()


    def load_config():
        pass
        QTimer.singleShot(1000, lambda: (splash.progressBar.setValue(10),
                                         splash.progressBarStatusLabel.setText("正在读取配置...")))


    def load_model():
        pass
        QTimer.singleShot(4000, lambda: (splash.progressBar.setValue(30),
                                         splash.progressBarStatusLabel.setText("正在加载模型...")))


    def load_camera():
        pass
        QTimer.singleShot(5000, lambda: (splash.progressBar.setValue(80),
                                         splash.progressBarStatusLabel.setText("正在打开相机...")))


    def create_window():
        app.w = QWidget()
        QTimer.singleShot(6000, lambda: (splash.progressBar.setValue(100),
                                         splash.progressBarStatusLabel.setText("加载完毕"),
                                         app.w.show(),
                                         splash.finish(app.w)))


    splash.progressBarStatusLabel.setText("正在创建界面...")
    load_config()
    load_model()
    load_camera()
    create_window()
    sys.exit(app.exec_())
