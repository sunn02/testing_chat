import socket
import select
import errno # ---> We use errno to match specific error codes, try to reseive messages and if we cant we will get an error


HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 8002
my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

client_socket.setblocking(False) # ---> the receive functionality wont be blocking 

# ----------------------------------------------------------------------------------------------------------------------------

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

client_socket.send(username_header + username)


while True:
   message = input(f'{my_username}: ')
   
   # if message is not empty
   if message:
       message = message.encode('utf-8')
       message_header = f'{len(message):< {HEADER_LENGTH}}'.encode('utf-8')
       client_socket.send(message_header + message)
       
   try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                    print('Connection closed by the server')
                    break
            
            
            # Convert header to int value
            username_length = int(username_header.decode('utf-8'))

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            
            #The exact process we did with users when the client socket send a message 
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8'))
            message = client_socket.recv(message_length).decode('utf-8')
            
            
            print(f'{username} : {message}')
            
   except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            break
        continue
    
   except Exception as e:
        #any other exception - something happened, exit
        print('General Error:', str(e))
        break
        
        
        
                 
    
        