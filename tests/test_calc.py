import unittest
from src.calc_module import calculate_cashback


class TestCalc(unittest.TestCase):
    def test_single(self):
        result = calculate_cashback([('супермаркеты', 1000)], {}, 500)
        self.assertEqual(result['total'], 10.0)

    def test_limit(self):
        result = calculate_cashback([('супермаркеты', 100000)], {}, 500)
        self.assertEqual(result['total'], 500)

    def test_bonus(self):
        result = calculate_cashback([('супермаркеты', 1000)], {'супермаркеты': 2}, 500)
        self.assertEqual(result['total'], 30.0)


if __name__ == '__main__':
    unittest.main()