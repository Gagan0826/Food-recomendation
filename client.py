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
        while True:
            print("\nAdmin Menu")
            print("1. Add Menu Item")
            print("2. Update Menu Item")
            print("3. Delete Menu Item")
            print("4. View Menu Item")
            print("5. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter item name: ")
                price = float(input("Enter item price: "))
                availability = input("Enter item availability (1 for yes/ 0 for no): ")
                command = f"ADD_MENU_ITEM,{admin_id},{admin_name},{name},{price},{availability}"
                ConsoleApplication.send_request(command)

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                new_price = float(input("Enter new price: "))
                new_availability = input("Enter new availability (yes/no): ")
                command = f"UPDATE_MENU_ITEM,{admin_id},{admin_name},{item_id},{new_price},{new_availability}"
                ConsoleApplication.send_request(command)

            elif choice == '3':
                item_id = int(input("Enter item ID: "))
                command = f"DELETE_MENU_ITEM,{admin_id},{admin_name},{item_id}"
                response = ConsoleApplication.send_request(command)
                print(response)
            
            elif choice == '4':
                command = f"VIEW_MENU,{admin_id},{admin_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                break

    @staticmethod
    def chef_menu(chef_id, chef_name):
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
            print("11. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                item_id = input("Enter item id: ")
                date = currentDate.today()
                command = f"RECOMMEND_MENU,{chef_id},{chef_name},{item_id},{date}"
                ConsoleApplication.send_request(command)

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                command = f"VIEW_FEEDBACK,{chef_id},{chef_name},{item_id}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '3':
                notification_message = input("Enter the notification message: ")
                command = f"SEND_NOTIFICATION,{notification_message}"
                ConsoleApplication.send_request(command)

            elif choice == '4':
                command = f"VIEW_ALL_MENU,{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                command = f"VIEW_RECOMMENDATION_MENU,{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '6':
                command = f"VIEW_ORDERED_ITEMS,{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)
            
            elif choice == '7':
                command = f"RECOMMEND_TOP_ITEMS"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '8':
                command = f"VIEW_GENERATED_RECOMMENDED_ITEMS,{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '9':
                command = f"VIEW_VOTED_ITEMS,{chef_id},{chef_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '10':
                print("Please enter the dates in the format YYYY-MM-DD")
                date_from = input("Enter starting date: ")
                date_till = input("Enter ending date: ")
                command = f"GENERATE_REPORT,{chef_id},{chef_name},{date_from},{date_till}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '11':
                break

    @staticmethod
    def employee_menu(emp_id, emp_name):
        while True:
            print("\nEmployee Menu")
            print("1. Choose Meal")
            print("2. Give Feedback")
            print("3. View available Menu")
            print("4. Receive Notifications")
            print("5. View all Menu")
            print("6. Vote for food")
            print("7. Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                date = currentDate.today()
                item_id = int(input("Enter item ID: "))
                command = f"CHOOSE_MEAL,{emp_id},{emp_name},{date},{item_id}"
                ConsoleApplication.send_request(command)
                print("meal choosen")

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                comment = input("Enter your comment: ")
                rating = int(input("Enter your rating: "))
                date= currentDate.today()
                command = f"GIVE_FEEDBACK,{emp_id},{emp_name},{item_id},{comment},{rating},{date}"
                ConsoleApplication.send_request(command)

            elif choice == '3':
                command = f"VIEW_AVAILABLE_MENU,{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '4':
                command = f"RECEIVE_NOTIFICATION"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '5':
                command = f"VIEW_ALL_MENU,{emp_id},{emp_name}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '6':
                date = currentDate.today()
                item_id = int(input("Enter food item ID: "))
                command = f"VOTE_FOOD_ITEM,{emp_id},{emp_name},{date},{item_id}"
                response = ConsoleApplication.send_request(command)
                print(response)

            elif choice == '7':
                break

    @staticmethod
    def send_request(command):
        HOST = '127.0.0.1'
        PORT = 8080
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        client_socket.send(command.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return response

if __name__ == "__main__":
    ConsoleApplication.run()
