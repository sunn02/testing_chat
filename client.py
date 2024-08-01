import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Here we connect the socket to the server on the same port that the server-side code
s.connect((socket.gethostname(),8000)) 

# We recieved the message from the server, in a -buffer- size of 1024 bytes at a time
message = s.recv(1024)
print(message.decode('utf-8'))