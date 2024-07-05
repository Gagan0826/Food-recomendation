from MenuItem import MenuItem
from User import User
from Database import Database
from FeedbackAnalyzer import FeedbackAnalyzer

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def add_menu_item(self, name, price, type,availability):
        query = "INSERT INTO menu_items (name, price, food_type, availability) VALUES (%s, %s, %s,%s)"
        Database.execute_query(query, (name, price,type, availability))

    def update_menu_item(self, item_id, new_price, new_availability):
        item = MenuItem(item_id, None, None, None)
        item.set_price(new_price)
        item.set_availability(new_availability)

    def delete_menu_item(self, item_id):
        query = "DELETE FROM menu_items WHERE item_id=%s"
        Database.execute_query(query, (item_id,))
        response = "item deleted successfully"
        return response
    
    def view_menu(self):
        query = "SELECT * FROM menu_items"
        return Database.fetch_query(query)
    
    def get_low_rated_items(self):
        discard_items = FeedbackAnalyzer.discard_items()
        discarded_item_names = []
        for item_id in discard_items:
            item_name = MenuItem.get_item_name(item_id)
            if item_name:
                discarded_item_names.append(item_name)
        return discarded_item_names

    def confirm_discard_items(self, items_to_discard):
        for item_name in items_to_discard:
            item_id = MenuItem.get_item_id(item_name)
            if item_id:
                MenuItem.remove_item(item_id)
