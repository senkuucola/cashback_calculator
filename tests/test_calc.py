import unittest
from src.calc_module import calculate_cashback


class TestCashbackCalculator(unittest.TestCase):

    def test_single_purchase(self):
        result = calculate_cashback([('супермаркеты', 1000)], {}, 500)
        self.assertEqual(result['total'], 10.0)

    def test_multiple_purchases(self):
        result = calculate_cashback([('супермаркеты', 1000), ('аптеки', 500)], {}, 100)
        expected = 1000 * 0.01 + 500 * 0.03
        self.assertEqual(result['total'], expected)

    def test_limit_exceeded(self):
        result = calculate_cashback([('супермаркеты', 100000)], {}, 500)
        self.assertEqual(result['total'], 500)

    def test_with_bonus(self):
        result = calculate_cashback([('супермаркеты', 1000)], {'супермаркеты': 2}, 500)
        self.assertEqual(result['total'], 30.0)

    def test_unknown_category(self):
        result = calculate_cashback([('unknown', 1000)], {}, 500)
        self.assertEqual(result['total'], 5.0)


if __name__ == '__main__':
    unittest.main()