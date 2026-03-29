import unittest
from remote_exec import app

class RemoteExecTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_code(self):
        resp = self.app.post('/exec', data={'code': 'print(2+2)', 'timeout': 5})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'4', resp.data)

    def test_timeout_exceeded(self):
        resp = self.app.post('/exec', data={'code': 'import time; time.sleep(10)', 'timeout': 1})
        self.assertEqual(resp.status_code, 408)
        self.assertIn(b'timeout', resp.data)

    def test_invalid_form_missing_code(self):
        resp = self.app.post('/exec', data={'timeout': 5})
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'code', resp.data)

    def test_invalid_timeout_range(self):
        resp = self.app.post('/exec', data={'code': 'print(1)', 'timeout': 50})
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b'timeout', resp.data)

    def test_shell_injection_prevention(self):
        malicious = 'print(1)"; echo "hacked'
        resp = self.app.post('/exec', data={'code': malicious, 'timeout': 5})
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(b'hacked', resp.data)

    def test_resource_limitation(self):
        fork_bomb = 'import subprocess; subprocess.run(["python3", "-c", "while True: pass"])'
        resp = self.app.post('/exec', data={'code': fork_bomb, 'timeout': 2})
        self.assertIn(resp.status_code, (200, 408))

if __name__ == '__main__':
    unittest.main()
