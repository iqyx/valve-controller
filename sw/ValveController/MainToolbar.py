from PyQt4 import QtGui, QtCore

class MainToolbar(QtGui.QToolBar):

	def __init__(self):
		super(MainToolbar, self).__init__("Main toolbar")
		self.setObjectName("main_toolbar")
		self.setIconSize(QtCore.QSize(30, 30))

		self.vc_driver = None

		self.a_connect = QtGui.QAction(QtGui.QIcon("img/connect.svg"), "Connect", self)
		self.a_connect.triggered.connect(self.connect)
		# self.a_connect.setShortcut("ctrl+c")
		self.a_disconnect = QtGui.QAction(QtGui.QIcon("img/disconnect.svg"), "Disconnect", self)
		self.a_disconnect.triggered.connect(self.disconnect)

		self.addAction(self.a_connect)
		self.addAction(self.a_disconnect)

	def setVcDriver(self, vc_driver):
		self.vc_driver = vc_driver


	def connect(self):
		print "connect"

	def disconnect(self):
		pass
