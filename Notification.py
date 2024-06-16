import queue
class Notification:
    queue = queue.Queue()

    @staticmethod
    def send(notification_type, item_id):
        message = f"{notification_type}: Item {item_id}"
        Notification.queue.put(message)

    @staticmethod
    def receive(user_id):
        notifications = []
        while not Notification.queue.empty():
            notifications.append(Notification.queue.get())
        return notifications