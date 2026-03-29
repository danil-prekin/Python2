import unittest
from app import app

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_registration(self):
        data = {
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456',
            'comment': 'Some comment'
        }
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_missing_required_fields(self):
        data = {'email': 'test@example.com'}
        response = self.app.post('/registration', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Phone', response.data)
        self.assertIn(b'Name', response.data)
        self.assertIn(b'Address', response.data)
        self.assertIn(b'Index', response.data)

    def test_invalid_email_format(self):
        data = {
            'email': 'not-an-email',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Email', response.data)
        self.assertIn(b'Некорректный формат', response.data)

    def test_phone_length_invalid(self):
        data = {
            'email': 'test@example.com',
            'phone': '12345',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Phone', response.data)
        self.assertIn(b'10 цифр', response.data)

    def test_phone_not_number(self):
        data = {
            'email': 'test@example.com',
            'phone': 'abc',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Phone', response.data)

    def test_index_length_valid_5(self):
        data = {
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '12345'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Registration successful', response.data)

    def test_index_length_invalid(self):
        data = {
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Index', response.data)
        self.assertIn(b'5 или 6', response.data)

    def test_comment_optional(self):
        data = {
            'email': 'test@example.com',
            'phone': '1234567890',
            'name': 'Иван',
            'address': 'Москва',
            'index': '123456'
        }
        response = self.app.post('/registration', data=data)
        self.assertIn(b'Registration successful', response.data)

if __name__ == '__main__':
    unittest.main()
