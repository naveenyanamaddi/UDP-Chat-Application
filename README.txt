Basic Chat Application running UDP sockets

VERSION=python 2.7.12

QUICKSTART:

Server:
	python chatServer.py -sp <port>

Client:
	python chatClient.py -u <username> -sip <server ip> -sp <server portnumber>
	
Documentation:

Server:

Server accepts three types of packets
SIGN-IN -> To accept the client sign-in and maintain the active sign-in users
LIST -> To send the current active users 
MESSAGE -> Server receives the MESSAGE packet and send back peer client information to the requested client

Client:

Sample Usage of Commands 
	+> Prompt message from user
	+> list -> Requests list of signed in users at server
	<– Signed In Users: User1, User2 -> Displays list of signed in users
	+> send User1 Hello this is User1. Sends User1 "Hello this is User1”
	<– <From IP:PORT:User1>: Hi User1!
	+>