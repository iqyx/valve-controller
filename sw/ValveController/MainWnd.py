from PyQt4 import QtGui, QtCore

from ValveController.MainToolbar import *
from ValveController.ScheduleControl import *
from ValveController.ValveControl import *
from ValveController.ScheduleView import *
from ValveController.VcDriver import *

class MainWnd (QtGui.QMainWindow):

	def __init__(self):
		super(MainWnd, self).__init__()

		self._vc_driver = VcDriver()

		self._settings =  QtCore.QSettings("valve_controller.ini", QtCore.QSettings.IniFormat)
		self.initUi()
		self.show()

		# window status update timer
		self._status_utimer = QtCore.QTimer()
		self._status_utimer.timeout.connect(self.updateStatusBar)
		self._status_utimer.start(1000)


	def updateStatusBar(self):
		self.statusBar().showMessage(self._vc_driver.getStatus())

	def saveSettings(self):
		self._settings.beginGroup("MainWnd")
		self._settings.setValue("state", self.saveState())
		self._settings.endGroup()


	def loadSettings(self):
		self._settings.beginGroup("MainWnd")
		self.restoreState(self._settings.value("state").toByteArray())
		self._settings.endGroup()


	def initUi(self):

		# Valve control can override active valve status and displays
		# current status of all valves.
		self._valve_control = ValveControl()
		self._valve_control.setVcDriver(self._vc_driver)

		# Just displays loaded valve schedule. May be used to seek in time
		# when the schedule is stopped/paused ("run from here" function)
		self._schedule_view = ScheduleView()

		# Schedule control can be used to seek in time, load/clear valve
		# schedules, etc. It also displays all possible actions for the user.
		self._schedule_control = ScheduleControl()
		self._schedule_control.setScheduleView(self._schedule_view)
		self._schedule_control.setVcDriver(self._vc_driver)

		self._toolbar = MainToolbar()
		self._toolbar.setVcDriver(self._vc_driver)

		# Configure main window
		self.setDockNestingEnabled(True)
		self.resize(600, 400)
		self.statusBar().showMessage('Ready')
		self.setWindowTitle('Valve controller')

		# Add all available widgets/docks
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._valve_control)
		self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._schedule_view)
		self.addToolBar(self._toolbar)
		self.addToolBar(self._schedule_control)

		# and restore saved settings from last session
		self.loadSettings()


	def closeEvent(self, event):
		self.saveSettings()
		self._vc_driver.disconnect()
		QtGui.qApp.quit()
