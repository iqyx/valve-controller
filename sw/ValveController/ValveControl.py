from PyQt4 import QtGui, QtCore
import threading


class ValveButton(QtGui.QPushButton):

	entered = QtCore.pyqtSignal()
	left = QtCore.pyqtSignal()

	def __init__(self, num):
		super(ValveButton, self).__init__()
		self.setStyleSheet("background-color: #fff;")
		self.setFixedSize(QtCore.QSize(40, 25))
		self.setCheckable(True)

		icon = QtGui.QIcon()
		icon.addFile("img/valve_closed.svg", mode = QtGui.QIcon.Normal, state = QtGui.QIcon.Off)
		icon.addFile("img/valve_closed.svg", mode = QtGui.QIcon.Active, state = QtGui.QIcon.Off)
		icon.addFile("img/valve_opened.svg", mode = QtGui.QIcon.Normal, state = QtGui.QIcon.On)
		icon.addFile("img/valve_opened.svg", mode = QtGui.QIcon.Active, state = QtGui.QIcon.On)
		self.setIcon(icon)

		self.setText(str(num))

		self._num = num

	def enterEvent(self, event):
		self.entered.emit()

	def leaveEvent(self, event):
		self.left.emit()

	def getNum(self):
		return self._num


class ValveControl(QtGui.QDockWidget):

	def __init__(self):
		super(ValveControl, self).__init__("Valve control")
		self.setObjectName("valve_control")
		self._vc_driver = None
		self._valve_count = 0

		self._vlayout = QtGui.QVBoxLayout()
		#~ self._vlayout.setSpacing(0)
		self._widget = QtGui.QWidget()
		self._widget.setLayout(self._vlayout)
		self.setWidget(self._widget)

		self._update_timer = QtCore.QTimer()
		self._update_timer.timeout.connect(self._update)
		self._update_timer.start(100)


	def setVcDriver(self, vc_driver):
		self._vc_driver = vc_driver


	def _clearButtons(self):
		for v in reversed(range(self._vlayout.count())):
			hlayout = self._vlayout.itemAt(v)
			for h in reversed(range(hlayout.count())):
				item = hlayout.itemAt(h)
				if item.widget():
					item.widget().close()
				hlayout.removeItem(item)


	def _makeButtons(self):
		for vc in self._vc_driver._vc_list:
			label = QtGui.QLabel("%s:%s  " % (vc._host, vc._port))

			hlayout = QtGui.QHBoxLayout()
			hlayout.setSpacing(0)
			hlayout.addWidget(label)
			for i in range (vc._valve_count):
				b = ValveButton(vc._valve_start + i)
				b.clicked.connect(self._buttonClicked)
				b.entered.connect(self._buttonEntered)
				b.left.connect(self._buttonLeft)
				hlayout.addWidget(b)

			hlayout.addStretch()
			self._vlayout.addLayout(hlayout)


	def _updateButtons(self):
		for v in range(self._vlayout.count()):
			hlayout = self._vlayout.itemAt(v)
			for h in range(hlayout.count()):
				w = hlayout.itemAt(h).widget()
				if isinstance(w, QtGui.QPushButton):
					if w.getNum() in self._vc_driver._valve_state:
						w.setChecked(True)
						w.setStyleSheet("background-color: #fcc;")
					else:
						w.setChecked(False)
						w.setStyleSheet("background-color: #fff;")


	def _buttonClicked(self):
		if self._vc_driver:
			self._vc_driver.setValve(self.sender().getNum(), self.sender().isChecked())


	def _buttonEntered(self):
		if self._vc_driver:
			self._vc_driver.setHighlight(self.sender().getNum(), True)


	def _buttonLeft(self):
		if self._vc_driver:
			self._vc_driver.setHighlight(self.sender().getNum(), False)


	def _update(self):
		if self._vc_driver:
			n = self._vc_driver.numOfValves()
			if n != self._valve_count:
				self._valve_count = n
				self._updateDisplay()
			self._updateButtons()


	def _updateDisplay(self):
		self._clearButtons()
		self._makeButtons()
