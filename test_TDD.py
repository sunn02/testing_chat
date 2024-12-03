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
import socket
import threading
from .chat_server import Server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1236
HEADER_LENGTH = 10


def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    username = "testUser"
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username.encode('utf-8'))
    
    return client_socket

def test_message_empty():
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    mock_client_socket = create_client()
    
    empty_message = b''
    empty_message_header = f"{len(empty_message):<{HEADER_LENGTH}}".encode('utf-8')

    mock_client_socket.send(empty_message_header + empty_message)

    message_length = int(empty_message_header.decode("utf-8").strip())
    assert message_length == 0, 'La longitud del mensaje debe ser 0'
    
    response = server.receive_message(mock_client_socket)
    assert response is False, 'El mensaje vacío debe ser rechazado'
    mock_client_socket.close()

def test_message_empty():
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
    mock_client_socket = create_client()
    
    empty_message = b''
    empty_message_header = f"{len(empty_message):<{HEADER_LENGTH}}".encode('utf-8')

    mock_client_socket.send(empty_message_header + empty_message)

    message_length = int(empty_message_header.decode("utf-8").strip())
    assert message_length == 0, 'La longitud del mensaje debe ser 0'
    
    response = server.receive_message(mock_client_socket)
    assert response is False, 'El mensaje vacío debe ser rechazado'
    mock_client_socket.close()

