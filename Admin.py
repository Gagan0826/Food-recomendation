from MenuItem import MenuItem
from User import User
from Database import Database


class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def add_menu_item(self, name, price, availability):
        query = "INSERT INTO menu_items (name, price, availability) VALUES (%s, %s, %s)"
        Database.execute_query(query, (name, price, availability))

    def update_menu_item(self, item_id, new_price, new_availability):
        item = MenuItem(item_id, None, None, None)
        item.set_price(new_price)
        item.set_availability(new_availability)

    def delete_menu_item(self, item_id):
        query = "DELETE FROM menu_items WHERE item_id=%s"
        Database.execute_query(query, (item_id,))

    def generate_report(self, report_type, date_range):
        pass