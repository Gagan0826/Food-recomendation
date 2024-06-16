import socket

class NotificationClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def send_notification(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            print(f'Received: {data.decode()}')