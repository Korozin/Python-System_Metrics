import psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

class SystemMonitor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('System Metrics : KorOwOzin')
        self.setFixedSize(420, 500)

        self.cpu_label = QtWidgets.QLabel(self)
        self.ram_label = QtWidgets.QLabel(self)
        self.storage_label = QtWidgets.QLabel(self)
        self.temp_label = QtWidgets.QLabel(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.storage_label)
        self.layout.addWidget(self.temp_label)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)  # update every second

    def update_labels(self):
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        storage_percent = psutil.disk_usage("/").percent
        
        sensor_output = os.popen('sensors').read()

        self.cpu_label.setText("CPU Usage: {}%".format(cpu_percent))
        self.ram_label.setText("RAM Usage: {}%".format(ram_percent))
        self.storage_label.setText("Storage Usage: {}%".format(storage_percent))
        self.temp_label.setText("\nCPU Metrics:\n\n{}".format(sensor_output))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    monitor = SystemMonitor()
    monitor.show()
    app.exec_()
