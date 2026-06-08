"""
Математическая модель выбора оптимальной карты.
Целевая функция: максимизация итогового кэшбэка.
Ограничение: кэшбэк ≤ лимит карты.
"""

# База данных карт
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


def calculate_card_cashback(purchases, card):
    """Расчёт кэшбэка для конкретной карты."""
    total = 0.0
    details = {}

    for category, amount in purchases:
        rate = card['rates'].get(category, card['rates'].get('другое', 0.5))
        cash = amount * rate / 100.0
        details[category] = details.get(category, 0.0) + cash
        total += cash

    if total > card['limit']:
        total = card['limit']

    return total, details


def find_best_card(purchases, cards=None):
    """Находит карту с максимальным кэшбэком."""
    if cards is None:
        cards = CARDS_DATABASE

    best_card = None
    best_cashback = -1.0
    best_details = None
    all_results = []

    for card in cards:
        cashback, details = calculate_card_cashback(purchases, card)
        all_results.append({
            'name': card['name'],
            'cashback': cashback,
            'limit': card['limit']
        })

        if cashback > best_cashback:
            best_cashback = cashback
            best_card = card['name']
            best_details = details

    return {
        'best_card': best_card,
        'best_cashback': best_cashback,
        'best_details': best_details,
        'all_results': all_results
    }