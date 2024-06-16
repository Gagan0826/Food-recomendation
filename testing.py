import unittest
from unittest.mock import patch
from datetime import date
from Chef import Chef
from Database import Database

class TestChef(unittest.TestCase):

    @patch('Database.Database.execute_query')
    def test_recommend_menu(self, mock_execute_query):
        chef = Chef(user_id=22, name='GaganChef')
        chef.recommend_menu(item_id=101, meal_type='Lunch')
        mock_execute_query.assert_called_once_with(
            "INSERT INTO chef_recommendation_menu (item_id, food_type, rolled_out_date) VALUES (%s, %s, %s)",
            (101, 'Lunch', date.today())
        )
'''
    @patch('your_module.Database.fetch_query')
    def test_view_menu(self, mock_fetch_query):
        mock_fetch_query.return_value = [
            {'item_id': 101, 'name': 'Test Item', 'description': 'Test Description'}
        ]
        chef = Chef(user_id=1, name='Test Chef')
        result = chef.view_menu()
        mock_fetch_query.assert_called_once_with(
            "SELECT * FROM menu_items WHERE item_id IN (SELECT item_id FROM chef_recommendation_menu)"
        )
        self.assertEqual(result, [
            {'item_id': 101, 'name': 'Test Item', 'description': 'Test Description'}
        ])

if __name__ == '__main__':
    unittest.main()
'''