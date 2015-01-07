#!/usr/bin/python

import socket
import time
import sys
import struct

ip = sys.argv[1]
port = int(sys.argv[2])
print "sending to %s:%d" % (ip, port)

udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsock.sendto("v%s" % struct.pack("!I", 0), (ip, port))
udpsock.sendto("h%s" % struct.pack("!I", 0), (ip, port))

valves = "00000000000000000000000000001111";

while True:
	print "Sending update %s" % valves
	udpsock.sendto("v%s" % struct.pack("!I", int(valves, 2)), (ip, port))

	# rotate valves
	valves = valves[1:] + valves[:1]
	time.sleep(0.1)
