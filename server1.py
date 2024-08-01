import socket
import select

## We use select to handle multiple connections; where our server handle many clients
## The client needs to be able to send messages to the server and then the server needs to distribute them 
## to the rest of the connected clients.

# ----------------------------------------------------------------------------------------------------------------------------

HEADER_LENGHT = 10 # ---> We use this to distinguish each message, where one message ends and the next begins
IP = "127.0.0.1"
PORT = 8001
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen()

# ----------------------------------------------------------------------------------------------------------------------------

sockets_list = [server_socket] # ---> List of sockets for select to keep track of, sockets from which we expect to read

clients = {} # ---> We use a dictionary where the clients sockets will be the key and then user data the value

print(f'Listening for connections on {IP}:{PORT}')

# ----------------------------------------------------------------------------------------------------------------------------

## The server's main job is to receive messages, and then disperse 
## them to the connected clients. 
## For receiving messages, we're going to make a function:

def receive_message(client_socket):    

# First Step for receiving a message is to read the header:

    try: # ---> To test a block of code for errors

        message_header = client_socket.recv(HEADER_LENGHT)

        # If a client closes a connection gracefully, then a socket.close() will be issued and there will be no header.
        if not len(message_header):
            return False
        
        message_lengh = int(message_header.decode("utf-8")).strip(()) # ---> Header to lenght
        
        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_lengh) }
    
    except: # --> lets you to handle the error 

        # Something went wrong like empty message or client exited abruptly.
        return False

# ----------------------------------------------------------------------------------------------------------------------------

# To receive messages for all of our client sockets and
# then send all of the messages out to all of the client sockets. 
# We need a loop

while True:
    # < -- select.select(rlist, wlist, xlist)--->
    #   This is a straightforward interface to the Unix select() system call. 
    #   The first three arguments are iterables of ‘waitable objects
    #   - rlist - sockets to be monitored for incoming data, 'wait' until ready for reading
    #   - wlist - sockets for data to be send to, 'wait' until ready for writing
    #     (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            client_socket, client_address = server_socket.accept()

            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

# ----------------------------------------------------------------------------------------------------------------------------

        # Else existing socket is sending a message
        else:
            message = receive_message(notified_socket)


            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # But don't sent it to sender
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
