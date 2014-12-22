from PyQt4 import QtGui, QtCore

class ScheduleView(QtGui.QDockWidget):

	def __init__(self):
		super(ScheduleView, self).__init__("Schedule view")
		self.setObjectName("schedule_view")

		self.setMinimumWidth(400)
		self.setMinimumHeight(120)

		self._table = QtGui.QTreeWidget()
		self.setWidget(self._table);


	def setValves(self, valves):
		self._table.setColumnCount(len(valves) + 1)

		self._table.headerItem().setText(0, "Time")
		self._table.setColumnWidth(0, 120)
		i = 1
		for valve in valves:
			self._table.headerItem().setText(i, valve)
			self._table.setColumnWidth(i, 20)
			i += 1
