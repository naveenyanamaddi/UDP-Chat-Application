#############################################################################
# The chat server
#############################################################################

"""
UDP Chat Server to accept the connection from Chat Clients and maintain list 
of Signed In users. 
"""

#!/usr/bin/python

import os
import sys
import pickle
import socket
import signal

BUFFSIZE = 4096 #Accept 4096 bytes of data from Clients

#signal handler to handle the Keyboard interruptions
def ServerSignalHandler(SignalType, Handler):
	print 'Shutting down the Chat Server...'
	sys.exit(0)

def usage():
	print "UDP Chat Application"
	print "Usage: ChatServer.py -sp port"
	print "Examples:"
	print "Python ChatServer.py -sp 5500"
	sys.exit(0)
	
def main():
	if len(sys.argv) != 3:
		usage()

	try:	
		port = int(sys.argv[2])
	except Exception:
		print "Unhandle port defined"
		
	# we are going to create server socket to listen and 
	# accept connections from clients, and maintain list  
	# of clients
        try:
	    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    serverSocket.bind(('', port)) #bind the socket to listen on all interfaces
        except socket.error:
            print 'Error occurred... Please try again!!'
            sys.exit(1)

	print 'Server Initialized...'
	activeClientList = [] #List to maintain the active user list
        activeClientData = [] #List to maintain the active user information (IP:PORT)

	signal.signal(signal.SIGINT, ServerSignalHandler) 
	
        while True:
            try:
		clientData, clientAddress = serverSocket.recvfrom(BUFFSIZE) #Receive the connection and data from Clients	
		if clientData.find('SIGN-IN') != -1:
			username = clientData.split()[1]
			if username in activeClientList:
				serverSocket.sendto("User already exists!!", (clientAddress))
			else:
				activeClientList.append(username)
				activeClientData.append(clientAddress)	
				serverSocket.sendto("Client SIGN-IN Successful!!", (clientAddress)) #Send Successful message to Client if SIGN-IN done
                elif clientData.find('list') != -1:
			userToRemove = clientData.split()[1]
			activeListToSend = list(activeClientList)
			activeListToSend.remove(userToRemove) #Identify the User who request for list of users and Remove before Sending
			serverSocket.sendto(','.join(activeListToSend), (clientAddress))
		elif (clientData.find('MESSAGE') != -1):
			userToFetch = clientData.split()[1]
			if userToFetch in activeClientList:
				index = activeClientList.index(userToFetch) #Fetch the User Information and Send to Requested Client to deliver the MESSAGE
				serverSocket.sendto(pickle.dumps(activeClientData[index]), clientAddress)
			else:
				serverSocket.sendto("User not found!!", clientAddress)
            except socket.error:
                print 'Error has occurred... Shutting down the Chat Server!!'
                sys.exit(1)

main() #Chat execution starts from here
