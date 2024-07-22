import socket
from datetime import date as currentDate

class ConsoleApplication:
    @staticmethod
    def run():
        print("Welcome to the Cafeteria Recommendation Engine")
        while True:
            print("Select role:")
            print("1. Admin")
            print("2. Chef")
            print("3. Employee")
            print("4. Exit")
            role = input("Enter your choice: ")

            if role == '1':
                admin_id = input("Enter Admin ID: ")
                admin_name = input("Enter Admin Name: ")
                if ConsoleApplication.login("Admin", admin_id, admin_name):
                    ConsoleApplication.admin_menu(admin_id, admin_name)
                else:
                    print("Invalid Admin credentials")

            elif role == '2':
                chef_id = input("Enter Chef ID: ")
                chef_name = input("Enter Chef Name: ")
                if ConsoleApplication.login("Chef", chef_id, chef_name):
                    ConsoleApplication.chef_menu(chef_id, chef_name)
                else:
                    print("Invalid Chef credentials")

            elif role == '3':
                emp_id = input("Enter Employee ID: ")
                emp_name = input("Enter Employee Name: ")
                if ConsoleApplication.login("Employee", emp_id, emp_name):
                    ConsoleApplication.employee_menu(emp_id, emp_name)
                else:
                    print("Invalid Employee credentials")
                    
            elif role == '4':
                print("Thank you for using our app")
                break

            else:
                print("Invalid choice, please try again.")

    @staticmethod
    def login(user_type, user_id, name):
        command = f"LOGIN,{user_type},{user_id},{name}"
        response = ConsoleApplication.send_request(command)
        return response == "Login successful"

    @staticmethod
    def admin_menu(admin_id, admin_name):
        user_role="Admin"
        while True:
            print("\nAdmin Menu")
            print("1. Add Menu Item")
            print("2. Update Menu Item")
            print("3. Delete Menu Item")
            print("4. View Menu Item")
            print("5. Discard Menu Items Based on Feedback")
            print("6. Add User")
            print("7. Delete User")
            print("8. Update User")
            print("9. View All Users")
            print("10. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                try:
                    name = input("Enter item name: ")
                    price = float(input("Enter item price: "))
                    type = input("Enter item type('Breakfast', 'Lunch', 'Dinner'): ")
                    availability = input("Enter item availability (1 for yes/ 0 for no): ")
                    command = f"ADD_MENU_ITEM,{user_role},{admin_id},{admin_name},{name},{price},{type},{availability}"
                    ConsoleApplication.send_request(command)
                except ValueError:
                        print("Invalid input for price or availability. Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '2':
                try:
                    item_id = int(input("Enter item ID: "))
                    new_price = float(input("Enter new price: "))
                    type = input("Enter item type('Breakfast', 'Lunch', 'Dinner'): ")
                    new_availability = input("Enter new availability (yes/no): ")
                    command = f"UPDATE_MENU_ITEM,{user_role},{admin_id},{admin_name},{item_id},{new_price},{type},{new_availability}"
                    ConsoleApplication.send_request(command)
                except ValueError:
                        print("Invalid input for price or availability. Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '3':
                try:
                    item_id = int(input("Enter item ID: "))
                    command = f"DELETE_MENU_ITEM,{user_role},{admin_id},{admin_name},{item_id}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except ValueError:
                        print("Invalid input for item id Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            elif choice == '4':
                command = f"VIEW_ALL_MENU,{user_role},{admin_id},{admin_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                command = f"DISCARD_ITEMS,{user_role},{admin_id},{admin_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

                
                if "Do you want to delete these items? (yes/no)" in response:
                    user_confirmation = input("Enter your choice (yes/no): ").strip().lower()

                
                    if user_confirmation in ['yes']:
                        confirmation_command = f"CONFIRM_DISCARD,{user_role},{admin_id},{admin_name},{user_confirmation}"
                        final_response = ConsoleApplication.send_request(confirmation_command)
                        print(final_response)
                    else:
                        print("No items were removed from the menu.")

            elif choice == '6':
                try:
                    new_user_id = input("Enter new user ID: ")
                    new_user_name = input("Enter new user name: ")
                    new_user_role = input("Enter new user role (Admin/Chef/Employee): ")
                    command = f"ADD_USER,{user_role},{admin_id},{admin_name},{new_user_id},{new_user_name},{new_user_role}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '7':
                try:
                    user_id = input("Enter the user ID to delete: ")
                    command = f"DELETE_USER,{user_role},{admin_id},{admin_name},{user_id}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '8':
                try:
                    user_id = input("Enter the user ID to update: ")
                    new_user_name = input("Enter new user name: ")
                    new_user_role = input("Enter new user role (Admin/User): ")
                    command = f"UPDATE_USER,{user_role},{admin_id},{admin_name},{user_id},{new_user_name},{new_user_role}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except Exception as e:
                    print(f"An error occurred: {e}")
            
            elif choice == '9':
                command = f"VIEW_ALL_USERS,{user_role},{admin_id},{admin_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '10':
                break

    @staticmethod
    def chef_menu(chef_id, chef_name):
        user_role="Chef"
        while True:
            print("\nChef Menu")
            print("1. Recommend Menu")
            print("2. View Feedback")
            print("3. Send Notification")
            print("4. View All Menu Items")
            print("5. View Recommendation Menu Items")
            print("6. View Ordered Items")
            print("7. Generate recomendations")
            print("8. View Generated Recommended Items")
            print("9. View employee voted Items")
            print("10. Generate Report")
            print("11. View deleted item feedback")
            print("12. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                command = f"VIEW_ALL_MENU,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)
                item_id = input("Enter item id: ")
                date = currentDate.today()
                command = f"RECOMMEND_MENU,{user_role},{chef_id},{chef_name},{item_id},{date}"
                ConsoleApplication.send_request(command)

            elif choice == '2':
                try:
                    command = f"VIEW_ALL_MENU,{user_role},{chef_id},{chef_name}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                    item_id = int(input("Enter item ID: "))
                    command = f"VIEW_FEEDBACK,{user_role},{chef_id},{chef_name},{item_id}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except ValueError:
                        print("Invalid input for item id Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '3':
                notification_message = input("Enter the notification message: ")
                command = f"SEND_NOTIFICATION,{user_role},{notification_message}"
                ConsoleApplication.send_request(command)

            elif choice == '4':
                command = f"VIEW_ALL_MENU,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                command = f"VIEW_RECOMMENDATION_MENU,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '6':
                command = f"VIEW_ORDERED_ITEMS,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)
            
            elif choice == '7':
                command = f"RECOMMEND_TOP_ITEMS",{user_role}
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '8':
                command = f"VIEW_GENERATED_RECOMMENDED_ITEMS,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '9':
                command = f"VIEW_VOTED_ITEMS,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '10':
                print("Please enter the dates in the format YYYY-MM-DD")
                date_from = input("Enter starting date: ")
                date_till = input("Enter ending date: ")
                command = f"GENERATE_REPORT,{user_role},{chef_id},{chef_name},{date_from},{date_till}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '11':
                command = f"VIEW_DELETED_ITEM_FEEDBACK,{user_role},{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '12':
                break

    @staticmethod
    def employee_menu(emp_id, emp_name):
        user_role="Employee"
        while True:
            print("\nEmployee Menu")
            print("1. Choose Meal")
            print("2. Give Feedback")
            print("3. View available Menu")
            print("4. View All Menu Items")
            print("5. Show Notifications")
            print("6. Vote for food")
            print("7. Provide Feedback on Deleted Item")
            print("8. Update User Profile")
            print("9. View Personalized Menu")
            print("10. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                try:
                    date = currentDate.today()
                    item_id = int(input("Enter item ID: "))
                    command = f"CHOOSE_MEAL,{user_role},{emp_id},{emp_name},{date},{item_id}"
                    ConsoleApplication.send_request(command)
                    print("meal choosen")
                except ValueError:
                        print("Invalid input for item id Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '2':
                try:
                    item_id = int(input("Enter item ID: "))
                    comment = input("Enter your comment: ")
                    rating = int(input("Enter your rating: "))
                    date= currentDate.today()
                    command = f"GIVE_FEEDBACK,{user_role},{emp_id},{emp_name},{item_id},{comment},{rating},{date}"
                    ConsoleApplication.send_request(command)
                except ValueError:
                        print("Invalid input for item id or rating Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '3':
                command = f"VIEW_AVAILABLE_MENU,{user_role},{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '4':
                command = f"VIEW_ALL_MENU,{user_role},{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                command = f"RECEIVE_NOTIFICATION,{user_role}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '6':
                try:    
                    command = f"VIEW_AVAILABLE_MENU,{user_role},{emp_id},{emp_name}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                    date = currentDate.today()
                    item_id = int(input("Enter food item ID: "))
                    command = f"VOTE_FOOD_ITEM,{user_role},{emp_id},{emp_name},{date},{item_id}"
                    response = ConsoleApplication.send_request(command)
                    print(response)
                except ValueError:
                        print("Invalid input for item id Please enter a number.")
                except Exception as e:
                    print(f"An error occurred: {e}")

            elif choice == '7':
                command = f"VIEW_DELETED_MENU,{user_role},{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)
                deleted_item_name = input("Enter the name of the deleted item: ")
                questions = [
                    "What didn’t you like about the item?",
                    "How would you like the item to taste?",
                    "Share your mom’s recipe."
                ]
                feedback = []
                for question in questions:
                    answer = input(f"{question} ")
                    feedback.append(answer)
                command = f"FEEDBACK_DELETED_ITEM,{user_role},{deleted_item_name},{feedback[0]},{feedback[1]},{feedback[2]}"
                response = ConsoleApplication.send_request(command)
                print(response)
                
            elif choice == '8':
                print("\nUpdate User Profile")
                diet_preference = input("Enter diet preference (Vegetarian/Non Vegetarian/Eggetarian): ")
                spice_level = input("Enter spice level preference (High/Medium/Low): ")
                cuisine_preference = input("Enter cuisine preference (North Indian/South Indian/Other): ")
                sweet_tooth = input("Do you have a sweet tooth? (Yes/No): ").lower() == 'yes'
                command = f"UPDATE_USER_PROFILE,{user_role},{emp_id},{emp_name},{diet_preference},{spice_level},{cuisine_preference},{sweet_tooth}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '9':
                command = f"VIEW_PERSONALIZED_MENU,{user_role},{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '10':
                break

    @staticmethod
    def send_request(command):
        HOST = 'localhost'
        PORT = 8080
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(command.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        client_socket.close()
        return response   

if __name__ == "__main__":
    ConsoleApplication.run()
