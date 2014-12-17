from PyQt4 import QtGui, QtCore

from ValveController.MainToolbar import *
from ValveController.ScheduleControl import *
from ValveController.ValveControl import *
from ValveController.ScheduleView import *


class MainWnd (QtGui.QMainWindow):

	def __init__(self):
		super(MainWnd, self).__init__()

		self.settings =  QtCore.QSettings("valve_controller.ini", QtCore.QSettings.IniFormat)
		self.initUi()
		self.show()


	def saveSettings(self):
		self.settings.beginGroup("MainWnd")
		self.settings.setValue("state", self.saveState())
		self.settings.endGroup()


	def loadSettings(self):
		self.settings.beginGroup("MainWnd")
		self.restoreState(self.settings.value("state").toByteArray())
		self.settings.endGroup()


	def initUi(self):
		# Schedule control can be used to seek in time, load/clear valve
		# schedules, etc. It also displays all possible actions for the user.
		self.schedule_control = ScheduleControl()

		# Valve control can override active valve status and displays
		# current status of all valves.
		self.valve_control = ValveControl()

		# Just displays loaded valve schedule. May be used to seek in time
		# when the schedule is stopped/paused ("run from here" function)
		self.schedule_view = ScheduleView()
		self.schedule_view.setHeaders(("Time", "0", "1", "2", "3", "4", "5", "6", "7"))

		# Configure main window
		self.setDockNestingEnabled(True)
		self.resize(600, 400)
		self.statusBar().showMessage('Ready')
		self.setWindowTitle('Valve controller')

		# Add all available widgets/docks
		self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.schedule_control)
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.valve_control)
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.schedule_view)

		# and restore saved settings from last session
		self.loadSettings()


	def closeEvent(self, event):
		self.saveSettings()
		QtGui.qApp.quit()
