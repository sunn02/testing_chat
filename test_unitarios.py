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

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1236
HEADER_LENGTH = 10
MAX_MESSAGE_LENGTH = 50


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


def test_message_too_long():
    """
    Prueba que el servidor rechaza mensajes que son demasiado largos.
    """
    client_socket = create_client()

    long_message = "A" * (MAX_MESSAGE_LENGTH + 1)  # Mensaje más largo que el permitido
    try:
        send_message(client_socket, long_message)
        assert False, "No se debería enviar un mensaje demasiado largo."
    except ValueError as e:
        assert "Mensaje demasiado largo" in str(e), f"El servidor maneja correctamente el mensaje largo: {str(e)}"



def test_connection_loss():
    """
    Prueba la pérdida de conexión del cliente.
    """
    client_socket = create_client()
    client_socket.close()  # Cerramos el socket

    try:
        send_message(client_socket, "Hola después de desconexión")
        assert False, "No se debería enviar un mensaje después de la desconexión."
    except OSError as e:
        assert "Se intentó realizar una operación en un elemento que no es un socket" in str(e), f"El servidor maneja correctamente la pérdida de conexión: {str(e)}"
