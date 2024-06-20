from Database import Database

class Validation:
    @staticmethod
    def check_menu_item_existence(item_id):
        query = "SELECT COUNT(1) FROM menu_items WHERE item_id = %s"
        result = Database.execute_query(query, (item_id,))
        if result and result[0][0] > 0:
            return True
        else:
            return False
