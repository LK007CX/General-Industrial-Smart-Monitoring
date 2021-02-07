import sys
import xml.etree.ElementTree as ET

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, \
    QVBoxLayout, QSplitter, QApplication

from ui.SwitchButton import SwitchButton


class RemoteCVSettingsWidget(QWidget):

    def __init__(self, config_path, *args, **kwargs):
        super(RemoteCVSettingsWidget, self).__init__(*args, **kwargs)
        self.configPath = config_path
        self.enableLabel = QLabel("启用远程视频推送")
        self.enableSwitchButton = SwitchButton()
        self.savePushButton = QPushButton("保存")
        self.init_ui()
        self.load_config()

    def init_ui(self):
        """
        Initialize UI.
        :return: None
        """
        self.savePushButton.clicked.connect(self.saveAction)
        self.enableSwitchButton.setFixedSize(QSize(40, 24))
        enableLayout = QHBoxLayout()
        enableLayout.addWidget(QLabel())
        enableLayout.addWidget(self.enableLabel)
        enableLayout.addWidget(self.enableSwitchButton)
        enableLayout.addWidget(QLabel())
        layout = QVBoxLayout()
        layout.addWidget(QSplitter(Qt.Vertical))
        layout.addLayout(enableLayout)
        layout.addWidget(QLabel())
        layout.addWidget(self.savePushButton, 0, Qt.AlignCenter)
        layout.addWidget(QSplitter(Qt.Vertical))
        self.setLayout(layout)

    def load_config(self):
        """
        Load application configuration.
        :return: None
        """
        tree = ET.parse(self.configPath)
        root = tree.getroot()

        enable = bool(int(root.find('remotecv').find('enable').text))
        self.enableSwitchButton.setChecked(enable)

    def saveAction(self):
        """
        Slot function to save user parameters.
        :return: None
        """
        tree = ET.parse(self.configPath)
        root = tree.getroot()

        enable = self.enableSwitchButton.checked
        root.find('remotecv').find('enable').text = "1" if enable else "0"
        tree.write(self.configPath)

    def showEvent(self, QShowEvent):
        """
        Reload application configuration when widget show again.
        :param QShowEvent: event
        :return: None
        """
        self.load_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RemoteCVSettingsWidget('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
