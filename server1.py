import socket
import select

# We use select to handle multiple connections; where our server handle many clients
# The client needs to be able to send messages to the server and then the server needs to distribute them 
# to the rest of the connected clients.

HEADER_LENGHT = 10 # We use this to distinguish each message, where one message ends and the next begins
IP = "127.0.0.1"
PORT = 8001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()


sockets_list = [server_socket] #List of sockets for select to keep track of

clients = {} #We use a dictionary where the clients sockets will be the key and then user data the value

print(f'Listening for connections on {IP}:{PORT}...')



def receive_message(client_socket):    
    try: # ---> To test a block of code for errors
        message_header = client_socket.recv(HEADER_LENGHT)
        # If a client closes a connection gracefully, then a socket.close() will be issued and there will be no header.
        if not len(message_header):
            return False
        
        message_lengh = int(message_header.decode("utf-8")).strip(()) #header to lenght
        
        return {'header': message_header, 'data': client_socket.recv(message_lengh) }
    
    except: # --> lets you to handle the error 
         # Something went wrong like empty message or client exited abruptly.
        return False

