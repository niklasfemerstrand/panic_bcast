#!/usr/bin/python2.7
# Copyright (c) 2012, Niklas Femerstrand <nik@qnrq.se>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import re
import os
import socket
import netinfo
import threading
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Basic HTTP server that listens to GET /panic and triggers panic.
# Written to provide a standardized interface for panic triggering.
# To trigger panic through HTTP simply request http://localhost:8080/panic
class panicHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == "/\x70\x61\x6e\x69\x63":
			sendSignal()

def httpd():
	s = HTTPServer(('', 8080), panicHandler)
	s.serve_forever()

def treatPanic():
	os.popen("killall truecrypt")
	# TODO: Improve by overwriting memory locations directly.
	#       This method crashes the kernel by overwriting sensitive
	#       addressestoo fast. C is needed to do this efficiently.
	os.popen("dd if=/dev/zero of=/dev/mem bs=" + memtotal())

def memtotal():
	# Linux:
	memtotal = int(os.popen("grep \"MemTotal\" /proc/meminfo | grep -o \"[0-9]*\"").read()) / 1024

	# TODO FreeBSD (bytes): sysctl hw.physmem
	return memtotal

def sigListener():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.bind(("", 1337)) # Listen on all devices

	while 1:
		try:
			message, address = s.recvfrom(5)
			if message == "\x70\x61\x6e\x69\x63":
				treatPanic()
		except:
			pass

# Extracts device paths from any system that uses fstab
# TODO Add ZFS support
def fstabDrives():
	drives = []
	# Verified to work on Linux
	for line in open("/etc/fstab", 'r'):
		# The comments, Jim. Don't let 'em parse.
		if line is not "" and re.match("^[ \t]*#", line) is None:
			for drive in re.findall("^[ \t]*(\/\w*\/\w*)", line):
				drives.append(drive)
	return drives

def myIP():
	for route in netinfo.get_routes():
		if route["gateway"] != "0.0.0.0":
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect((route["gateway"], 1337))
	
			ip = s.getsockname()[0]
			s.close()

			return ip

def bcast():
	bcast = re.sub("\.[0-9]+$", ".255", myIP())
	return bcast
	
def sendSignal():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto("\x70\x61\x6e\x69\x63", (bcast(), 1337))
	s.close()

	return 0

httpd = threading.Thread(name="httpd", target=httpd)
httpd.start()
sigListener = threading.Thread(name="sigListener", target=sigListener)
sigListener.start()
