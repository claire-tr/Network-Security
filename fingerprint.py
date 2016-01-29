from __future__ import division
import sys, pcap, dpkt,mlpy
import numpy as np
def train():
	
	websitename = ['google','facebook','youtube','yahoo','baidu','wikipedia','amazon','twitter','taobao','qq','google_in','live','linkedin','sina','weibo','yahoo_jp','tmall','google_jp','ebay','t','blogspot','google_de','yandex','hao123','bing']
	classlabel = []
	example_count = 0
	for i in range(0,25):
		for j in range(1,11):
			incomingcount = 0
			outgoingcount = 0
			avg_len_incoming = 0
			avg_len_outgoing = 0
			avg_space_in = 0
			avg_space_out = 0
			pre_time = 0
			incoming = False
			outgoing = False	
			filename = '%s%d'%(websitename[i]+'_',j)
			pc = pcap.pcap(filename)
			for ptime,pdata in pc:
				p = dpkt.ethernet.Ethernet(pdata)
				ip = p.data
				tcp = ip.data
				sport = tcp.sport
				dport = tcp.dport
				if sport==443:
					outgoingcount += 1
					avg_len_outgoing += len(tcp.data)
					if(outgoing):
						avg_space_out += ptime-pre_time
					else:
						pre_time = 0
					pre_time = ptime
					out = True
					incoming = False
				if dport == 443:
					incomingcount += 1
		                	avg_len_incoming += len(tcp.data)
                                        avg_len_outgoing += len(tcp.data)
                                        if(incoming):
                                                avg_space_out += ptime-pre_time
                                        else:
                                                pre_time = 0
                                        pre_time = ptime
                                        out = False
                                        incoming = True
#			print incomingcount
#			print avg_len_outgoing 
			if(incomingcount != 0 and outgoingcount!=0):
				#avg_space_out = avg_space_out/outgoingcount
				#avg_space_in = avg_space_in/incomingcount
				avg_len_incoming = avg_len_incoming/incomingcount
				avg_len_outgoing = avg_len_outgoing/outgoingcount
			elif(outgoingcount!=0):
                                #avg_space_out = avg_space_out/outgoingcount
                                avg_space_in = 0
                                avg_len_incoming = 0
                                avg_len_outgoing = avg_len_ougoing/outgoingcount
			elif(incomingcount!= 0):
                                avg_space_out = 0
                                #avg_space_in = avg_space_in/incomingcount
                                avg_len_incoming = avg_len_incoming/incomingcount
                                avg_len_outgoing = 0
			else:
                                avg_space_out = 0
                                avg_space_in = 0
                                avg_len_incoming = 0
                                avg_len_outgoing = 0

			temp = [incomingcount,outgoingcount,avg_len_incoming,avg_len_outgoing, avg_space_out]

			trainset[example_count] = temp
			classlabel.append(i+1)
			example_count += 1
	a = np.array(trainset)
	a /= np.max(np.abs(a),axis=0)
	b = np.array(classlabel)
	knn.compute(a,b)
#	knn.compute(a,b)
#	print a
#	print trainset 
#	print a.max(0)
#	print a.min(0)
	return 0
def predict(filename):
	correct = 0
	wrong = 0
        websitename = ['google','facebook','youtube','yahoo','baidu','wikipedia','amazon','twitter','taobao','qq','google_in','live','linkedin','sina','weibo','yahoo_jp','tmall','google_jp','ebay','t','blogspot','google_de','yandex','hao123','bing']
	incomingcount = 0
	outgoingcount = 0
        avg_len_incoming = 0
        avg_len_outgoing = 0
        avg_space_in = 0
        avg_space_out = 0
        pre_time = 0
        incoming = False
        outgoing = False
        pc = pcap.pcap(filename)
        for ptime,pdata in pc:
        	p = dpkt.ethernet.Ethernet(pdata)
		ip = p.data
                tcp = ip.data
                sport = tcp.sport
                dport = tcp.dport
                if sport == 443:
                	outgoingcount += 1
                        avg_len_outgoing += len(tcp.data)
                        if(outgoing):
                        	avg_space_out += ptime-pre_time
                        else:
                                pre_time = 0
                        pre_time = ptime
                        out = True
                        incoming = False
		if dport == 443:
			incomingcount += 1
                        avg_len_incoming += len(tcp.data)
                        avg_len_outgoing += len(tcp.data)
                        if(incoming):
                                 avg_space_out += ptime-pre_time
                        else:
                                 pre_time = 0
                        pre_time = ptime
                        out = False
                        incoming = True
	if (incomingcount != 0 and outgoingcount != 0):
                                #avg_space_out = avg_space_out/outgoingcount
                                #avg_space_in = avg_space_in/incomingcount
	        avg_len_incoming = avg_len_incoming/incomingcount
                avg_len_outgoing = avg_len_outgoing/outgoingcount
        elif (outgoingcount != 0):
                                #avg_space_out = avg_space_out/outgoingcount
                avg_space_in = 0
                avg_len_incoming = 0
                avg_len_outgoing = avg_len_ougoing/outgoingcount
        elif (incomingcount!= 0):
                avg_space_out = 0
                                #avg_space_in = avg_space_in/incomingcount
                avg_len_incoming = avg_len_incoming/incomingcount
                avg_len_outgoing = 0
        else:
                avg_space_out = 0
                avg_space_in = 0
                avg_len_incoming = 0
                avg_len_outgoing = 0
        temp = [incomingcount,outgoingcount,avg_len_incoming,avg_len_outgoing, avg_space_out]         
	a = np.array(trainset)
	b = a.max(0)
	for i in range(0,5):
		temp[i] = temp[i]/b[i]
	test = np.array(temp)
	print websitename[knn.predict(test)-1]
	return 0

filename = sys.argv[1]
trainset = [[] for i in range(250)]
knn = mlpy.Knn(k=10)
train()
predict(filename)
