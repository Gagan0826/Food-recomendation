from MenuItem import MenuItem
from Notification import Notification
from User import User
from Database import Database


class Chef(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)

    def recommend_menu(self, item_id, date):
        query = "INSERT INTO chef_recommendation_menu (item_id, rolled_out_date,food_type) VALUES (%s,%s)"
        Database.execute_query(query, (item_id, date))

    def view_feedback(self, item_id):
        item = MenuItem(item_id, None, None, None)
        return item.get_feedback()

    def send_notification(self, notification_type, item_id):
        Notification.send(notification_type, item_id)