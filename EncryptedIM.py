import sys,getopt,socket,select
import hmac
from M2Crypto import m2
from M2Crypto.EVP import Cipher
from M2Crypto import util
from Crypto import Random
import os

confkey = ''
authkey = ''
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
					print 'End of File'
						
				#if message == EOF:
					sys.exit(0)
                                iv = Random.new().read(16)
                                encrypted_message = Encrypt(confkey, iv, message)
                                newhmac = hmac.new(authkey)
                                newhmac.update(encrypted_message)
                                auth = newhmac.hexdigest()
                                #print encrypted_message
                                #print auth
                                #print iv
                                sending = encrypted_message+'\n'+auth+'\n'+iv   
				csock.send(sending)
			else:
				data = r.recv(1024);
				if data =='':
					print 'End of File'
					sys.exit(0)
				received = data.split('\n')
				encrypted_message = received[0]
				auth = received[1]
				iv = received[2]	
				#print encrypted_message
				#print auth
				#print iv
				newhmac = hmac.new(authkey)
				newhmac.update(encrypted_message)
				authtest = newhmac.hexdigest()
				if authtest!= auth : 
					print 'Authentication faliure.'
					sys.exit(0)				
				decrypted_message = Decrypt(confkey, iv, encrypted_message)
				print decrypted_message
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
	while 1:
		rs,ws,es = select.select(inputs,[],[],1)
        	for r in rs:
                	if r is s:
				#server received data
                		data = s.recv(1024)
				if data == '':
					print 'End of File'
					sys.exit(0)
                                received = data.split('\n')
                                encrypted_message = received[0]
                                auth = received[1]
                                iv = received[2]
                                #print encrypted_message
                                #print auth
                                #print iv
                                newhmac = hmac.new(authkey)
                                newhmac.update(encrypted_message)
                                authtest = newhmac.hexdigest()
                                if authtest!= auth :
                                        print 'Authentication faliure.'
                                        sys.exit(0)
                                decrypted_message = Decrypt(confkey, iv, encrypted_message)
                                print decrypted_message

                	else:
				#server send data
				message = sys.stdin.readline()
				if message == '':
					print 'End of File'
					sys.exit(0)
        	            	iv = Random.new().read(16)
				encrypted_message = Encrypt(confkey, iv, message) 
				newhmac = hmac.new(authkey)
				newhmac.update(encrypted_message)
				auth = newhmac.hexdigest()
				#print encrypted_message
				#print auth
				#print iv
				sending = encrypted_message+'\n'+auth+'\n'+iv					
				s.send(sending)
				
	s.close()
	return 0

def Encrypt(confkey,iv,msg):
	cipher = Cipher(alg = 'aes_128_cbc', key = confkey,iv = iv,op =1 )
	buffer = cipher.update(msg)
	buffer += cipher.final()
	del cipher
	encrypted =''
	for i in buffer: encrypted +='%02X' %(ord(i))
	return encrypted

def Decrypt(confkey, iv, encrypted):
	encrypted = util.h2b(encrypted)
	cipher = Cipher(alg = 'aes_128_cbc', key = confkey, iv = iv, op =0)
	buffer = cipher.update(encrypted)
	buffer += cipher.final()
	del cipher
	return buffer

flag = 0	
if len(sys.argv)<5:
	print 'invalid input, please try again.'
	sys.exit(0)

if sys.argv[1]=='-s':
	if sys.argv[2] == '-confkey':
		confkey = sys.argv[3]
		if sys.argv[4] == '-authkey':
			authkey = sys.argv[5]
			flag = 1
		        server()
if sys.argv[1]=='-c':
        hostname = sys.argv[2]
	if sys.argv[3] == '-confkey':
        	confkey = sys.argv[4]
                if sys.argv[5] == '-authkey':
                        authkey = sys.argv[6]
                        flag = 1     
			client()

if flag == 0:
	print 'invalid input!'


