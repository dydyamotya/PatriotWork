import itertools
import sys

from PySide2 import QtWidgets, QtCore

from gasmix import GasMix, GasMixException
from functools import partial


class MyMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.stopped = True
        self._init_gui()
        self.gasmix = None
        self.gas_iterator = itertools.cycle((2, 0, 2, 1))

    def _init_gui(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QFormLayout()

        self.timer = QtCore.QTimer()

        main_layout.addLayout(layout)

        self.gas_cycle_time = QtWidgets.QLineEdit()
        self.comport = QtWidgets.QLineEdit()
        self.toggle_button = QtWidgets.QPushButton(text="Start")
        self.toggle_button.clicked.connect(self.toggle)
        self.current_gas = QtWidgets.QLabel()

        buttons_layout = QtWidgets.QVBoxLayout()
        for i in range(3):
            button = QtWidgets.QPushButton(text=str(i))
            button.clicked.connect(partial(self.choose_gas, i))
            buttons_layout.addWidget(button)

        layout.addRow("Cycle time", self.gas_cycle_time)
        layout.addRow("Comport", self.comport)
        layout.addWidget(self.toggle_button)
        layout.addRow("Current gas", self.current_gas)
        main_layout.addLayout(buttons_layout)

        self.show()

    def choose_gas(self, i):
        if self.stopped:
            try:
                self.gasmix = GasMix(port=self.comport.text(), unit_num=11)
            except GasMixException:
                pass
            else:
                self.gasmix.open_valve_close_others(i)
                self.gasmix.close()

    def toggle(self):
        if self.stopped:
            self.toggle_button.setText("Stop")
            self.start_cycle()
        else:
            self.toggle_button.setText("Start")
            self.stop_cycle()

    def start_cycle(self):
        self.stopped = False

        try:
            period = int(self.gas_cycle_time.text())
        except ValueError:
            self.error_start()
        else:
            self.timer.setInterval(period * 1000)
            try:
                self.gasmix = GasMix(port=self.comport.text(), unit_num=11)
            except GasMixException:
                self.error_start()
            else:
                self.gasmix.open_valve_close_others(next(self.gas_iterator))
                self.timer.timeout.connect(self._cycle)
                self.timer.start()

    def stop_cycle(self):
        self.stopped = True
        self.timer.stop()

    def error_start(self):
        self.toggle_button.setText("Start")
        self.stop_cycle()

    def _cycle(self):
        gas = next(self.gas_iterator)
        self.gasmix.open_valve_close_others(gas)
        self.current_gas.setText(str(gas))


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    win = MyMainWindow()

    sys.exit(app.exec_())
