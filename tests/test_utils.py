import socket

HEADER_LENGHT = 10


def create_socket():
    mock_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mock_client_socket.connect(("127.0.0.1", 1234))
    
    username = "testUser"
    username_header = f"{len(username):<{HEADER_LENGHT}}".encode('utf-8')
    mock_client_socket.send(username_header + username.encode('utf-8'))
    
    return mock_client_socket


def create_server():
    mock_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    mock_server_socket.bind(("127.0.0.1", 1234))
    
    return mock_server_socket