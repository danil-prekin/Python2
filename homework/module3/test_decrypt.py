import unittest
from decrypt import decrypt


class DecryptTestCase(unittest.TestCase):
    def test_single_dot(self):
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("1..2.3", "23"),
            ("абр......a.", "a"),
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot(self):
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            (" абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_only_dots(self):
        test_cases = [
            ("абра........", ""),
            (".", ""),
            ("1.......................", ""),
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)


if __name__ == '__main__':
    unittest.main()
