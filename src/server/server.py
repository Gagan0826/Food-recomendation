import socket
import threading
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(project_root)
from src.business.Admin import Admin
from src.business.Chef import Chef
from src.business.Employee import Employee
from src.utils.Notification import Notification
from src.business.FeedbackAnalyzer import FeedbackAnalyzer
from src.data.models.DeletedMenuItem import DeletedMenuItem
from src.data.models.UserProfile import UserProfile

HOST = 'localhost'
PORT = 8080
NOTIFICATION_PORT = 5050

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
            handle_admin_requests(client_socket, command, params[1:])
        elif role == "Chef":
            handle_chef_requests(client_socket, command, params[1:])
        elif role == "Employee":
            handle_employee_requests(client_socket, command, params[1:])
        else:
            client_socket.send("Invalid role".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error processing request: {e}".encode('utf-8'))

def handle_admin_requests(client_socket, command, params):
    try:
        if len(params) >= 2:
            admin = Admin(user_id=params[0], name=params[1])
        else:
            client_socket.send("Invalid parameters".encode('utf-8'))
            return
        if command == "LOGIN":
            if admin.login():
                client_socket.send("Login successful".encode('utf-8'))
            else:
                client_socket.send("Invalid credentials".encode('utf-8'))
        elif command == "ADD_MENU_ITEM":
            admin.add_menu_item(params[2], float(params[3]), params[4], params[5])
            client_socket.send("Menu item added successfully".encode('utf-8'))
        elif command == "UPDATE_MENU_ITEM":
            admin.update_menu_item(int(params[2]), float(params[3]), params[4])
            client_socket.send("Menu item updated successfully".encode('utf-8'))
        elif command == "DELETE_MENU_ITEM":
            response = admin.delete_menu_item(int(params[2]))
            client_socket.send(response.encode('utf-8'))
        elif command == "DISCARD_ITEMS":
            low_rated_items = admin.get_low_rated_items()
            if not low_rated_items:
                response = "No items to remove from the menu."
            else:
                confirmation_message = " Do you want to delete these items? (yes/no)"
                response = f"Items identified for removal: {low_rated_items}. {confirmation_message}"
            client_socket.send(response.encode('utf-8'))
        elif command.startswith("CONFIRM_DISCARD"):
            user_confirmation = params[2].strip().lower()
            if user_confirmation == 'yes':
                low_rated_items = admin.get_low_rated_items()  
                admin.confirm_discard_items(low_rated_items)
                response = f"Items removed from the menu: {low_rated_items}"
            else:
                response = "No items were removed from the menu."
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_ALL_MENU":
            all_items = admin.view_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in all_items])
            client_socket.send(response.encode('utf-8'))
        else:
            client_socket.send("Unknown command for Admin".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error processing admin request: {e}".encode('utf-8'))

def handle_chef_requests(client_socket, command, params):
    try:
        if len(params) >= 2:
            chef = Chef(user_id=params[0], name=params[1])
        else:
            client_socket.send("Invalid parameters".encode('utf-8'))
            return
        if command == "LOGIN":
            if chef.login():
                client_socket.send("Login successful".encode('utf-8'))
            else:
                client_socket.send("Invalid credentials".encode('utf-8'))
        elif command == "RECOMMEND_MENU":
            chef.recommend_menu(params[2], params[3])
            client_socket.send("Recommended successfully".encode('utf-8'))
        elif command == "VIEW_FEEDBACK":
            item_id = int(params[2])
            feedback = chef.view_feedback(item_id)
            overall_rating = chef.get_overall_rating(item_id)
            response = "\n".join([f"Comment: {f[0]}, Rating: {f[1]}" for f in feedback])
            response += f"\nOverall Rating: {overall_rating}"
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_RECOMMENDATION_MENU":
            menu = chef.view_recommendation_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_ORDERED_ITEMS":
            menu = chef.view_ordered_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_VOTED_ITEMS":
            menu = chef.view_voted_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in menu])
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_GENERATED_RECOMMENDED_ITEMS":
            recommended_items = chef.view_generated_recommended_items()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Score: {item[3]:.2f}" for item in recommended_items])
            client_socket.send(response.encode('utf-8'))
        elif command == "GENERATE_REPORT":
            date_from = params[2]
            date_till = params[3]
            generated_report = chef.generate_report(date_from, date_till)
            if generated_report:
                response = generated_report
            else:
                response = "No feedback found for the specified date range."
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_DELETED_ITEM_FEEDBACK":
            feedback_items = chef.view_deleted_items_feedback()
            if feedback_items:
                response = "\n".join([
                    f"Feedback ID: {item[0]}, Deleted Item ID: {item[1]}, Name: {item[2]}, Reason: {item[3]}, Improvement Required: {item[4]}, Mother's Recipe: {item[5]}"
                    for item in feedback_items
                ])
            else:
                response = "No feedback available for deleted items."
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_ALL_MENU":
            all_items = chef.view_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in all_items])
            client_socket.send(response.encode('utf-8'))
        else:
            client_socket.send("Unknown command for Chef".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error processing chef request: {e}".encode('utf-8'))

def handle_employee_requests(client_socket, command, params):
    try:
        if command == "LOGIN":
            employee = Employee(user_id=params[0], name=params[1])
            if employee.login():
                client_socket.send("Login successful".encode('utf-8'))
            else:
                client_socket.send("Invalid credentials".encode('utf-8'))
        elif command == "GIVE_FEEDBACK":
            employee = Employee(user_id=params[0], name=params[1])
            item_id = int(params[2])
            comment = params[3]
            rating = params[4]
            date = params[5]
            try:
                employee.give_feedback(item_id, comment, rating, date)
                response = "Feedback given successfully"
            except Exception as e:
                response = f"Failed to give feedback: {e}"
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_AVAILABLE_MENU":
            try:
                employee = Employee(user_id=params[0], name=params[1])
                menu = employee.view_chef_recommended_menu()
                if menu:
                    response = "\n".join([
                        f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" 
                        for item in menu
                    ])
                    client_socket.send(response.encode('utf-8'))
                else:
                    response = "No items added yet"
                    client_socket.send(response.encode('utf-8'))
            except Exception as e:
                error_message = f"An error occurred while fetching the menu: {str(e)}"
                client_socket.send(error_message.encode('utf-8'))
        elif command == "CHOOSE_MEAL":
            employee = Employee(user_id=params[0], name=params[1])
            date = params[2]
            item_id = int(params[3])
            user_id = params[0]
            employee.choose_meal(date, item_id, user_id)
            client_socket.send("Meal chosen successfully".encode('utf-8'))
        elif command == "VOTE_FOOD_ITEM":
            employee = Employee(user_id=params[0], name=params[1])
            date = params[2]
            item_id = params[3]
            employee.request_food_item(date, item_id, params[0])  
            client_socket.send("Vote recorded successfully".encode('utf-8'))
        elif command == "VIEW_ALL_MENU":
            employee = Employee(user_id=params[0], name=params[1],)
            all_items = employee.view_menu()
            response = "\n".join([f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}" for item in all_items])
            client_socket.send(response.encode('utf-8'))
        elif command == "VIEW_PERSONALIZED_MENU":
            user_id = params[0]
            user_name = params[1]
            personalized_menu = UserProfile.get_personalized_menu(user_id)
            if personalized_menu:
                response = "Personalized Menu:\n"
                for item in personalized_menu:
                    response += f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type: {item[3]}, Availability: {item[4]}\n"
            else:
                response = "No personalized menu items found based on your preferences."
            client_socket.send(response.encode('utf-8'))
        elif command.startswith("UPDATE_USER_PROFILE"):
            user_id = params[0]
            user_name = params[1]
            diet_preference = params[2]
            spice_level = params[3]
            cuisine_preference = params[4]
            sweet_tooth = params[5].lower() == 'true'
            UserProfile.update_profile(user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth)
            response = f"Profile updated for user: {user_name}"
        else:
            client_socket.send("Unknown command for Employee".encode('utf-8'))
    except Exception as e:
        client_socket.send(f"Error processing employee request: {e}".encode('utf-8'))

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
    def __init__(self, host='localhost', port=NOTIFICATION_PORT):
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
