import socket
import threading

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

class Server():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen()

        self.clients = []  # Lista para almacenar los sockets de los clientes
        self.running = True

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return False

            message_length = int(message_header.decode("utf-8").strip())
            message_data = client_socket.recv(message_length)

            if not message_data:
                return False
            return message_data.decode('utf-8')

        except Exception as e:
            print(f"Error receiving message: {e}")
            return False

    def broadcast_message(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print(f"Error broadcasting message: {e}")
    
    def debug_connected_clients(self):
        print(f"Connected clients: {len(self.clients)}")


    def handle_client(self, client_socket):
        self.clients.append(client_socket)
        print("New client connected.")
        try:
            while self.running:
                message_header = client_socket.recv(HEADER_LENGTH)
                if not message_header:
                    print("Client disconnected.")
                    break

                message_length = int(message_header.decode("utf-8").strip())
                message = client_socket.recv(message_length).decode("utf-8")
                print(f"Received message: {message}")
        except Exception as e:
            print(f"Error receiving message: {e}")
        finally:
            self.clients.remove(client_socket)
            client_socket.close()


    def start(self):
        print("Server started, waiting for connections...")
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                self.clients.append(client_socket)
                print(f"New connection from {client_address}")

                # Start a new thread to handle the client
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

            except Exception as e:
                print(f"Server error: {e}")
                break

    def stop(self):
        self.running = False
        self.server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    server = Server()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    input("Press Enter to stop the server...\n")
    server.stop()
