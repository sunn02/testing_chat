# Crea pruebas unitarias utilizando la herramienta elegida según el lenguaje de
# programación utilizado

# - Gestión de las conexiones de los clientes: Verificar que los clientes se conectan correctamente al servidor y que se gestionan de manera adecuada cuando se desconectan.
# - Manejo de errores: Asegurar que los errores comunes, como la **pérdida de conexión** o el **envío fallido de un mensaje, se gestionen de manera adecuada.**

# **Las pruebas unitarias deben abordar tanto los casos positivos como los negativos.** 

# - Casos Positivos (happy path): Verificar que el sistema funcione
# correctamente bajo condiciones ideales. Por ejemplo, cuando se envía
# un mensaje válido, este debe ser aceptado y procesado sin problemas.
# - Casos Negativos: Probar escenarios en los que el sistema debería
# manejar entradas incorrectas o condiciones excepcionales. Por ejemplo,
# si se intenta enviar un mensaje vacío o demasiado largo, el sistema debe
# rechazarlo y devolver un error.
# - Cobertura Completa: Cada prueba debe enfocarse en un
# comportamiento específico. Al escribir pruebas unitarias, asegúrate de
# cubrir todas las posibles rutas de ejecución en la función, incluyendo los
# posibles errores.


import socket
import time
import pytest

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


# Caso positivo: mensaje válido
def test_valid_message():
    mock_client_socket = create_client()
    
    message = 'Hola Servidor'.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')

    mock_client_socket.send(message_header + message)
    
    time.sleep(0.5)
    response = receive_message(mock_client_socket)
    
    assert response is not False, 'El mensaje fue recibido correctamente'
    mock_client_socket.close()


# Caso negativo: mensaje vacío
def test_message_empty():
    mock_client_socket = create_client()
    
    empty_message = b''
    empty_message_header = f"{len(empty_message):<{HEADER_LENGTH}}".encode('utf-8')

    mock_client_socket.send(empty_message_header + empty_message)

    message_length = int(empty_message_header.decode("utf-8").strip())
    assert message_length == 0, 'La longitud del mensaje debe ser 0'
    
    response = receive_message(mock_client_socket)
    assert response is False, 'El mensaje vacío debe ser rechazado'
    mock_client_socket.close()


# Caso negativo: mensaje demasiado largo
def test_message_too_long():
    mock_client_socket = create_client()

    long_message = 'A' * 1000  # Suponiendo que 1000 es demasiado largo
    long_message = long_message.encode('utf-8')

    long_message_header = f"{len(long_message):<{HEADER_LENGTH}}".encode('utf-8')

    mock_client_socket.send(long_message_header + long_message)

    time.sleep(0.5)

    response = receive_message(mock_client_socket)
    assert response is False, 'El mensaje demasiado largo debe ser rechazado'
    mock_client_socket.close()


# Caso negativo: pérdida de conexión
def test_connection_loss():
    mock_client_socket = create_socket()

    # Enviar un mensaje después de la desconexión
    mock_client_socket.close()  # Cerramos la conexión
    
    try:
        mock_client_socket.send(b'Hola')
    except Exception as e:
        assert str(e) == 'Socket is closed', 'El servidor debe manejar la pérdida de conexión'

