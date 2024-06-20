import socket
import threading
from Admin import Admin
from Chef import Chef
from Employee import Employee
from Notification import Notification
from FeedbackAnalyzer import FeedbackAnalyzer

HOST = '127.0.0.1'
PORT = 8080
NOTIFICATION_PORT = 5050

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
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
        if command == "LOGIN":
            user_type, user_id, name = params
            if user_type == "Admin":
                user = Admin(user_id, name)
            elif user_type == "Chef":
                user = Chef(user_id, name)
            elif user_type == "Employee":
                user = Employee(user_id, name)
            else:
                client_socket.send("Invalid user type".encode('utf-8'))
                return
            
            if user.login():
                client_socket.send("Login successful".encode('utf-8'))
            else:
                client_socket.send("Invalid credentials".encode('utf-8'))
        elif command == "ADD_MENU_ITEM":
            admin = Admin(user_id=params[0], name=params[1])
            admin.add_menu_item(params[2], float(params[3]), params[4])
            client_socket.send("Menu item added successfully".encode('utf-8'))

        elif command == "UPDATE_MENU_ITEM":
            admin = Admin(user_id=params[0], name=params[1])
            admin.update_menu_item(int(params[2]), float(params[3]), params[4])
            client_socket.send("Menu item updated successfully".encode('utf-8'))

        elif command == "DELETE_MENU_ITEM":
            admin = Admin(user_id=params[0], name=params[1])
            response = admin.delete_menu_item(int(params[2]))
            client_socket.send(response.encode('utf-8'))

        elif command == "GIVE_FEEDBACK":
            employee = Employee(user_id=params[0], name=params[1])
            item_id = int(params[2])
            comment = params[3]
            rating = params[4]
            date = params[5]
            employee.give_feedback(item_id,comment,rating,date)
            client_socket.send("Feedback given successfully".encode('utf-8'))

        elif command == "VIEW_MENU":
            admin = Admin(user_id=params[0], name=params[1])
            menu = admin.view_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))

        elif command == "SEND_NOTIFICATION":
            notification_message = params[0]
            Notification.send(notification_message)
            client_socket.send("Notification sent successfully".encode('utf-8'))

        elif command == "RECEIVE_NOTIFICATION":
            notifications = Notification.receive()
            client_socket.send("\n".join(notifications).encode('utf-8'))

        elif command == "VIEW_FEEDBACK":
            chef = Chef(user_id=params[0], name=params[1])
            item_id = int(params[2])
            feedback = chef.view_feedback(item_id)
            overall_rating = chef.get_overall_rating(item_id)
            response = "\n".join([f"Comment: {f[0]}, Rating: {f[1]}" for f in feedback])
            response += f"\nOverall Rating: {overall_rating}"
            client_socket.send(response.encode('utf-8'))

        elif command == "VIEW_RECOMMENDATION_MENU":
            chef = Chef(user_id=params[0], name=params[1])
            menu = chef.view_recomendation_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))

        elif command == "VIEW_ORDERED_ITEMS":
            chef = Chef(user_id=params[0], name=params[1])
            menu = chef.view_ordered_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))

        elif command == "CHOOSE_MEAL":
            employee = Employee(user_id=params[0], name=params[1])
            date = params[2]
            item_id = int(params[3])
            user_id = params[0]
            employee.choose_meal(date, item_id, user_id)
            client_socket.send("Meal chosen successfully".encode('utf-8'))

        elif command == "RECOMMEND_TOP_ITEMS":
            feedbackAnalyzer=FeedbackAnalyzer()
            feedbackAnalyzer.recommend_top_items()
            client_socket.send("Top items recommended successfully".encode('utf-8'))

        elif command == "VIEW_RECOMMENDED_ITEMS":
            chef = Chef(user_id=params[0], name=params[1])
            recommended_items = chef.view_generated_recommended_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Score: {item[3]:.2f}" for item in recommended_items])
            client_socket.send(response.encode('utf-8'))

        elif command == "GENERATE_REPORT":
            chef_id = int(params[0])
            chef_name = params[1]
            date_from = params[2]
            date_till = params[3]
            
            chef = Chef(user_id=chef_id, name=chef_name)
            generated_report = chef.generate_report(date_from, date_till)
            
            if generated_report:
                response = generated_report
            else:
                response = "No feedback found for the specified date range."
            
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_RECOMMENDED_ITEMS":
            chef = Chef(user_id=params[0], name=params[1])
            recommended_items = chef.view_generated_recommended_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Score: {item[3]:.2f}" for item in recommended_items])
            client_socket.send(response.encode('utf-8'))
            
        else:
            client_socket.send("Unknown command".encode('utf-8'))
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

class NotificationServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=NOTIFICATION_PORT):
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
                        data = conn.recv(1024)
                        if not data:
                            break
                        Notification.send(data.decode())
                        conn.sendall(b'Notification received')

if __name__ == "__main__":
    main_server_thread = threading.Thread(target=start_server)
    notification_server_thread = NotificationServer()

    main_server_thread.start()
    notification_server_thread.start()

    main_server_thread.join()
    notification_server_thread.join()
