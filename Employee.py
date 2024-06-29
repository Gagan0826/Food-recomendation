from Feedback import Feedback
from Notification import Notification
from User import User
from Database import Database


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