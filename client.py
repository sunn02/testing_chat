import socket

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1235

class Client():
    def __init__(self, username):
        self.username = username
        self.client_socket = None

    def connect(self):    
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((IP, PORT))
            self.send_message(self.username.encode("utf-8"))
            print(f"Client {self.username} sent username to server.")
        except Exception as e:
            print(f"Connection Error: {e}")
            exit()

    def disconnect(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                print(f"{self.username} disconnected.")
            except Exception as e:
                print(f"Error disconnecting {self.username}: {e}")

    def send_message(self, message):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')  
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + message)
        except Exception as e:
            print(f"Sending message error: {e}")

    def receive_message(self):
        try:
            message_header = self.client_socket.recv(HEADER_LENGTH)
            if not message_header:
                print('Connection closed by the server')
                self.disconnect()  # Disconnect if the server closes the connection
                return None
            
            message_length = int(message_header.decode('utf-8'))
            message = self.client_socket.recv(message_length).decode('utf-8')
            
            return message
        except Exception as e:
            print(f"Receiving message error: {e}")
            return False

    def handle_communication(self):
        print(f'Connected as {self.username}. You can send messages.')
        while True:
            try:
                message = input(f'{self.username}: ')
                
                if message:
                    self.send_message(message)

                # Receive and print any new messages from the server
                received_message = self.receive_message()
                if received_message:
                    print(f"Server: {received_message}")
                else:
                    print("No new messages")
                    
            except KeyboardInterrupt:
                print("\nDisconnecting...")
                self.disconnect()
                break


def main():
    username = input("Username: ")
    client = Client(username)
    client.connect()
    client.handle_communication()

if __name__ == "__main__":
    main()



        
                 
    
        