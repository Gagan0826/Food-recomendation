from src.business.Employee import Employee
from src.utils.Notification import Notification
from src.data.models.UserProfile import UserProfile
from src.data.models.DeletedMenuItem import DeletedMenuItem
import tabulate
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
                menu = employee.view_chef_recommended_menu()
                client_socket.send(menu.encode('utf-8'))

            elif command == "CHOOSE_MEAL":
                date = params[2]
                item_id = int(params[3])
                employee.choose_meal(date, item_id, params[0])
                client_socket.send("Meal chosen successfully".encode('utf-8'))

            elif command == "RECEIVE_NOTIFICATION":
                notifications = Notification.receive()
                client_socket.send("\n".join(notifications).encode('utf-8'))

            elif command == "VOTE_FOOD_ITEM":
                date = params[2]
                item_id = params[3]
                employee.request_food_item(date, item_id, params[0])  
                client_socket.send("Vote recorded successfully".encode('utf-8'))

            elif command == "VIEW_ALL_MENU":
                all_items = employee.view_menu()
                client_socket.send(all_items.encode('utf-8'))

            elif command == "VIEW_PERSONALIZED_MENU":
                user_id = params[0]
                personalized_menu = UserProfile.get_personalized_menu(user_id)
                if personalized_menu:
                    response=personalized_menu
                else:
                    response = "No personalized menu items found based on your preferences."
                client_socket.send(response.encode('utf-8'))

            elif command == "UPDATE_USER_PROFILE":
                user_id = params[0]
                diet_preference = params[2]
                spice_level = params[3]
                cuisine_preference = params[4]
                sweet_tooth = params[5].lower() == 'true'
                UserProfile.update_profile(user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth)
                response = f"Profile updated for user: {params[1]}"
                client_socket.send(response.encode('utf-8'))

            elif command == "VIEW_DELETED_MENU":
                deleted_items = DeletedMenuItem.view_deleted_menu() 
                response = deleted_items
                client_socket.send(response.encode('utf-8'))

            elif command.startswith("FEEDBACK_DELETED_ITEM"):
                deleted_item_name = params[0]
                reason = params[1]
                improvement_required = params[3]
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
