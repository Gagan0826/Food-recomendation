
from Database import Database


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def login(self):
        query = "SELECT * FROM users WHERE user_id=%s AND user_name=%s"
        result = Database.fetch_query(query, (self.user_id, self.name))
        return result
    
    def view_menu(self):
        query = "SELECT * FROM menu_items"
        return Database.fetch_query(query)