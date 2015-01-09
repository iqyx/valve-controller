from PyQt4 import QtGui, QtCore

class ScheduleView(QtGui.QDockWidget):

	def __init__(self):
		super(ScheduleView, self).__init__("Schedule view")
		self.setObjectName("schedule_view")

		self.setMinimumWidth(400)
		self.setMinimumHeight(120)

		self._table = QtGui.QTreeWidget()
		#~ self._table.setEnabled(False)
		self._table.setIconSize(QtCore.QSize(20, 20))
		self.setWidget(self._table);

		self._icon_opened = QtGui.QIcon("img/valve_opened.svg")
		self._icon_closed = QtGui.QIcon("img/valve_closed.svg")

	def setColumns(self, valves):
		self._table.setColumnCount(valves + 1)

		self._table.headerItem().setText(0, "Time")
		self._table.setColumnWidth(0, 120)
		for valve in range(valves):
			self._table.headerItem().setText(valve + 1, str(valve))
			self._table.setColumnWidth(valve + 1, 20)


	def clearSchedule(self):
		self._table.clear()


	def setSchedule(self, schedule, columns):
		"""Set schedule to view.

		Schedule is a list of ScheduleItem objects.
		"""

		print "setSchedule, rows = %d, columns = %d" % (len(schedule), columns)

		self.setColumns(columns)

		for schedule_item in schedule:
			item = QtGui.QTreeWidgetItem()
			item.setText(0, self.formatTime(schedule_item.getTime()))
			valve_list = schedule_item.getValves()
			for i in range(columns):
				if i in valve_list:
					item.setIcon(i + 1, self._icon_opened)
					item.setText(i + 1, "opened")
				else:
					item.setIcon(i + 1, self._icon_closed)
					item.setText(i + 1, "closeed")

			self._table.addTopLevelItem(item)


	def setPosition(self, position):
		self._table.setCurrentIndex(self._table.model().index(position, 0))


	def formatTime(self, t):
		return "%dh %dm %.03fs" % (int(t / 3600), int((t % 3600) / 60), t % 60)
