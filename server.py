import socket
import select

## We use select to handle multiple connections; where our server handle many clients
## The client needs to be able to send messages to the server and then the server needs to distribute them 
## to the rest of the connected clients.


HEADER_LENGHT = 10 
IP = "127.0.0.1"
PORT = 1234
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()


sockets_list = [server_socket] # ---> List of sockets for select to keep track of, sockets from which we expect to read
clients = {} # ---> We use a dictionary where the clients sockets will be the key and then user data the value

print(f'Listening for connections on {IP}:{PORT}')


def receive_message(client_socket):    
    try: 
        message_header = client_socket.recv(HEADER_LENGHT)
        # If we dont get any data, the client close the connection
        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        
        if message_length == 0:
            return False
        
        message_data = client_socket.recv(message_length)
        
        if not message_data:
            return False
        
        return {'header': message_header, 'data': message_data }
    
    except: 
        # Something went wrong like empty message or client exited abruptly.
        return False

def broadcast_message(message, notified_socket):
    # Iterate over connected clients and broadcast message
    for client_socket in clients:
        if client_socket != notified_socket:
            try:
                client_socket.send(message)
            except socket.error as e:
                print(f"Error sending message to {client_socket}: {e}")                                

def chat_server_loop():
    while True:
        
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = receive_message(client_socket)

                # If False - client disconnected before he sent his name
                if user is not False:
                    sockets_list.append(client_socket)
                    clients[client_socket] = user
                    
                    print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            else:
                message = receive_message(notified_socket)
                
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                    sockets_list.remove(notified_socket)

                    del clients[notified_socket] 
                    continue
                

                user = clients[notified_socket]

                print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

                
        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]
            
if __name__ == "__main__":
    chat_server_loop()