from Database import Database

class MenuItem:
    def __init__(self, item_id, name, price, availability):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.availability = availability

    def set_price(self, price):
        self.price = price
        query = "UPDATE menu_items SET price=%s WHERE item_id=%s"
        Database.execute_query(query, (price, self.item_id))

    def set_availability(self, availability):
        self.availability = availability
        query = "UPDATE menu_items SET availability=%s WHERE item_id=%s"
        Database.execute_query(query, (availability, self.item_id))

    def get_feedback(self):
        query = "SELECT comment, rating FROM feedback WHERE item_id=%s"
        return Database.fetch_query(query, (self.item_id,))

    def get_average_rating(self):
        query = "SELECT AVG(rating) FROM feedback WHERE item_id=%s"
        result = Database.fetch_query(query, (self.item_id,))
        if result and result[0][0] is not None:
            return f"{result[0][0]:.2f}"
        return None