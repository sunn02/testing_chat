import threading
from unittest.mock import MagicMock, patch
import pytest
from chat_server import Server  

@pytest.fixture
def mock_server():
    server = Server()

    # Simulamos la conexión de varios clientes
    with patch('socket.socket.accept', side_effect=[
        (MagicMock(), ('127.0.0.1', 1235)),
        (MagicMock(), ('127.0.0.2', 1236)),
        (MagicMock(), ('127.0.0.3', 1237))
    ]):
        server_thread = threading.Thread(target=server.start)
        server_thread.daemon = False
        server_thread.start()
        yield server
        server_thread.join() 

def test_server_accepts_connection(mock_server):
    print(f"Total connected clients: {len(mock_server.clients)}")
    assert len(mock_server.clients) > 0




    
