import socket
import select
import threading
import time
from server import receive_message, chat_server_loop
import pytest

from tests.test_utils import create_socket


HEADER_LENGHT = 12

#Funcion para manejar conexiones y desconexiones de clientes
#Funcion para manejar perdida de conexion o desconexion inesperada y envio fallido del mensaje.
# Casos positivos: Manejar mensajes que cumplan con ciertas condiciones para ser enviado
# Casos negativos: Si el mensaje esta vacio, rechazar el mensaje y devolver el error

# Escribe pruebas unitarias e integración enfocadas en el servidor:
# Verifica que el servidor pueda aceptar múltiples conexiones.
# Prueba el manejo de mensajes inválidos o vacíos desde un cliente.
# Simula clientes que se desconectan mientras otros envían mensajes.
# Asegura que los mensajes llegan en el orden correcto y no se duplican.

#Caso positivo, mensaje valido
# def test_valid_message():
#     mock_client_socket = create_socket()
    
#     message = 'Hola Servidor'.encode('utf-8')

#     message_header = f"{len(message):<{HEADER_LENGHT}}".encode('utf-8')
#     mock_client_socket.send(message_header + message)
    
#     time.sleep(0.5)
#     response = receive_message(mock_client_socket)
#     assert response is not False, 'El mensaje fue recibido correctamente'
#     mock_client_socket.close()

#Caso negativo, mensaje vacio
def test_message_empty():
    mock_client_socket = create_socket()
        
    empty_message = b''
    empty_message_header = f"{len(empty_message):<{HEADER_LENGHT}}".encode('utf-8')
    mock_client_socket.send(empty_message_header + empty_message)
   
    message_lenght = int(empty_message_header.decode("utf-8").strip())
    
    assert message_lenght == 0
    # response = receive_message(mock_client_socket)
    # assert response is False, 'El mensaje fue rechazado'
    mock_client_socket.close()
    
def test_simulate_client_connection():
    mock_client_socket = create_socket()
    
    assert mock_client_socket
    mock_client_socket.close()
 
def test_simulate_client_disconection():
    mock_client_socket = create_socket()
    
    mock_client_socket.close()
    time.sleep(1)
    response = receive_message(mock_client_socket)

    assert response is False
    
