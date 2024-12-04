import socket
import threading
import time
import pytest

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1236
HEADER_LENGTH = 10


def create_client():
    """
    Crea un cliente y lo conecta al servidor.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    return client_socket


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
            return None
        message_length = int(message_header.decode("utf-8").strip())
        return client_socket.recv(message_length).decode("utf-8")
    except Exception as e:
        print(f"Error receiving message: {e}")
        return None


def test_valid_message():
    """
    Prueba el envío de un mensaje válido.
    """
    client_socket = create_client()
    message = "Hola Servidor"
    send_message(client_socket, message)

    time.sleep(0.5)
    response = receive_message(client_socket)

    assert response == message, "El mensaje válido no fue recibido correctamente."
    client_socket.close()


def test_empty_message():
    """
    Prueba el envío de un mensaje vacío.
    """
    client_socket = create_client()
    send_message(client_socket, "")

    time.sleep(0.5)
    response = receive_message(client_socket)

    assert response is None, "El mensaje vacío no debería ser aceptado."
    client_socket.close()


def test_long_message():
    """
    Prueba el envío de un mensaje demasiado largo.
    """
    client_socket = create_client()
    long_message = "A" * 1000  # Mensaje muy largo
    send_message(client_socket, long_message)

    time.sleep(0.5)
    response = receive_message(client_socket)

    assert response is None, "El mensaje demasiado largo no debería ser aceptado."
    client_socket.close()


def test_connection_loss():
    """
    Prueba la pérdida de conexión del cliente.
    """
    client_socket = create_client()
    client_socket.close()  # Cerramos el socket

    try:
        send_message(client_socket, "Hola después de desconexión")
        assert False, "No se debería enviar un mensaje después de la desconexión."
    except Exception as e:
        assert "Socket is closed" in str(e), "El servidor maneja correctamente la pérdida de conexión."
