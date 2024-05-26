import socket
import threading
import json
from concurrent.futures import ThreadPoolExecutor

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received from {addr}: {data.decode()}")
        client_socket.sendall(data)

    client_socket.close()
    print(f"Connection from {addr} closed")

def start_server():
    # Чтение конфигурации из JSON файла
    with open('config.json', 'r') as f:
        config = json.load(f)

    address = config['address']
    port = config['port']

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(5)
    print(f"Server started on {address}:{port}")

    # Использование пула потоков с максимум 10 потоками
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            client_socket, addr = server_socket.accept()
            executor.submit(handle_client, client_socket, addr)

if __name__ == "__main__":
    start_server()
