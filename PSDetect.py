#if run PSDetect on alice, need to specify interface to be eth1 by typing
#	python PSDetect.py eth1
#in command line

import sys,pcap,dpkt,datetime

class IP:

	def __init__(self, address):
		self.address = address
		self.portlist = []
		self.record = {}
		self.head = 0
	
	def add(self, port, time):
		self.portlist.append((port, time))
		if port in self.record: self.record[port] += 1
		else: self.record[port] = 1
		while (time - self.portlist[self.head][1]).seconds > 5:
			headport = self.portlist[self.head][0]
			if self.record[headport] == 1:
				del self.record[headport]
			else: self.record[headport] -=1
			self.head += 1
		if len(self.record) >= 30: 
			print 'Scanner detected. The scanner originated from host %s'%self.address 
			sys.exit(0)	 

dev = 'eth0'

#can select which interface to detect
if len(sys.argv)>1:
	dev = sys.argv[1]
	#print dev

iplist = []
pc = pcap.pcap(dev)
pc.setfilter('tcp')
for ptime,pdata in pc:
	current_time = datetime.datetime.now()
	p = dpkt.ethernet.Ethernet(pdata)
#	print ('%x',p)
	src = '%d.%d.%d.%d' % tuple(map(ord,list(p.data.src)))
	port = p.data.data.dport
	flag = True
	for ip in iplist:
		if ip.address == src: 
			flag = False
			ip.add(port, current_time) 
	if flag:
		ip = IP(src)
		ip.add(port, current_time)
		iplist.append(ip)

#	print p.data.data.dport
