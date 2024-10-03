from src.data.Database import Database
from src.Values.Values import menu_tables, user_profile_columns
from tabulate import tabulate

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
    def fetch_all_menu_items():
        query = "SELECT item_id, name, price, food_type, diet_type, spice_level, cuisine_type FROM menu_items"
        return Database.fetch_query(query)

    @staticmethod
    def get_personalized_menu(user_id):
        user_profile = UserProfile.get_user_profile(user_id)
        if not user_profile:
            return "No user profile found."
        all_menu_items = UserProfile.fetch_all_menu_items()
        if not all_menu_items:
            return "No menu items found."

        personalized_menu = []

        for item in all_menu_items:
            score = UserProfile.calculate_item_score(item, user_profile)
            if score > 0:
                personalized_menu.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6], score))

        personalized_menu.sort(key=lambda x: -x[7])

        headers = ["Item ID", "Name", "Price", "Food Type", "Diet Type", "Spice Level", "Cuisine Type", "Score"]
        return tabulate(personalized_menu, headers, tablefmt="pretty") if personalized_menu else "No personalized menu items found based on your preferences."

    @staticmethod
    def calculate_item_score(item, user_profile):
        score = 0
        if item[menu_tables["diet_preference"]] == user_profile[user_profile_columns["diet_preference"]]: 
            score += 3
        elif (item[menu_tables["diet_preference"]] == 'veg' and user_profile[user_profile_columns["diet_preference"]] in ['Non Veg', 'Egg']) or \
            (item[menu_tables["diet_preference"]] == 'Egg' and user_profile[user_profile_columns["diet_preference"]] == 'Non Veg'):
            score += 1

        if item[menu_tables["spice_level"]] == user_profile[user_profile_columns["spice_level"]]: 
            score += 2
        elif (item[menu_tables["spice_level"]] == 'Medium' and user_profile[user_profile_columns["spice_level"]] in ['Low', 'High']) or \
            (user_profile[user_profile_columns["spice_level"]] == 'Medium' and item[menu_tables["spice_level"]] in ['Low', 'High']):
            score += 1
        if item[menu_tables["cuisine_preference"]] == user_profile[user_profile_columns["cuisine_preference"]]:  
            score += 2

        return score