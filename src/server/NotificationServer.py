import threading
import socket
from src.utils.Notification import Notification
from src.Values.Values import *
class NotificationServer(threading.Thread):
    def __init__(self, host=HOST, port=NOTIFICATION_SERVER_PORT):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f'Notification Server listening on {self.host}:{self.port}')
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    print(f'Connected by {addr}')
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        Notification.send(data.decode())
                        conn.sendall(b'Notification received')