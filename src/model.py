"""Математическая модель выбора оптимальной карты."""

CARDS_DATABASE = [
    {
        'name': 'Карта "Супермаркет+"',
        'rates': {'супермаркеты': 5.0, 'аптеки': 2.0, 'транспорт': 1.0,
                  'кафе': 1.0, 'развлечения': 1.0, 'другое': 0.5},
        'limit': 3000
    },
    {
        'name': 'Карта "Транспортная"',
        'rates': {'супермаркеты': 1.0, 'аптеки': 1.0, 'транспорт': 10.0,
                  'кафе': 0.5, 'развлечения': 2.0, 'другое': 0.5},
        'limit': 2000
    },
    {
        'name': 'Карта "Всё включено"',
        'rates': {'супермаркеты': 2.0, 'аптеки': 2.0, 'транспорт': 2.0,
                  'кафе': 2.0, 'развлечения': 2.0, 'другое': 2.0},
        'limit': 5000
    }
]


def find_best_card(purchases):
    best_card = None
    best_cashback = -1.0

    for card in CARDS_DATABASE:
        total = 0.0
        for category, amount in purchases:
            rate = card['rates'].get(category, card['rates'].get('другое', 0.5))
            total += amount * rate / 100.0
        if total > card['limit']:
            total = card['limit']

        if total > best_cashback:
            best_cashback = total
            best_card = card['name']

    return {'best_card': best_card, 'best_cashback': best_cashback}