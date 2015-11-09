import sys,getopt,socket,select
def server():
  server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	port=9999
	server.bind(('',port))
	server.listen(5)
	csock,caddr = server.accept()## new socket for client
	inputs=[server,csock,sys.stdin]
	while 1:
		rs,ws,es=select.select(inputs,[],[],1)
		for r in rs:
			if r is server:
        		        clientsock,clientaddr=r.accept()
               			inputs.append(clientsock)
			if r is sys.stdin:
                		message = sys.stdin.readline()
              			if message == '':
					print "End of File"
					sys.exit(0)
		  		csock.send(message)
			else:
				data=r.recv(1024);
				if data =='':
					print 'Receiving End of File'
					sys.exit(0)
				print data
	server.close()
	clientsock.close()
	csock.close()
	return 0


def client():
	port=9999
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((hostname,port))
	# whether the system input or from the client
	inputs=[s,sys.stdin]
	#no select
	#message = raw_input()
        #s.send(message)  
        #data = s.recv(512)
        #if data:       
        #       print data
	while 1:
		rs,ws,es = select.select(inputs,[],[],1)
        	for r in rs:
                	if r is s:
					#server received data
                		data = s.recv(1024)
				if data == '':
					print 'Receiving End of File'
					sys.exit(0)
                    		print data

                	else:
					#server send data
				message = sys.stdin.readline()
				if message =='':
					print'End of File'
					sys.exit(0)
        	            	s.send(message)

	s.close()
	return 0
	
if len(sys.argv)>2:
        hostname = sys.argv[2]
if sys.argv[1]=='-s':
        server()
if sys.argv[1]=='-c':
        client()
