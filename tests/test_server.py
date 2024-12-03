import threading
import time
from server import Server
from client import Client


def test_clients_connections():
    server = Server()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    time.sleep(1)  # Give server time to start

    cliente1 = Client("User1")
    cliente2 = Client("User2")

    # Connect the clients
    cliente1.connect()
    cliente2.connect()

    # Wait for connections to be established
    start_time = time.time()
    while server.debug_connected_clients() < 2:
        if time.time() - start_time > 10:  # Timeout
            server.stop()
            raise AssertionError("Server couldn't handle multiple connections within the expected time.")

    print("All clients connected successfully.")

    cliente1.disconnect()
    cliente2.disconnect()
    server.stop()


    
