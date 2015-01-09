from PyQt4 import QtGui, QtCore
import csv

# TODO: run button (continue), stop button (pause), reset button
# TODO: load schedule, clear schedule (?)
# TODO: current time,


class ScheduleItem(object):

	def __init__(self, time = 0, valves = []):
		# time when the current schedule state will be set
		self._time = time
		self._valves = valves


	def setTime(self, time):
		self._time = time


	def setValves(self, valves):
		self._valves = valves


	def getValves(self):
		return self._valves


	def getTime(self):
		return self._time


class ScheduleControl(QtGui.QToolBar):

	def __init__(self):
		super(ScheduleControl, self).__init__("Schedule control")
		self.setObjectName("schedule_control")

		# if set, it is used to display current schedule
		self._schedule_view = None
		self._vc_driver = None

		self._a_open = QtGui.QAction(QtGui.QIcon("img/file_open.svg"), "Open schedule (CSV)", self)
		self._a_open.triggered.connect(self.openSchedule)

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

		# Valve schedule is an ordered list of ScheduleItem objects
		self._schedule = []
		self._schedule_columns = 0

		self._schedule_pos = 0
		self._schedule_running = False

		self._schedule_timer = QtCore.QTimer()
		self._schedule_timer.timeout.connect(self._scheduleTimer)


	def setVcDriver(self, vc_driver):
		self._vc_driver = vc_driver


	def setScheduleView(self, schedule_view):
		"""Set schedule view used to display currently loaded valve schedule"""

		self._schedule_view = schedule_view


	def _scheduleTimer(self):
		self.advanceSchedule(self._schedule_pos + 1)


	def advanceSchedule(self, pos):
		self._schedule_pos = pos

		if self._schedule_view:
			self._schedule_view.setPosition(pos)

		if self._vc_driver:
			self._vc_driver.setValves(self._schedule[self._schedule_pos].getValves())


	def openSchedule(self):
		"""Display a file open dialog to let the user select a new schedule CSV file"""

		if self._schedule_running:
			return

		d = QtGui.QFileDialog()
		if d.exec_():
			# if a file was selected successfully, clear current schedule
			# and load new schedule from selected files
			self.clearSchedule()
			files = d.selectedFiles()
			#~ try:
			for i in range(files.count()):
				self.loadSchedule(str(files.takeAt(i)))
			#~ except:
				# TODO
				#~ print "error opening csv file"

			self.restartSchedule()

			self._a_open.setEnabled(True)
			self._a_run.setEnabled(True)
			self._a_stop.setEnabled(False)
			self._a_restart.setEnabled(True)


	def clearSchedule(self):
		if not self._schedule_running:
			self.restartSchedule()
			self._schedule = []
			self._schedule_columns = 0

			self._a_open.setEnabled(True)
			self._a_run.setEnabled(False)
			self._a_stop.setEnabled(False)
			self._a_restart.setEnabled(False)


	def loadSchedule(self, fname):
		"""Load schedule from specified CSV file"""

		# Open the file, iterate over rows, extract first columen (count)
		# and all opened valves
		with open(fname, "rb") as csvfile:
			reader = csv.reader(csvfile, delimiter = ",", quotechar = "\"")
			maxcolumns = 0

			for row in reader:
				t = float(row.pop(0))
				v = []

				for i in range(len(row)):
					if row[i] in ["1", "y", "Y", "o", "O", "t", "T", "open"]:
						v.append(i)
						if i > maxcolumns:
							maxcolumns = i

				self._schedule.append(ScheduleItem(t, v))

			if (maxcolumns + 1) > self._schedule_columns:
				self._schedule_columns = maxcolumns + 1

		if self._schedule_view:
			self._schedule_view.setSchedule(self._schedule, self._schedule_columns)


	def runSchedule(self):
		if not self._schedule_running:
			self._schedule_running = True

			self._a_open.setEnabled(False)
			self._a_run.setEnabled(False)
			self._a_stop.setEnabled(True)
			self._a_restart.setEnabled(False)

			self._schedule_timer.start(1000)


	def stopSchedule(self):
		if self._schedule_running:
			self._schedule_running = False

			self._a_open.setEnabled(True)
			self._a_run.setEnabled(True)
			self._a_stop.setEnabled(False)
			self._a_restart.setEnabled(True)

			self._schedule_timer.stop()


	def restartSchedule(self):
		if not self._schedule_running:
			self._schedule_running = False

			self._a_open.setEnabled(True)
			self._a_run.setEnabled(True)
			self._a_stop.setEnabled(False)
			self._a_restart.setEnabled(True)
