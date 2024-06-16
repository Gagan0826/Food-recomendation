from Admin import Admin
from Chef import Chef
from Employee import Employee
from NotificationServer import NotificationServer
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
                admin = Admin(admin_id, admin_name)
                print("test line")
                if admin.login():
                    ConsoleApplication.admin_menu(admin)
                else:
                    print("Invalid Admin credentials")

            elif role == '2':
                chef_id = input("Enter Chef ID: ")
                chef_name = input("Enter Chef Name: ")
                chef = Chef(chef_id, chef_name)
                if chef.login():
                    ConsoleApplication.chef_menu(chef)
                else:
                    print("Invalid Chef credentials")

            elif role == '3':
                emp_id = input("Enter Employee ID: ")
                emp_name = input("Enter Employee Name: ")
                employee = Employee(emp_id, emp_name)
                if employee.login():
                    ConsoleApplication.employee_menu(employee)
                else:
                    print("Invalid Employee credentials")
                    
            elif role == '4':
                print("Thank you for using our app")
                break

            else:
                print("Invalid choice, please try again.")


    @staticmethod
    def admin_menu(admin):
        while True:
            print("\nAdmin Menu")
            print("1. Add Menu Item")
            print("2. Update Menu Item")
            print("3. Delete Menu Item")
            print("4. view Menu Item")
            print("5. Generate Report")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter item name: ")
                price = float(input("Enter item price: "))
                availability = input("Enter item availability (yes/no): ")
                admin.add_menu_item(name, price, availability)
                print("Menu item added successfully.")

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                new_price = float(input("Enter new price: "))
                new_availability = input("Enter new availability (yes/no): ")
                admin.update_menu_item(item_id, new_price, new_availability)
                print("Menu item updated successfully.")

            elif choice == '3':
                item_id = int(input("Enter item ID: "))
                admin.delete_menu_item(item_id)
                print("Menu item deleted successfully.")
            
            elif choice == '4':
                menu = admin.view_menu()
                for item in menu:
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal:{item[3]}, Availability: {item[4]}")

            elif choice == '5':
                report_type = input("Enter report type: ")
                date_range = input("Enter date range: ")
                admin.generate_report(report_type, date_range)
                print("Report generated successfully.")

            elif choice == '6':
                break

    @staticmethod
    def chef_menu(chef):
        while True:
            print("\nChef Menu")
            print("1. Recommend Menu")
            print("2. View Feedback")
            print("3. Send Notification")
            print("4. view Menu Item")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                item_id = input("Enter item id: ")
                date = currentDate.today()
                chef.recommend_menu(item_id, date)
                print("Menu recommended successfully.")

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                feedback = chef.view_feedback(item_id)
                for comment, rating in feedback:
                    print(f"Comment: {comment}, Rating: {rating}")

            elif choice == '3':
                notification_type = input("Enter notification type: ")
                item_id = int(input("Enter item ID: "))
                chef.send_notification(notification_type, item_id)
                print("Notification sent successfully.")

            elif choice == '4':
                menu = chef.view_menu()
                for item in menu:
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal:{item[3]}, Availability: {item[4]}")

            elif choice == '5':
                break

    @staticmethod
    def employee_menu(employee):
        while True:
            print("\nEmployee Menu")
            print("1. Choose Meal")
            print("2. Give Feedback")
            print("3. View Menu")
            print("4. Receive Notifications")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                meal_type = input("Enter meal type: ")
                date = currentDate.today()
                item_id = int(input("Enter item ID: "))
                employee.choose_meal(meal_type, date, item_id)
                print("Meal chosen successfully.")

            elif choice == '2':
                item_id = int(input("Enter item ID: "))
                comment = input("Enter your comment: ")
                rating = int(input("Enter your rating: "))
                employee.give_feedback(item_id, comment, rating)
                print("Feedback given successfully.")

            elif choice == '3':
                menu = employee.view_menu()
                for item in menu:
                    print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Type of meal: {item[3]}, Availability: {item[4]}")

            elif choice == '4':
                notifications = employee.receive_notification()
                for notification in notifications:
                    print(notification)

            elif choice == '5':
                break

if __name__ == "__main__":
    notification_server = NotificationServer()
    notification_server.start()
    ConsoleApplication.run()
