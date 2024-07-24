from src.data.Database import Database
from src.business.FeedbackAnalyzer import FeedbackAnalyzer
from src.utils.Notification import Notification
class MenuItem:
    def __init__(self, item_id, name, price, availability):
        self.item_id = item_id
        self.name = name
        self.price = price

    def set_price(self, price):
        self.price = price
        query = "UPDATE menu_items SET price=%s WHERE item_id=%s"
        Database.execute_query(query, (price, self.item_id))

    def get_feedback(self):
        query = "SELECT comment, rating FROM feedback WHERE item_id=%s"
        return Database.fetch_query(query, (self.item_id,))

    def get_average_rating(self):
        query = "SELECT AVG(rating) FROM feedback WHERE item_id=%s"
        result = Database.fetch_query(query, (self.item_id,))
        if result and result[0][0] is not None:
            return f"{result[0][0]:.2f}"
        return None
    @staticmethod
    def remove_item(item_id):
        query = "DELETE FROM menu_items WHERE item_id=%s"
        item_name=MenuItem.get_item_name(item_id)
        Notification.send(f"{item_name} has been deleted, please provide feedback")
        Database.execute_query(query, (item_id,))

    @staticmethod
    def get_item_name(item_id):
        query = "SELECT name FROM menu_items WHERE item_id = %s"
        result = Database.fetch_query(query, (item_id,))
        if result:
            return result[0][0]
        else:
            return None

    @staticmethod
    def get_item_id(item_name):
        query = "SELECT item_id FROM menu_items WHERE name = %s"
        result = Database.fetch_query(query, (item_name,))
        if result:
            return result[0][0]
        else:
            return None