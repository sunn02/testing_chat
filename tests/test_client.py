
# Manejar errores como la desconexion repentina del servidor, como mostrar un mensaje o reconectar
# Recibir los mensajes de error en caso de que el serviodr rechaze el mensaje debido a ciertas validaciones si 
# esta vacio o es muy largo

# Mejorar la funcion de validar si el mensaje esta vacio aplicano TDD

import socket
import time
from unittest.mock import patch
from client import handle_communication, setup_connection
import pytest

from tests.test_utils import create_server

HEADER_LENGHT = 10


def test_input():
    with patch('builtins.input', return_value="TestUser"):
        username = input()
        assert username == "TestUser"

def test_server_disconection():
    mock_server_socket = create_server()
    mock_server_socket.listen(1)
    
    try: 
        client_socket = setup_connection()
        username = 'TestUser'
        
        server_connection, _ = mock_server_socket.accept()
        mock_server_socket.close()
        time.sleep(1)
        
        response = handle_communication(client_socket, username)
        assert response is False
        
        print("Servidor desconectado")
    except:
        print('Error en el test')
    finally:
        client_socket.close()

def test_empty_message():
    mock_server_socket = create_server()
    mock_server_socket.listen(1)
    
    try: 
        client_socket = setup_connection()
        username = 'TestUser'
        
        server_connection, _ = mock_server_socket.accept()
        
        
        empty_message = b''
        empty_message_header = f"{len(empty_message):<{HEADER_LENGHT}}".encode('utf-8')
        client_socket.send(empty_message_header + empty_message)
        
        # message_lenght = int(empty_message_header.decode("utf-8").strip())
        response = handle_communication()
        
    except:
        print('Error en el test')
        
