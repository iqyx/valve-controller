
class VcController(object):

	def __init__(self, host, port, valve_start, valve_count):
		self._host = host
		self._port = port
		self._valve_start = valve_start
		self._valve_count = valve_count
		self._error = None


	def setError(self, error):
		self._error = error


	def getStatus(self):
		if self._error:
			return "Error %s" % self._error
		else:
			return "OK"


	def getUrl(self):
		return "http://%s:%d/" % (self._host, self._port)


class VcDriver(object):

	def __init__(self):
		# ordered list of valve controllers (VcController instances)
		self._vc_list = []
		self._connected = False
		self._valve_state = []
		self._highlight_state = []


	def connect(self, vc_list):
		"""Set current controller list.

		This method simulates a "connect". It sets a list of valve
		controller available for valve opening/closing. It also sets its
		internal state to connected and periodically tries to refresh
		valve controller statuses.
		"""


		if not self._connected:
			print "connecting vcdriver"
			self._vc_list = vc_list
			self._connected = True
			self._valve_state = []
			self._highlight_state = []

		return self


	def disconnect(self):
		"""Disconnect currently connected valve controllers
		"""

		if self._connected:
			# stop refresh timer first
			# TODO

			print "disconnecting vcdriver"
			self._connected = False
			self._vc_list = []

		return self


	def getStatus(self):
		"""Return status of all controllers as a single string."""

		if self._connected:
			return "%d valves, active controllers %s" % (self.numOfValves(), ",".join("%s (%s)" % (vc.getUrl(), vc.getStatus()) for vc in self._vc_list))
		else:
			return "Disconnected"


	def numOfValves(self):
		"""Get number of valves on all connected controllers."""

		num = 0
		for vc in self._vc_list:
			num += vc._valve_count
		return num


	def request(self, req):
		"""Make request to a single controller."""

		# When a request is to be made, check if any status refresh timer
		# is running. Stop it and make the request. Then enable the timer
		# again.
		pass


	def setHighlight(self, valves):
		"""Highlight selected valves

		Set valve highlight. Valves parameter is a list of valves to be
		highlighted (old highlights will be removed, ie. highlighted valves
		will be replaced with new set)
		"""

		for vc in self._vc_list:
			vc_valves = []
			# iterate all valves available on this controller
			for valve_num in range(vc._valve_start, vc._valve_start + vc._valve_count):
				if valve_num in valves:
					# and check if valves from this controller are
					# contained in the "valves" parameter. If so,
					# add them to vc_valves with index local to
					# this particular valve controller (remove offset)
					vc_valves.append(valve_num - vc._valve_start)

			vc_valves_bin = self.valvesToBin(vc_valves)
			self.request("%s?status_set=%d" % (vc.getUrl, vc_valves_bin))

		self._highlight_state = valves



	def addHighlight(self, valves):
		"""Highlight new valve"""
		pass


	def delHighlight(self, valves):
		"""Remove existing valve highlight."""
		pass


	def setValves(self, valves):
		"""Set valve state.

		Open valves which are in the "valves" parameter. All other valves
		will be closed.
		"""
		pass


	def openValves(self, valves):
		"""Open specified valves. Do not change other valves."""
		pass


	def closeValves(self, valves):
		"""Close specified valves. Do not change other valves."""
		pass
