from Database import Database


class Feedback:
    def __init__(self, item_id, comment, rating):
        self.item_id = item_id
        self.comment = comment
        self.rating = rating

    def save(self):
        query = "INSERT INTO feedback (item_id, comment, rating) VALUES (%s, %s, %s)"
        Database.execute_query(query, (self.item_id, self.comment, self.rating))
        