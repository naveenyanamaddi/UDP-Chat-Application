# UDP-Chat-Application

Implemented UDP client-server chat application in Python. All communications will usee UDP sockets. When started, the server should listen on a UDP port specified as an argument to the program (-sp port). When started, a client sends a SIGN-IN message to the server including a USERNAME. The IP address and port of the server should be given as arguments to the client program (-sip server-ip -sp port). On receiving the SIGN-IN message from a client, the server will record important information about the client for enabling future communications between multiple clients (e.g., username, IP address, port).

The client program should support two user commands:

  list
  send USERNAME MESSAGE
the 'list' command should display all the users currently signed into the system. The 'send' command sends the user USERNAME a message, MESSAGE.

Additional Constraints: the messages should be directly sent to the clients and not transit through the server. This means that when executing the send command, the client should first retrieve the IP address and port of the destination USERNAME and use this information to directly send the message.

In order to make your design scalable, your design should support a way to allow the server to systematically distinguish between received messages/commands. There are at least three types of packets SIGN-IN, LIST, and MESSAGE. Make sure that you are able to distinguish between them in an elegant and scalable way. You might want to consider python's pickle serialization, json, or bytearrays to achieve this.

A sample run of your application works as follows:

server$ python ChatServer.py -sp 9090 runs the server on port 9090
Server Initialized... Server is left running
user1$ python ChatClient.py -u Alice -sip server-ip -sp 9090 runs the client and signs in with username Alice.
+> Prompt message from user
+> list Requests list of signed in users at server
<– Signed In Users: Bob, Carole Displays list of signed in users
+> send Carole Hello this is Alice. Sends Carole "Hello this is Alice"
<– <From IP:PORT:Carole>: Hi Alice! How are you The client also displays received messages.
+>

