import psutil
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import subprocess

class SystemMonitor(QWidget):
    # Creates a signal that will emit when the timer is up
    update_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle('System Monitor')
        self.setFixedSize(375, 370)
        # Create tabs for the interface
        self.create_tabs()
        # Create widgets for the interface
        self.create_widgets()
        # Create layouts for the interface
        self.create_layouts()
        # Create a timer that will call the update_labels function
        self.create_timer()
        # Connect the signal to the update_labels function
        self.update_signal.connect(self.update_labels)
        # Update the labels when the program starts
        self.update_labels()


    def create_tabs(self):
        # Create a tabwidget
        self.tab_widget = QTabWidget(self)
        # Create a basic tab
        self.basic_tab = QWidget()
        # Create an advanced tab
        self.advanced_tab = QWidget()
        # Add the basic tab to the tabwidget
        self.tab_widget.addTab(self.basic_tab, "Basic")
        # Add the advanced tab to the tabwidget
        self.tab_widget.addTab(self.advanced_tab, "Advanced")


    # Create widgets for displaying metrics
    def create_widgets(self):
        # Create a list to hold the CPU Metric labels
        self.cpu_metrics = []
        # Create a label for each CPU Core
        for i in range(psutil.cpu_count()):
            label = QLabel(self.basic_tab)
            label.setFixedHeight(20)
            self.cpu_metrics.append(label)
        
        # Create a label to hold the RAM Usage
        self.ram_usage = QLabel(self.basic_tab)
        # Create a label to hold the Disk Usage
        self.storage_usage = QLabel(self.basic_tab)
        # Create a label to hold the CPU Temperature
        self.cpu_temp = QLabel(self.basic_tab)
        # Create a TextEdit Widget to hold Advanced Metrics
        self.sensors_output = QTextEdit(self.advanced_tab)
        # Resize TextEdit Widget to fix Application Size
        self.sensors_output.resize(375, 370)
        # Set TextEdit Widget to read only
        self.sensors_output.setReadOnly(True)


    # Create layouts for widgets
    def create_layouts(self):
        # Create a vertical layout for the basic tab
        vbox = QVBoxLayout(self.basic_tab)
        vbox.setSpacing(5)
        # Add the cpu metric labels to the layout
        for label in self.cpu_metrics:
            vbox.addWidget(label)
        # Add the RAM Usage label to the layout
        vbox.addWidget(self.ram_usage)
        # Add the Storage Usage label to the layout
        vbox.addWidget(self.storage_usage)
        # Add the CPU Temperature Usage label to the layout
        vbox.addWidget(self.cpu_temp)
        
        # Create a new Layout to apply to the Tab Widgets
        layout = QVBoxLayout(self)
        # Apply Layout to Tab Widgets
        layout.addWidget(self.tab_widget)


    # Create timer for updating metrics
    def create_timer(self):
        self.timer = QtCore.QTimer(self)
        # Link timeout to pyqtSignal()
        self.timer.timeout.connect(self.update_signal)
        # Updates every second
        self.timer.start(1000)               
        
        
    # Update labels with current system metrics
    def update_labels(self):
        # Helper function to fetch CPU temperature using psutil
        def get_cpu_temp():
            # Use subprocess to fetch advanced system metrics
            global output
            output = subprocess.run(['sensors'], stdout=subprocess.PIPE,      stderr=subprocess.PIPE).stdout.decode()
            # look for 'CPU:' string in full output to put into 'Basic' tab
            for line in output.splitlines():
                if 'CPU:' in line:
                    # format output so it shows just the CPU Temperature for 'Basic' tab
                    return str(line.split()[-1][1:-2])
                    
        # Set Label heights so they aren't spaced too far apart
        self.ram_usage.setFixedHeight(40)
        self.storage_usage.setFixedHeight(20)
        self.cpu_temp.setFixedHeight(20)
    
        # Use psutil to grab Basic metrics
        cpu_percent = psutil.cpu_percent(percpu=True)
        ram_percent = psutil.virtual_memory().percent
        storage_percent = psutil.disk_usage("/").percent
        # Define 'cpu_temp' as the formatted string from the function 'get_cpu_temp()'
        cpu_temp = get_cpu_temp()
        # Split CPU Core labels so they output individually
        for i, label in enumerate(self.cpu_metrics):
            label.setText(f"CPU Core {i+1}: {cpu_percent[i]}%")
        # output RAM Usage below CPU metrics
        self.ram_usage.setText("\nRAM Usage: {}%".format(ram_percent))
        # if info grab is successful, output data. If not, output error message
        if cpu_temp:
            self.cpu_temp.setText("CPU Temperature: {}°C".format(cpu_temp))
            self.storage_usage.setText("Storage Usage: {}%".format(storage_percent))
        else:
            self.cpu_temp.setText("CPU Temperature: Unavailable")
            self.storage_usage.setText("Storage Usage: {}%".format(storage_percent))
        # Use Global Var 'output' to show Advanced metrics
        self.sensors_output.setText(output)
        
# Start program
if __name__ == "__main__":
    app = QApplication([])
    monitor = SystemMonitor()
    monitor.show()
    app.exec_()
