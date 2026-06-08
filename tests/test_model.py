import unittest
from src.model import find_best_card


class TestModel(unittest.TestCase):
    def test_supermarket_card(self):
        result = find_best_card([('супермаркеты', 10000)])
        self.assertEqual(result['best_card'], 'Карта "Супермаркет+"')

    def test_transport_card(self):
        result = find_best_card([('транспорт', 10000)])
        self.assertEqual(result['best_card'], 'Карта "Транспортная"')


if __name__ == '__main__':
    unittest.main()