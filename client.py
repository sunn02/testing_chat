import socket

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1238

def connect(username):
    """
    Establece una conexión con el servidor y envía el nombre de usuario.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        send_message(client_socket, username.encode("utf-8"))
        print(f"Client {username} sent username to server.")
        return client_socket
    except Exception as e:
        print(f"Connection Error: {e}")
        exit()

def disconnect(client_socket, username):
    """
    Desconecta el cliente del servidor.
    """
    if client_socket:
        try:
            client_socket.close()
            print(f"{username} disconnected.")
        except Exception as e:
            print(f"Error disconnecting {username}: {e}")

def send_message(client_socket, message):
    """
    Envía un mensaje al servidor.
    """
    message_encoded = message.encode("utf-8")
    message_header = f"{len(message_encoded):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message_encoded)


def receive_message(client_socket):
    """
    Recibe un mensaje del servidor.
    """
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not message_header:
            print('Connection closed by the server')
            disconnect(client_socket, "Unknown")  # Desconectar si el servidor cierra la conexión
            return None

        message_length = int(message_header.decode('utf-8'))
        message = client_socket.recv(message_length).decode('utf-8')

        return message
    except Exception as e:
        print(f"Receiving message error: {e}")
        return False

def handle_communication(username, client_socket):
    """
    Maneja la comunicación con el servidor: envío y recepción de mensajes.
    """
    print(f'Connected as {username}. You can send messages.')
    while True:
        try:
            message = input(f'{username}: ')
            
            if message:
                send_message(client_socket, message)

            # Recibe y muestra cualquier nuevo mensaje del servidor
            received_message = receive_message(client_socket)
            if received_message:
                print(f"Server: {received_message}")
            else:
                print("No new messages")
                
        except KeyboardInterrupt:
            print("\nDisconnecting...")
            disconnect(client_socket, username)
            break

def main():
    """
    Función principal del cliente.
    """
    username = input("Username: ")
    client_socket = connect(username)
    handle_communication(username, client_socket)

if __name__ == "__main__":
    main()

        
                 
    
        