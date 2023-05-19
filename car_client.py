import socket
import service
import logging as LOG

LOG.basicConfig(format='%(asctime)s - %(message)s', level=LOG.INFO)

# Server details
server_host = 'localhost'
server_port = 8888
server_socket = None


def startServer():
    # Socket server setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    LOG.info(f"[Traffic-Client] - Socket server is up and running on port : {server_port})")
    return server_socket

def listenAndReceiveMsg(server_socket):
    while True:
        # Accept a client connection
        LOG.info("[Traffic-Client] - Listing for connection...")
        client_socket, client_address = server_socket.accept()
        LOG.info(f"[Traffic-Client] - Received connection from: {client_address}")
        client_socket.settimeout(None)
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                LOG.info("[Traffic-Client] - Client Disconnected.")
                break
            # LOG.info(f"Received data from client: {data}")
            service.handle_car(data)