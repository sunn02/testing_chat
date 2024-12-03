import socket
import threading
import time
import pytest
from .chat_server import Server

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1236
HEADER_LENGTH = 10

@pytest.fixture(scope="module")
def test_server_start():
    server = Server()
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(1)  # Give time for the server to start before the tests
    
    yield server  # Provide the server instance to the tests
    
    server.server_socket.close()  # Close the server socket after tests

def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    
    username = "testUser"
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header + username.encode('utf-8'))
    
    return client_socket

def test_multiple_connections(test_server_start):
    client1 = create_client()
    client2 = create_client()
    client3 = create_client()
    
    message1 = "Hello from client1"
    message2 = "Hello from client2"
    message3 = "Hello from client3"

    # Enviar mensajes siguiendo el protocolo
    client1.send(f"{len(message1):<{HEADER_LENGTH}}".encode('utf-8') + message1.encode('utf-8'))
    client2.send(f"{len(message2):<{HEADER_LENGTH}}".encode('utf-8') + message2.encode('utf-8'))
    client3.send(f"{len(message3):<{HEADER_LENGTH}}".encode('utf-8') + message3.encode('utf-8'))
    
    time.sleep(1)  # Dar tiempo para que los mensajes sean procesados

    # Verificar que los mensajes se retransmiten
    assert client1.recv(1024).decode('utf-8') == message2
    assert client1.recv(1024).decode('utf-8') == message3
    
    assert client2.recv(1024).decode('utf-8') == message1
    assert client2.recv(1024).decode('utf-8') == message3
    
    assert client3.recv(1024).decode('utf-8') == message1
    assert client3.recv(1024).decode('utf-8') == message2

    client1.close()
    client2.close()
    client3.close()


def test_client_disconnection(test_server_start):
    server = test_server_start
    
    client1 = create_client()
    client2 = create_client()
    
    client1.send(b"Message from client1")
    time.sleep(1)
    client1.close()  # Close client1
    
    assert client2.recv(1024) == b"Message from client1"
    
    client2.close()

def test_broadcast_message(test_server_start):
    server = test_server_start
    
    client1 = create_client()
    client2 = create_client()
    
    client1.send(b"Broadcast message")
    
    assert client1.recv(1024) == b"Broadcast message"
    assert client2.recv(1024) == b"Broadcast message"
    
    client1.close()
    client2.close()

