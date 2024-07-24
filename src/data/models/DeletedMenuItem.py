from src.data.Database import Database
from tabulate import tabulate

class DeletedMenuItem:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    @staticmethod
    def add_item(item):
        query = "INSERT INTO deleted_items (item_name) VALUES (%s)"
        return Database.execute_query(query, (item,))

    @staticmethod
    def view_deleted_menu():
        query = "SELECT deleted_item_id, item_name FROM deleted_items"
        result = Database.fetch_query(query)
        headers = ["Deleted Item ID", "Name"]
        return tabulate(result, headers, tablefmt="pretty") if result else "No deleted items found."
    
    @staticmethod
    def save(deleted_item_id, item_name, reason, improvement_required, mothers_recipie):
        query = "INSERT INTO deleted_item_feedback (deleted_item_id, item_name, reason, improvement_required, mothers_recipie) VALUES (%s, %s, %s, %s, %s)"
        Database.execute_query(query, (deleted_item_id, item_name, reason, improvement_required, mothers_recipie))
        
    @staticmethod
    def get_deleted_item_id(item_name):
        query = "SELECT deleted_item_id FROM deleted_items WHERE item_name = %s"
        result = Database.fetch_query(query, (item_name,))
        if result:
            return result[0][0]
        return None
