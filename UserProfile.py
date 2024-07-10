from Database import Database

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
        
        # Match diet preference
        if item[5] == user_profile[2]: 
            score += 3
        elif (item[5] == 'Vegetarian' and user_profile[1] in ['Non Vegetarian', 'Eggetarian']) or \
             (item[5] == 'Eggetarian' and user_profile[1] == 'Non Vegetarian'):
            score += 1

        # Match spice level
        if item[6] == user_profile[3]: 
            score += 2
        elif (item[6] == 'Medium' and user_profile[2] in ['Low', 'High']) or \
             (user_profile[2] == 'Medium' and item[6] in ['Low', 'High']):
            score += 1

        # Match cuisine preference
        if item[7] == user_profile[4]:  
            score += 2
        return score