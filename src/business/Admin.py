from src.data.models.MenuItem import MenuItem
from src.data.models.User import User
from src.data.Database import Database
from src.business.FeedbackAnalyzer import FeedbackAnalyzer
from src.data.models.DeletedMenuItem import DeletedMenuItem
from tabulate import tabulate

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def add_menu_item(self, name, price, type):
        query = "INSERT INTO menu_items (name, price, food_type) VALUES (%s, %s, %s)"
        Database.execute_query(query, (name, price, type))

    def update_menu_item(self, item_id, new_price):
        item = MenuItem(item_id, None, None, None)
        item.set_price(new_price)

    def delete_menu_item(self, item_id):
        query = "DELETE FROM menu_items WHERE item_id=%s"
        Database.execute_query(query, (item_id,))
        return "Item deleted successfully"

    def view_menu(self):
        query = "SELECT item_id, name, price, food_type FROM menu_items"
        result = Database.fetch_query(query)
        headers = ["Item ID", "Name", "Price", "Type of Meal"]
        return tabulate(result, headers, tablefmt="pretty") if result else "No menu items found."

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
            DeletedMenuItem.add_item(item_name)
            item_id = MenuItem.get_item_id(item_name)
            if item_id:
                MenuItem.remove_item(item_id)

    def add_user(self, user_id, name, role):
        query = "INSERT INTO users (user_id, user_name, role) VALUES (%s, %s, %s)"
        Database.execute_query(query, (user_id, name, role))

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id=%s"
        Database.execute_query(query, (user_id,))

    def update_user(self, user_id, new_user_name, new_user_role):
        query = "UPDATE users SET user_name=%s, role=%s WHERE user_id=%s"
        Database.execute_query(query, (new_user_name, new_user_role, user_id))
        
    def view_all_users(self):
        query = "SELECT * FROM users"
        result = Database.fetch_query(query)
        headers = ["User ID", "Name", "Role"]
        return tabulate(result, headers, tablefmt="pretty") if result else "No users found."
