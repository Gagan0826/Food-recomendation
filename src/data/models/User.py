from src.data.Database import Database
from tabulate import tabulate
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def login(self):
        query = "SELECT * FROM users WHERE user_id=%s AND user_name=%s"
        result = Database.fetch_query(query, (self.user_id, self.name))
        return result

    def view_menu(self):
        query = '''SELECT  mi.item_id, mi.name, mi.price, mi.food_type, 
                    mi.diet_type, mi.spice_level, mi.cuisine_type
                FROM menu_items mi '''
        result = Database.fetch_query(query)
        if result:
            headers = ["Item ID", "Name", "Price", "Food Type", "Diet Type", "Spice Level", "Cuisine Type"]
            return tabulate(result, headers, tablefmt="pretty")
        else:
            return "No menu items found."
