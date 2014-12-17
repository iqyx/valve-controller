from PyQt4 import QtGui, QtCore

class ScheduleView(QtGui.QDockWidget):

	def __init__(self):
		super(ScheduleView, self).__init__("Schedule view")
		self.setObjectName("schedule_view")

		self.setMinimumWidth(400)
		self.setMinimumHeight(120)

		self.table = QtGui.QTreeWidget()
		self.setWidget(self.table);


	def setHeaders(self, headers):
		self.table.setColumnCount(len(headers))
		self.table.setHeaderLabels(headers)

