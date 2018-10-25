from PyQt4 import QtGui, QtCore
from ValveController.VcDriver import *
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import struct

class VcSelectBox(QtGui.QComboBox):

	def __init__(self):
		super(VcSelectBox, self).__init__()
		self.setEditable(True)
		self.setMinimumWidth(300);

		self._sock = socket(AF_INET, SOCK_DGRAM)
		self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self._sock.bind(("", 5001))
		self._sock.settimeout(0.1)

		self._recv_timer = QtCore.QTimer()
		self._recv_timer.timeout.connect(self._recvTimer)
		self._recv_timer.start(1000)

		self._ip_list = []
		self.addNew("192.168.0.20 (Default)")

	def _recvTimer(self):
		try:
			(data, addr) = self._sock.recvfrom(64)
			if len(data) == 12 and data[:2] == "vc":
				p = struct.unpack("10B", data[2:])
				ip = "%d.%d.%d.%d" % p[0:4]
				mac = "%02x:%02x:%02x:%02x:%02x:%02x" % p[4:10]
				self.addNew("%s (%s)" % (ip, mac))

		except:
			pass

	def addNew(self, ip):
		if not ip in self._ip_list:
			self._ip_list.append(ip)
			self.addItem(ip)




class MainToolbar(QtGui.QToolBar):

	def __init__(self):
		super(MainToolbar, self).__init__("Main toolbar")
		self.setObjectName("main_toolbar")
		self.setIconSize(QtCore.QSize(30, 30))

		self._vc_driver = None

		self._select_box = VcSelectBox()

		self._a_connect = QtGui.QAction(QtGui.QIcon("img/connect.svg"), "Connect", self)
		self._a_connect.triggered.connect(self.connect)
		# self._a_connect.setShortcut("ctrl+c")
		self._a_disconnect = QtGui.QAction(QtGui.QIcon("img/disconnect.svg"), "Disconnect", self)
		self._a_disconnect.triggered.connect(self.disconnect)
		self._a_disconnect.setEnabled(False)

		self.addWidget(self._select_box)
		self.addAction(self._a_connect)
		self.addAction(self._a_disconnect)

	def setVcDriver(self, vc_driver):
		self._vc_driver = vc_driver


	def connect(self):
		if self._vc_driver:
			vclist = []
			vclist.append(VcController(self._select_box.currentText().split(" ")[0], 5000, 0, 24))
			self._select_box.addNew(self._select_box.currentText())
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
