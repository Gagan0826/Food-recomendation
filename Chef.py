from MenuItem import MenuItem
from Notification import Notification
from User import User
from Database import Database
from tabulate import tabulate


class Chef(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def recommend_menu(self, item_id, date):
        query = "INSERT INTO chef_recommendation_menu (item_id, rolled_out_date) VALUES (%s,%s)"
        Database.execute_query(query, (item_id, date))

    def view_feedback(self, item_id):
        item = MenuItem(item_id, None, None, None)
        return item.get_feedback()

    def get_overall_rating(self,item_id):
        item = MenuItem(item_id, None, None, None)
        return item.get_average_rating()

    def send_notification(self, notification_message):
        Notification.send(notification_message)

    def view_recomendation_menu(self):
        query =  """
        SELECT *
        FROM menu_items
        WHERE item_id IN (SELECT item_id FROM chef_recommendation_menu)
        """
        return Database.fetch_query(query)
    
    def view_ordered_items(self):
        query =   """
        SELECT *
        FROM menu_items
        WHERE item_id IN (SELECT item_id FROM Final_Order)
        """
        return Database.fetch_query(query)
    
    def view_generated_recommended_items(self):
        query = """
        SELECT menu_items.item_id, menu_items.name, menu_items.price, generated_recommended_items.score
        FROM generated_recommended_items
        JOIN menu_items ON generated_recommended_items.item_id = menu_items.item_id
        ORDER BY generated_recommended_items.score DESC
        """
        return Database.fetch_query(query)
    
    def generate_report(self, date_from, date_till):
            query = """
            SELECT feedback.feedback_id, feedback.item_id, menu_items.name, feedback.comment, feedback.rating, feedback.feedback_date
            FROM feedback
            JOIN menu_items ON feedback.item_id = menu_items.item_id
            WHERE feedback.feedback_date BETWEEN %s AND %s
            ORDER BY feedback.feedback_date ASC
            """
            result = Database.fetch_query(query, (date_from, date_till))
        
            headers = ["Feedback ID", "Item ID", "Item Name", "Comment", "Rating", "Feedback Date"]
            table = tabulate(result, headers, tablefmt="pretty")
            return table
    
    def view_voted_items(self):
        query =   """
        SELECT *
        FROM menu_items
        WHERE item_id IN (SELECT item_id FROM user_preference_menu)
        """
        return Database.fetch_query(query)