from src.business.Employee import Employee
from src.utils.Notification import Notification
from src.data.models.UserProfile import UserProfile
from src.data.models.DeletedMenuItem import DeletedMenuItem
class EmployeeHandler:
    @staticmethod
    def handle_request(client_socket, command, params):
        try:
            if len(params) >= 2:
                employee = Employee(user_id=params[0], name=params[1])
            else:
                client_socket.send("Invalid parameters".encode('utf-8'))
                return
            if command == "LOGIN":
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
            elif command == "RECEIVE_NOTIFICATION":
                notifications = Notification.receive()
                client_socket.send("\n".join(notifications).encode('utf-8'))
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
            elif command == "UPDATE_USER_PROFILE":
                print(f"Received params: {params}")  # Debug print
                user_id = params[0]
                user_name = params[1]
                diet_preference = params[2]
                spice_level = params[3]
                cuisine_preference = params[4]
                sweet_tooth = params[5].lower() == 'true'
                UserProfile.update_profile(user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth)
                response = f"Profile updated for user: {user_name}"
                client_socket.send(response.encode('utf-8'))
            elif command == "VIEW_DELETED_MENU":
                deleted_items=DeletedMenuItem.view_deleted_menu()
                response = "\n".join([f"ID: {item[0]}, Name: {item[1]}" for item in deleted_items])
                client_socket.send(response.encode('utf-8'))
            elif command.startswith("FEEDBACK_DELETED_ITEM"):
                deleted_item_name = params[0]
                reason = params[1]
                improvement_required = params[2]
                mothers_recipie = params[3]
                
                deleted_item_id = DeletedMenuItem.get_deleted_item_id(deleted_item_name)
                if deleted_item_id is not None:
                    DeletedMenuItem.save(deleted_item_id, deleted_item_name, reason, improvement_required, mothers_recipie)
                    response = f"Feedback received for the deleted item: {deleted_item_name}"
                else:
                    response = f"Deleted item '{deleted_item_name}' not found."

                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send("Unknown command for Employee".encode('utf-8'))
        except Exception as e:
            client_socket.send(f"Error processing employee request: {e}".encode('utf-8'))
