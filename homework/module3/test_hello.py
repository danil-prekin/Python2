import unittest
from freezegun import freeze_time
from app import app  # предполагаем, что Flask-приложение в файле app.py


class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @freeze_time("2025-03-28")
    def test_can_get_correct_username_with_weekdate(self):
        response = self.app.get('/hello-world/Анна')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn('Анна', data)
        self.assertIn('пятницы', data) 

    @freeze_time("2025-03-30")  # воскресенье
    def test_weekday_sunday(self):
        response = self.app.get('/hello-world/Петр')
        self.assertIn('воскресенья', response.get_data(as_text=True))

    @freeze_time("2025-03-24") 
    def test_weekday_monday(self):
        response = self.app.get('/hello-world/Иван')
        self.assertIn('понедельника', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
