import threading
import socket
import struct

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



class VcDriver(object):

	def __init__(self):
		# ordered list of valve controllers (VcController instances)
		self._vc_list = []
		self._connected = False
		self._valve_state = []
		self._highlight_state = []
		self._update_timer = None
		self._udp_socket = None
		self._update()


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
			self._valve_state = []
			self._highlight_state = []
			self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self._connected = True

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
			self._udp_socket = None

		return self


	def getStatus(self):
		"""Return status of all controllers as a single string."""

		if self._connected:
			return "%d valves, active controllers %s" % (self.numOfValves(), ",".join("%s:%d (%s)" % (vc._host, vc._port, vc.getStatus()) for vc in self._vc_list))
		else:
			return "Disconnected"


	def numOfValves(self):
		"""Get number of valves on all connected controllers."""

		num = 0
		for vc in self._vc_list:
			num += vc._valve_count
		return num


	def _valvesToBin(self, valves):

		c = 0
		for valve in valves:
			c += 1 << valve
		return c


	def _update(self):
		"""Update valve controllers ith current status."""

		if self._update_timer:
			self._update_timer.cancel()
			self._update_timer = None

		for vc in self._vc_list:
			vc_valve_state = []
			vc_highlight_state = []
			# iterate all valves available on this controller
			for valve_num in range(vc._valve_start, vc._valve_start + vc._valve_count):
				if valve_num in self._valve_state:
					vc_valve_state.append(valve_num - vc._valve_start)
				if valve_num in self._highlight_state:
					vc_highlight_state.append(valve_num - vc._valve_start)

			vc_valves_bin = self._valvesToBin(vc_valve_state)
			vc_highlights_bin = self._valvesToBin(vc_highlight_state)

			#~ print "vc %s:%d: valves %d highlight %d" % (vc._host, vc._port, vc_valves_bin, vc_highlights_bin)
			self._udp_socket.sendto("v%s" % struct.pack("!I", vc_valves_bin), (vc._host, vc._port))
			self._udp_socket.sendto("h%s" % struct.pack("!I", vc_highlights_bin), (vc._host, vc._port))

		self._update_timer = threading.Timer(0.5, self._update)
		self._update_timer.daemon = True
		self._update_timer.start()


	def setHighlights(self, valves):
		"""Highlight selected valves

		Set valve highlight. Valves parameter is a list of valves to be
		highlighted (old highlights will be removed, ie. highlighted valves
		will be replaced with new set)
		"""
		self._highlight_state = valves
		self._update()


	def setHighlight(self, valve, state):

		if state:
			if not valve in self._highlight_state:
				self._highlight_state.append(valve)
		else:
			if valve in self._highlight_state:
				self._highlight_state.remove(valve)
		self._update()


	def setValves(self, valves):
		"""Set valve state.

		Open valves which are in the "valves" parameter. All other valves
		will be closed.
		"""
		self._valve_state = valves
		self._update()


	def setValve(self, valve, state):

		if state:
			if not valve in self._valve_state:
				self._valve_state.append(valve)
		else:
			if valve in self._valve_state:
				self._valve_state.remove(valve)
		self._update()

