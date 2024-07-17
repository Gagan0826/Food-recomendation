from src.data.models.Feedback import Feedback
from src.utils.Notification import Notification
from src.data.models.User import User
from src.data.Database import Database


class Employee(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def choose_meal(self, date, item_id,user_id):
        query = "INSERT INTO Final_Order (employee_id, date, item_id) VALUES (%s, %s, %s)"
        Database.execute_query(query, (user_id, date, item_id))

    def give_feedback(self, item_id, comment, rating, date):
        feedback = Feedback(item_id, comment, rating, date)
        feedback.save()

    def view_chef_recommended_menu(self):
        query =  """
                SELECT mi.*
                FROM menu_items mi
                JOIN chef_recommendation_menu crm ON mi.item_id = crm.item_id
                WHERE crm.rolled_out_date = CURDATE() 
                """
        return Database.fetch_query(query)
    
    def receive_notification(self):
        return Notification.receive()
    
    def get_emp_id(self):
        return self.user_id
    
    def request_food_item(self, date, item_id,user_id):
        query = "INSERT INTO user_preference_menu (item_id,employee_id, choosen_date) VALUES (%s, %s, %s)"
        Database.execute_query(query, (item_id,user_id, date,))

    def view_menu(self):
        query = "SELECT * FROM menu_items"
        return Database.fetch_query(query)
    
    @staticmethod   
    def update_user_profile(emp_id, emp_name):
        print("\nUpdate User Profile")
        diet_preference = input("Enter diet preference (Vegetarian/Non Vegetarian/Eggetarian): ")
        spice_level = input("Enter spice level preference (High/Medium/Low): ")
        cuisine_preference = input("Enter cuisine preference (North Indian/South Indian/Other): ")
        sweet_tooth = input("Do you have a sweet tooth? (Yes/No): ").lower() == 'yes'

        command = f"UPDATE_USER_PROFILE,{emp_id},{emp_name},{diet_preference},{spice_level},{cuisine_preference},{sweet_tooth}"
        response = ConsoleApplication.send_request(command)
        print(response)