from PyQt4 import QtGui, QtCore

# TODO: run button (continue), stop button (pause), reset button
# TODO: load schedule, clear schedule (?)
# TODO: current time,



class ScheduleControl(QtGui.QToolBar):

	def __init__(self):
		super(ScheduleControl, self).__init__("Schedule control")
		self.setObjectName("schedule_control")

		# if set, it is used to display current schedule
		self._schedule_view = None
		self._vc_driver = None

		self._a_open = QtGui.QAction(QtGui.QIcon("img/file_open.svg"), "Open schedule (CSV)", self)
		self._a_open.triggered.connect(self.runSchedule)

		self._a_run = QtGui.QAction(QtGui.QIcon("img/play.svg"), "Run schedule", self)
		self._a_run.triggered.connect(self.runSchedule)
		self._a_run.setEnabled(False)

		self._a_stop = QtGui.QAction(QtGui.QIcon("img/stop.svg"), "Stop/pause schedule", self)
		self._a_stop.triggered.connect(self.stopSchedule)
		self._a_stop.setEnabled(False)

		self._a_restart = QtGui.QAction(QtGui.QIcon("img/reload.svg"), "Restart schedule", self)
		self._a_restart.triggered.connect(self.restartSchedule)
		self._a_restart.setEnabled(False)

		self.addAction(self._a_open)
		self.addSeparator()
		self.addAction(self._a_run)
		self.addAction(self._a_stop)
		self.addAction(self._a_restart)


	def setScheduleView(self, schedule_view):
		"""Set schedule view usd to display currently loaded valve schedule"""

		self._schedule_view = schedule_view


	def setVcDriver(self, vc_driver):
		self._vc_driver = vc_driver


	def runSchedule(self):
		pass


	def stopSchedule(self):
		pass


	def restartSchedule(self):
		pass
