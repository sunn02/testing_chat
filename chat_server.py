import socket
import select

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1240 
HEADER_LENGTH = 10
MAX_MESSAGE_LENGTH = 500

# Función para recibir mensajes del cliente
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not message_header:
            return False

        message_length = int(message_header.decode("utf-8").strip())
        message_data = client_socket.recv(message_length)

        if not message_data:
            return False

        return message_data.decode('utf-8')
    except Exception as e:
        print(f"Error receiving message: {e}")
        return False


# Función para enviar mensajes al cliente
def send_message(client_socket, message):
    """
    Envía un mensaje al servidor si el socket está abierto y el mensaje no es demasiado largo.
    """
    try:
        if client_socket.fileno() == -1:
            raise OSError("Socket está cerrado")

        if len(message) > MAX_MESSAGE_LENGTH:
            raise ValueError("Mensaje demasiado largo")

        message_encoded = message.encode("utf-8")
        message_header = f"{len(message_encoded):<{HEADER_LENGTH}}".encode("utf-8")
        
        client_socket.send(message_header + message_encoded)

    except OSError as e:
        print(f"Error al enviar mensaje: {e}")
        raise  # Propagar el error para que pueda ser manejado por el cliente

    except ValueError as e:
        print(f"Error al enviar mensaje: {e}")
        raise  # Propagar el error para que pueda ser manejado por el cliente


# Función para manejar a un cliente
def handle_client(client_socket):
    """
    Maneja la comunicación con el cliente.
    """
    try:
        while True:
            message = receive_message(client_socket)
            if message is False:  # Verifica si el mensaje es False
                print("No se recibió ningún mensaje o conexión cerrada.")
                break

            print(f"Mensaje recibido: {message}")

            if message == "":  # Mensaje vacío
                print("Mensaje vacío recibido")
                client_socket.send("Error: Mensaje vacío".encode("utf-8"))
                continue

            if len(message) > MAX_MESSAGE_LENGTH:  # Mensaje demasiado largo
                print("Mensaje demasiado largo, rechazado.")
                client_socket.send("Error: Mensaje demasiado largo".encode("utf-8"))
                continue

            # Si el mensaje es válido, procesarlo
            send_message(client_socket, message)

    except Exception as e:
        print(f"Error en la conexión: {e}")
    finally:
        client_socket.close()




# Función principal del servidor
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor iniciado en {SERVER_HOST}:{SERVER_PORT}")

    # Lista de sockets a monitorear
    sockets_list = [server_socket]
    
    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                # Acepta nueva conexión
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)
                print(f"Nueva conexión desde {client_address}")
            else:
                # Maneja un mensaje de un cliente existente
                handle_client(notified_socket)
                sockets_list.remove(notified_socket)
                notified_socket.close()

if __name__ == "__main__":
    start_server()
