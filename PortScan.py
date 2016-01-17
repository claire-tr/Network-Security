import sys,socket,datetime,random,time
count = 0

if len(sys.argv) != 2:
        print "Invalid Input"
        sys.exit(0)
else:
	hostname = sys.argv[1]
#print hostname
randomport = [n for n in range(0,65536)]
random.shuffle(randomport); #get random sequence of the ports
starttime = datetime.datetime.now()
for port in randomport:
#	time.sleep(0.05)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((hostname,port))
		print 'Port %s is open, service is %s ' % (port, socket.getservbyport(port))
		count+=1
		s.close()
	except socket.error,msg:
#		print 'pass'
		s.close()
		pass
endtime = datetime.datetime.now()
runtime = (endtime - starttime).seconds

print 'run time : %d seconds' % (runtime)
print 'number of ports found to be open: %d '% (count)
print 'scan rate : %d (ports scanned per second)' % (65536/runtime)
