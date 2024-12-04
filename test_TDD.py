# Implementaremos la validación de mensajes para que no se
# envíen mensajes vacíos

# • Red (Escribir la Prueba y Verla Fallar): Primero, escribe la prueba para
# este comportamiento, sabiendo que aún no has implementado la
# funcionalidad. El objetivo aquí es que la prueba falle inicialmente.
# • Green (Escribir el Código para Hacer que la Prueba Pase): Ahora que la
# prueba falla (como se esperaba), escribe el código mínimo para hacerla
# pasar. Aquí no te preocupes por optimizar o hacerlo perfecto, solo busca
# que la prueba pase.
# • Refactor (Optimizar el Código): Con la prueba ahora pasando, revisa tu
# código para mejorarlo. Este es el momento de aplicar principios como
# DRY (Don't Repeat Yourself) y clean code para optimizar la solución sin
# alterar su funcionalidad.
import pytest
import socket
import time
import threading

HEADER_LENGTH = 10
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1240  



def create_socket():
    """
    Crea y conecta un cliente al servidor.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    return client_socket

def start_server():
    """
    Inicia el servidor en un hilo separado.
    """
    from .chat_server import start_server  

    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    return server_thread

# Caso positivo: mensaje válido
def test_valid_message():
    """
    Test para el envío de un mensaje válido al servidor.
    """
    server_thread = start_server()
    
    time.sleep(1)

    mock_client_socket = create_socket()

    message = 'Hola Servidor'.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    mock_client_socket.send(message_header + message)

    # Espera y recibe la respuesta
    time.sleep(0.5)
    response = receive_message(mock_client_socket)

    # Verifica que el mensaje sea recibido correctamente
    assert response == 'Hola Servidor', 'El mensaje no fue recibido correctamente'
    mock_client_socket.close()

    # Espera que el hilo del servidor termine
    server_thread.join()

# Caso negativo: mensaje vacío
def test_message_empty():
    """
    Test para el envío de un mensaje vacío al servidor.
    """
    server_thread = start_server()
    
    time.sleep(1)

    mock_client_socket = create_socket()

    # Enviar mensaje vacío
    empty_message = ''.encode('utf-8')
    empty_message_header = f"{len(empty_message):<{HEADER_LENGTH}}".encode('utf-8')
    mock_client_socket.send(empty_message_header + empty_message)

    # Espera y recibe la respuesta
    time.sleep(0.5)
    response = receive_message(mock_client_socket)

    # Verifica que el servidor maneja correctamente el mensaje vacío
    assert response is None, 'El servidor no manejó el mensaje vacío correctamente'
    mock_client_socket.close()

    # Espera que el hilo del servidor termine
    server_thread.join()


def receive_message(client_socket):
    """
    Recibe un mensaje del servidor en un cliente.
    """
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not message_header:
            print('Connection closed by the server')
            client_socket.close()  # Desconectar si el servidor cierra la conexión
            return None

        message_length = int(message_header.decode('utf-8'))
        message = client_socket.recv(message_length).decode('utf-8')

        return message
    except Exception as e:
        print(f"Receiving message error: {e}")
        return None
