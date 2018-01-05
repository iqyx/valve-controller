from PyQt4 import QtGui, QtCore
from ValveController.VcDriver import *


class VcSelectBox(QtGui.QComboBox):

	def __init__(self):
		super(VcSelectBox, self).__init__()




class MainToolbar(QtGui.QToolBar):

	def __init__(self):
		super(MainToolbar, self).__init__("Main toolbar")
		self.setObjectName("main_toolbar")
		self.setIconSize(QtCore.QSize(30, 30))

		self._vc_driver = None

		self._a_connect = QtGui.QAction(QtGui.QIcon("img/connect.svg"), "Connect", self)
		self._a_connect.triggered.connect(self.connect)
		# self._a_connect.setShortcut("ctrl+c")
		self._a_disconnect = QtGui.QAction(QtGui.QIcon("img/disconnect.svg"), "Disconnect", self)
		self._a_disconnect.triggered.connect(self.disconnect)
		self._a_disconnect.setEnabled(False)

		self.addAction(self._a_connect)
		self.addAction(self._a_disconnect)

	def setVcDriver(self, vc_driver):
		self._vc_driver = vc_driver


	def connect(self):
		if self._vc_driver:
			vclist = []
			vclist.append(VcController("192.168.88.138", 5000, 0, 24))
			self._vc_driver.connect(vclist)

			# manipulate toolbar buttons and vcdriver selection
			self._a_connect.setEnabled(False)
			self._a_disconnect.setEnabled(True)

	def disconnect(self):
		if self._vc_driver:
			self._vc_driver.disconnect()

			# manipulate toolbar buttons and vcdriver selection
			self._a_connect.setEnabled(True)
			self._a_disconnect.setEnabled(False)
