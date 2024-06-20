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

    def view_menu(self):
        query =  """
        SELECT *
        FROM menu_items
        WHERE item_id IN (SELECT item_id FROM chef_recommendation_menu)
        """
        return Database.fetch_query(query)
    
    def receive_notification(self):
        return Notification.receive()
    
    def get_emp_id(self):
        return self.user_id
    