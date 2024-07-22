import socket
import threading
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)
from src.business.Admin import Admin
from src.business.Chef import Chef
from src.business.Employee import Employee  
from src.data.models.UserProfile import UserProfile
from NotificationServer import NotificationServer
from src.utils.Notification import Notification
from src.handlers.AdminHandler import AdminHandler
from src.handlers.ChefHandler import ChefHandler
from src.handlers.EmployeeHandler import EmployeeHandler
HOST = 'localhost'
PORT = 8080

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                break
            process_request(client_socket, request)
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()

def process_request(client_socket, request):
    try:
        command, *params = request.split(',')
        role = params[0]
        if role == "Admin":
            AdminHandler.handle_request(client_socket, command, params[1:])
        elif role == "Chef":
            ChefHandler.handle_request(client_socket, command, params[1:])
        elif role == "Employee":
            EmployeeHandler.handle_request(client_socket, command, params[1:])
        else:
            client_socket.send("Invalid role".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error processing request: {e}".encode('utf-8'))

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main_server_thread = threading.Thread(target=start_server)
    notification_server_thread = NotificationServer()

    main_server_thread.start()
    notification_server_thread.start()

    main_server_thread.join()
    notification_server_thread.join()
