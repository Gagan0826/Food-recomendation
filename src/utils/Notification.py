import queue

class Notification:
    queue = queue.Queue()

    @staticmethod
    def send(notification_message):
        message = f"Notification: {notification_message}"
        Notification.queue.put(message)

    @staticmethod
    def receive():
        if Notification.queue.empty():
            return ["No notifications available"]
        notifications = []
        while not Notification.queue.empty():
            notifications.append(Notification.queue.get())
        return notifications
