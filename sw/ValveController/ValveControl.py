from PyQt4 import QtGui, QtCore

class ValveControl(QtGui.QDockWidget):

	def __init__(self):
		super(ValveControl, self).__init__("Valve control")
		self.setObjectName("valve_control")

