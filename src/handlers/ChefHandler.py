from src.business.Chef import Chef
from src.utils.Notification import Notification
from src.business.FeedbackAnalyzer import FeedbackAnalyzer

class ChefHandler:
    @staticmethod
    def handle_request(client_socket, command, params):
        try:
            if len(params) >= 2:
                chef = Chef(user_id=params[0], name=params[1])
            else:
                client_socket.send("Invalid parameters".encode('utf-8'))
                return

            if command == "LOGIN":
                if chef.login():
                    client_socket.send("Login successful".encode('utf-8'))
                else:
                    client_socket.send("Invalid credentials".encode('utf-8'))
            
            elif command == "RECOMMEND_MENU":
                chef.recommend_menu(params[2], params[3])
                client_socket.send("Recommended successfully".encode('utf-8'))

            elif command == "SEND_NOTIFICATION":
                notification_message = params[3]
                Notification.send(notification_message)
                client_socket.send("Notification sent successfully".encode('utf-8'))

            elif command == "VIEW_FEEDBACK":
                item_id = int(params[2])
                feedback = chef.view_feedback(item_id)
                overall_rating = chef.get_overall_rating(item_id)
                response = f"{feedback}\nOverall Rating: {overall_rating}"
                client_socket.send(response.encode('utf-8'))

            elif command == "VIEW_RECOMMENDATION_MENU":
                menu = chef.view_recommendation_menu()
                client_socket.send(menu.encode('utf-8'))

            elif command == "VIEW_ORDERED_ITEMS":
                menu = chef.view_ordered_items()
                client_socket.send(menu.encode('utf-8'))

            elif command == "VIEW_VOTED_ITEMS":
                menu = chef.view_voted_items()
                client_socket.send(menu.encode('utf-8'))

            elif command == "VIEW_GENERATED_RECOMMENDED_ITEMS":
                recommended_items = chef.view_generated_recommended_items()
                client_socket.send(recommended_items.encode('utf-8'))

            elif command == "GENERATE_REPORT":
                date_from = params[2]
                date_till = params[3]
                generated_report = chef.generate_report(date_from, date_till)
                client_socket.send(generated_report.encode('utf-8'))

            elif command == "VIEW_DELETED_ITEM_FEEDBACK":
                feedback_items = chef.view_deleted_items_feedback()
                client_socket.send(feedback_items.encode('utf-8'))

            elif command == "VIEW_ALL_MENU":
                all_items = chef.view_menu()
                client_socket.send(all_items.encode('utf-8'))

            elif command == "RECOMMEND_TOP_ITEMS":
                feedbackAnalyzer = FeedbackAnalyzer()
                feedbackAnalyzer.recommend_top_items()
                client_socket.send("Top items recommended successfully".encode('utf-8'))
                
            else:
                client_socket.send("Unknown command for Chef".encode('utf-8'))
                
        except Exception as e:
            client_socket.send(f"Error processing chef request: {e}".encode('utf-8'))
