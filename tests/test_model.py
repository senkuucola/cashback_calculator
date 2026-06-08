import unittest
from src.model import find_best_card


class TestModel(unittest.TestCase):

    def test_best_card_for_supermarket(self):
        purchases = [('супермаркеты', 10000)]
        result = find_best_card(purchases)
        self.assertEqual(result['best_card'], 'Карта "Супермаркет+"')

    def test_best_card_for_transport(self):
        purchases = [('транспорт', 10000)]
        result = find_best_card(purchases)
        self.assertEqual(result['best_card'], 'Карта "Транспортная"')

    def test_limit_respected(self):
        purchases = [('супермаркеты', 1000000)]
        result = find_best_card(purchases)
        self.assertLessEqual(result['best_cashback'], 3000)


if __name__ == '__main__':
    unittest.main()