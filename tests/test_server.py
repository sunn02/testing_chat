import socket
import select
from threading import Thread
import time
from server import receive_message, chat_server_loop, verify_message
import pytest

from tests.test_utils import create_socket


HEADER_LENGHT = 10

#Funcion para manejar conexiones y desconexiones de clientes
#Funcion para manejar perdida de conexion o desconexion inesperada y envio fallido del mensaje.
# Casos positivos: Manejar mensajes que cumplan con ciertas condiciones para ser enviado
# Casos negativos: Si el mensaje esta vacio, rechazar el mensaje y devolver el error
def run_server():
    chat_server_loop()

def test_simulate_client_connection():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    mock_client_socket = create_socket()
    assert mock_client_socket
    mock_client_socket.close()

def test_message_empty():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    mock_client_socket = create_socket()
        
    empty_message = b''
    empty_message_header = f"{len(empty_message):<{HEADER_LENGHT}}".encode('utf-8')
    mock_client_socket.send(empty_message_header + empty_message)
   
    # message_lenght = int(empty_message_header.decode("utf-8").strip())
    # assert message_lenght != 0
    
    result = receive_message(mock_client_socket)
    
    assert result is False    
    mock_client_socket.close()
 
def test_simulate_client_disconection():
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    mock_client_socket = create_socket()
    
    mock_client_socket.close()
    time.sleep(1)
    response = receive_message(mock_client_socket)

    assert response is False
    
