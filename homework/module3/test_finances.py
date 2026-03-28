import unittest
from app import app, storage


class FinanceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        storage.clear()

    def setUp(self):
        storage.clear()

    def test_add_valid_date(self):
        response = self.app.get('/add/20250328/500')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добавлено 500 руб. за 20250328', response.get_data(as_text=True))

    def test_add_invalid_date_format(self):
        response = self.app.get('/add/2025-03-28/500')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Неверный формат даты', response.get_data(as_text=True))

    def test_add_invalid_month(self):
        response = self.app.get('/add/20251328/500')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Неверный месяц', response.get_data(as_text=True))

    def test_calculate_year_empty(self):
        response = self.app.get('/calculate/2025')
        self.assertEqual(response.status_code, 404)
        self.assertIn('трат нет', response.get_data(as_text=True))

    def test_calculate_year_with_data(self):
        self.app.get('/add/20250328/500')
        self.app.get('/add/20250329/200')
        response = self.app.get('/calculate/2025')
        self.assertIn('700', response.get_data(as_text=True))

    def test_calculate_month_empty(self):
        response = self.app.get('/calculate/2025/3')
        self.assertEqual(response.status_code, 404)
        self.assertIn('трат нет', response.get_data(as_text=True))

    def test_calculate_month_with_data(self):
        self.app.get('/add/20250328/500')
        self.app.get('/add/20250329/200')
        response = self.app.get('/calculate/2025/3')
        self.assertIn('700', response.get_data(as_text=True))

    def test_add_overwrites_storage(self):
        self.app.get('/add/20250328/500')
        self.app.get('/add/20250328/300')
        response = self.app.get('/calculate/2025/3')
        self.assertIn('800', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
