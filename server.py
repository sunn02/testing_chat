import socket

# class socket.socket(family=AF_INET, type=SOCK_STREAM)
# The arguments passed to socket() are constants used to specify the address family and socket type.
#   ---> AF_INET is the Internet address family for IPv4. 
#   ---> SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport messages
#   in the network.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# A socket will be tied to some port on some host, in case of a server we bind the socket
# to some port of the server (localhost)
# The .bind() method is used to associate the socket with a specific network interface and port number
s.bind((socket.gethostname(),  8000))

s.listen(5) 
# queue of five connections

while True:
    clientsocket, adress = s.accept()
    # ---> adress = where the client is coming from, the IP adress

    print(f"Connection from {adress} has been stablished")
    
    # In this part we want to send messages or data to our client

    clientsocket.send(bytes("Welcome to the server", "utf-8")) 
    
    # clientsocket.close()
    # We can use .close() on a socket to close it if we wish. We can do this either on the server, or on the client or both. 
    # It's probably a good idea to be prepared for either connection to drop or be closed for whatever reason