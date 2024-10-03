from src.data.models.Feedback import Feedback
from src.utils.Notification import Notification
from src.data.models.User import User
from src.data.Database import Database
from tabulate import tabulate

class Employee(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def choose_meal(self, date, item_id, user_id):
        query = "INSERT INTO Final_Order (employee_id, date, item_id) VALUES (%s, %s, %s)"
        Database.execute_query(query, (user_id, date, item_id))

    def give_feedback(self, item_id, comment, rating, date):
        feedback = Feedback(item_id, comment, rating, date)
        feedback.save()

    def view_chef_recommended_menu(self):
        query = """
                SELECT mi.item_id, mi.name, mi.price, mi.food_type, 
                       mi.diet_type, mi.spice_level, mi.cuisine_type
                FROM menu_items mi
                JOIN chef_recommendation_menu crm ON mi.item_id = crm.item_id
                WHERE crm.rolled_out_date = CURDATE() 
                """
        result = Database.fetch_query(query)
        headers = ["Item ID", "Name", "Price", "Food Type", "Diet Type", "Spice Level", "Cuisine Type"]
        return tabulate(result, headers, tablefmt="pretty") if result else "No items added yet."

    def receive_notification(self):
        return Notification.receive()

    def get_emp_id(self):
        return self.user_id

    def request_food_item(self, date, item_id, user_id):
        query = "INSERT INTO user_preference_menu (item_id, employee_id, choosen_date) VALUES (%s, %s, %s)"
        Database.execute_query(query, (item_id, user_id, date))

    def view_menu(self):
        query = "SELECT item_id, name, price, food_type, diet_type, spice_level, cuisine_type FROM menu_items"
        result = Database.fetch_query(query)
        headers = ["Item ID", "Name", "Price", "Food Type", "Diet Type", "Spice Level", "Cuisine Type"]
        return tabulate(result, headers, tablefmt="pretty") if result else "No menu items found."
