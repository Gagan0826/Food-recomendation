from src.business.Admin import Admin

class AdminHandler:
    @staticmethod
    def handle_request(client_socket, command, params):
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
                admin.add_menu_item(params[2], float(params[3]), params[4])
                client_socket.send("Menu item added successfully".encode('utf-8'))
            elif command == "UPDATE_MENU_ITEM":
                admin.update_menu_item(int(params[2]), float(params[3]))
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
                client_socket.send(all_items.encode('utf-8'))
            elif command == "ADD_USER":
                new_user_id = params[2]
                new_user_name = params[3]
                new_user_role = params[4]
                admin.add_user(new_user_id, new_user_name, new_user_role)
                client_socket.send("New user added successfully".encode('utf-8'))
            elif command == "DELETE_USER":
                user_id = params[2]
                admin.delete_user(user_id)
                client_socket.send("User deleted successfully".encode('utf-8'))
            elif command == "UPDATE_USER":
                user_id = params[2]
                new_user_name = params[3]
                new_user_role = params[4]
                admin.update_user(user_id, new_user_name, new_user_role)
                client_socket.send("User updated successfully".encode('utf-8'))
            elif command == "VIEW_ALL_USERS":
                all_users = admin.view_all_users()
                client_socket.send(all_users.encode('utf-8'))
            else:
                client_socket.send("Unknown command for Admin".encode('utf-8'))
        except Exception as e:
            client_socket.send(f"Error processing admin request: {e}".encode('utf-8'))
