import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSpinBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import Qt
import threading
import time
import pyautogui
# Disable PyAutoGUI fail-safe mechanism
pyautogui.FAILSAFE = False

class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()

        self.auto_click = False
        self.click_interval = 100  # Milliseconds

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.label_status = QLabel('Auto-Click: OFF', self)
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.toggle_auto_click)

        self.label_x = QLabel('X:', self)
        self.label_y = QLabel('Y:', self)
        self.label_interval = QLabel('Interval (ms):', self)

        self.input_x = QLineEdit(self)
        self.input_y = QLineEdit(self)
        self.input_interval = QSpinBox(self)
        self.input_interval.setMinimum(10)
        self.input_interval.setMaximum(10000)
        self.input_interval.setValue(self.click_interval)

        # Create a layout for the X and Y inputs
        coordinate_layout = QHBoxLayout()
        coordinate_layout.addWidget(self.label_x)
        coordinate_layout.addWidget(self.input_x)
        coordinate_layout.addWidget(self.label_y)
        coordinate_layout.addWidget(self.input_y)

        # Create a layout for the interval input
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.label_interval)
        interval_layout.addWidget(self.input_interval)

        # Create a layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_status)
        layout.addLayout(coordinate_layout)
        layout.addLayout(interval_layout)
        layout.addWidget(self.start_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle('Auto Clicker')
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

    def stop_auto_click(self):
        if self.auto_click:
            self.auto_click = False
            self.start_button.setText('Start')
            self.label_status.setText('Auto-Click: OFF')

    def toggle_auto_click(self):
        self.auto_click = not self.auto_click
        if self.auto_click:
            self.start_button.setText('Stop')
            self.label_status.setText('Auto-Click: ON')
            self.click_interval = self.input_interval.value()
            self.click_thread = threading.Thread(target=self.auto_click_thread)
            self.click_thread.start()
        else:
            self.start_button.setText('Start')
            self.label_status.setText('Auto-Click: OFF')

    def auto_click_thread(self):
        while self.auto_click:
            try:
                x = int(self.input_x.text())
                y = int(self.input_y.text())
                pyautogui.click(x, y)
            except ValueError:
                print("Invalid X or Y coordinate.")
            time.sleep(self.click_interval / 1000.0)

class AutoClickerApp(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create an instance of AutoClicker
        self.window = AutoClicker()
        self.window.show()

        # Create a shortcut to stop the auto-clicker (Ctrl+Q)
        stop_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self.window)
        stop_shortcut.activated.connect(self.window.stop_auto_click)


if __name__ == '__main__':
    app = AutoClickerApp(sys.argv)
    sys.exit(app.exec_())
