from src.data.Database import Database
from src.Values.Values import menu_tables, user_profile_columns

class UserProfile:
    @staticmethod
    def update_profile(user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth):
        query = """
        INSERT INTO user_profiles (user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        diet_preference = VALUES(diet_preference),
        spice_level = VALUES(spice_level),
        cuisine_preference = VALUES(cuisine_preference),
        sweet_tooth = VALUES(sweet_tooth)
        """
        params = (user_id, diet_preference, spice_level, cuisine_preference, sweet_tooth)
        Database.execute_query(query, params)

    @staticmethod
    def get_user_profile(user_id):
        query = "SELECT * FROM user_profiles WHERE user_id = %s"
        result = Database.fetch_query(query, (user_id,))
        return result[0] if result else None

    @staticmethod
    def get_all_menu_items():
        query = "SELECT * FROM menu_items"
        return Database.fetch_query(query)

    @staticmethod
    def get_personalized_menu(user_id):
        user_profile = UserProfile.get_user_profile(user_id)
        if not user_profile:
            return []

        all_menu_items = UserProfile.get_all_menu_items()
        personalized_menu = []

        for item in all_menu_items:
            score = UserProfile.calculate_item_score(item, user_profile)
            if score > 0:
                personalized_menu.append((item, score))

        personalized_menu.sort(key=lambda x: (-x[1], x[0][1]))

        return [item[0] for item in personalized_menu]

    @staticmethod
    def calculate_item_score(item, user_profile):
        score = 0
        if item[menu_tables["diet_preference"]] == user_profile[user_profile_columns["diet_preference"]]: 
            score += 3
        elif (item[menu_tables["diet_preference"]] == 'Vegetarian' and user_profile[user_profile_columns["diet_preference"]] in ['Non Vegetarian', 'Eggetarian']) or \
            (item[menu_tables["diet_preference"]] == 'Eggetarian' and user_profile[user_profile_columns["diet_preference"]] == 'Non Vegetarian'):
            score += 1

        if item[menu_tables["spice_level"]] == user_profile[user_profile_columns["spice_level"]]: 
            score += 2
        elif (item[menu_tables["spice_level"]] == 'Medium' and user_profile[user_profile_columns["spice_level"]] in ['Low', 'High']) or \
            (user_profile[user_profile_columns["spice_level"]] == 'Medium' and item[menu_tables["spice_level"]] in ['Low', 'High']):
            score += 1
        if item[menu_tables["cuisine_preference"]] == user_profile[user_profile_columns["cuisine_preference"]]:  
            score += 2

        return score