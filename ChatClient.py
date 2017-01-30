#############################################################################
# The chat client
#############################################################################

"""
A UDP chat client to connect with server and talk to peer clients over UDP
Currently client can see the list of active users with 'list' command
and can send message using 'send' 
"""

#!/usr/bin/python

import os
import sys
import socket
import pickle
import signal
import threading 

BUFFSIZE = 4096 #client accept 4096 bytes of data from server and peer clients

shutdown_event = threading.Event()

# signal handle to handle the all keyboard interruptions and kill the application
def signal_handler(signalType, Frame):
        print 'Shutting down the Chat Client...'
        os._exit(1)

def usage():
	print "UDP Chat Application"
	print "python ChatClient.py -u user-name -sip server-ip -sp port"
	print "Example:"
	print "python ChatClient.py -u Naveen -sip 127.0.0.1 -sp 5500"
#wait for user input to read the commands or messages
def promptForUserInput():
        sys.stdout.write('+> ')
        sys.stdout.flush()
# Client Thread to handle the input commands and Send MESSAGE to peer Clients        
def clientCommandThread():
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creating Client Socket for handling communication with Server and Peer Clients

        while True:
            promptForUserInput()
            inputCommand = sys.stdin.readline()
            if ((inputCommand.find('list') != -1) and (inputCommand.find('send') == -1)):
                try:
                    clientSocket.sendto(inputCommand + ' ' + sys.argv[2], (sys.argv[4], int(sys.argv[6])))
		    clientSocket.settimeout(10)
                    listOfActiveUsers, serverAddress = clientSocket.recvfrom(BUFFSIZE)
                    clientSocket.settimeout(None)
                    if listOfActiveUsers:
		        print '<- Signed In Users: ' + str(listOfActiveUsers).strip('[]')
		    else:
                        print 'No Signed In Users!! Except You: ' + sys.argv[2]
                except socket.timeout:
                    print 'Request timed out!! Shutting down the Chat Client...'
	            os._exit(1)
            elif ((inputCommand.find('send') != -1) and (inputCommand.find('list') == -1)):	
	        try:
                    peerClientName = inputCommand.split()[1]	
                    isCommandValid = True #Make sure send command not accept empty inputs
                except Exception:
                    print 'Please enter valid command'
                    isCommandValid = False
                if isCommandValid:
                    try:
                        clientSocket.sendto('MESSAGE ' + peerClientName, (sys.argv[4], int(sys.argv[6])))
                        clientSocket.settimeout(10)
		        peerClientInfo, serverAddress = clientSocket.recvfrom(BUFFSIZE)
                        clientSocket.settimeout(None)
	                if "not found" in peerClientInfo:
                            print peerClientInfo
                        else:    
                            peerClientAddress = pickle.loads(peerClientInfo) 
                            messageToSend = inputCommand.split()[2:]
	                    messageToSendString = ' '.join(messageToSend) #joining the message into string format
                            clientSocket.sendto(sys.argv[2] + ' ' + messageToSendString,peerClientAddress) #send message to peer client
                    except socket.timeout:
                        print 'Request timed out!! Shutting down the Chat Client...'
                        os._exit(1)
	    else:
		print 'Command not found! Please enter valid command'

def main():
	
	if len(sys.argv) != 7:
		usage() #If input is not proper, notify the user telling correct usage of ChatClient.py
	try:
		userName   = sys.argv[2]
		serverPort = int(sys.argv[6])
	except Exception:
		print "Unhandle input entered"
		sys.exit(1)
	try:
		socket.inet_aton(sys.argv[4])
	except socket.error:
		print "Unhandle IPv4 address"
		sys.exit(1)
	serverIP = sys.argv[4]

	#create a client socket object
	try:
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#send SIGN-IN and USERNAME to server
		message = 'SIGN-IN ' + userName
		clientSocket.sendto(message, (serverIP, serverPort))
                clientSocket.settimeout(5)
                serverResponse, serverAddress = clientSocket.recvfrom(BUFFSIZE)
		clientSocket.settimeout(None)
                if serverResponse.find('Successful') == -1:
			print serverResponse
			sys.exit(1)
	except socket.timeout:
                print 'Could not connect to chat server %s @%d' % (serverIP, serverPort)
                sys.exit(1)         
        signal.signal(signal.SIGINT, signal_handler) #signal handler registration
    
        clientThread = threading.Thread(target=clientCommandThread) #Create a thread to handle the user inputs and MESSAGE 
	clientThread.start()
        while True:
                messageFromPeerClient, peerClientAddress = clientSocket.recvfrom(BUFFSIZE) #Listen for MESSAGE from peer Client
                messageFromPeer = ' '.join(messageFromPeerClient.split()[1:])
                displayMessage = '\n<- <From ' + peerClientAddress[0] + ':' + str(peerClientAddress[1]) + ':' + messageFromPeerClient.split()[0] + '>: ' + messageFromPeer
                sys.stdout.write(displayMessage + '\n') #Display the MESSAGE on screen
                promptForUserInput()

main() #Application Start from here
