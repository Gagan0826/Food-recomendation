from sentiment_words import positive_words, negative_words
from Database import Database

class FeedbackAnalyzer:

    @staticmethod
    def analyze_sentiment(comment):
        words = comment.lower().split()
        score = 0
        for word in words:
            if word in positive_words:
                score += 1
            elif word in negative_words:
                score -= 1
        return score

    @staticmethod
    def calculate_item_scores():
        query = "SELECT item_id, comment FROM feedback"
        feedbacks = Database.fetch_query(query)
        
        item_scores = {}
        for item_id, comment in feedbacks:
            score = FeedbackAnalyzer.analyze_sentiment(comment)
            if item_id in item_scores:
                item_scores[item_id] += score
            else:
                item_scores[item_id] = score

        return item_scores

    @staticmethod
    def recommend_top_items():
        item_scores = FeedbackAnalyzer.calculate_item_scores()
        top_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        
        Database.execute_query("TRUNCATE TABLE generated_recommended_items")
        for item_id, score in top_items:
            query = "INSERT INTO generated_recommended_items (item_id, score) VALUES (%s, %s)"
            Database.execute_query(query, (item_id, score))

if __name__ == "__main__":
    FeedbackAnalyzer.recommend_top_items()
