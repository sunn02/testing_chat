import socket

# class socket.socket(family=AF_INET, type=SOCK_STREAM)
# The arguments passed to socket() are constants used to specify the address family and socket type.
#   ---> AF_INET is the Internet address family for IPv4. 
#   ---> SOCK_STREAM is the socket type for TCP, the protocol that will be used to transport messages in the network.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The .bind() method is used to associate the socket with a specific network interface and port number:
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    clientsocket, adress = s.accept()
    # adress = where are they coming from, the IP adress
    print(f"Connection from {adress} has been stablished")
    clientsocket.send(bytes("Welcome to the server", "utf-8"))