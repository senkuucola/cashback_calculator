"""Модуль основной логики расчёта кэшбэка."""

BASE_RATES = {
    'супермаркеты': 1.0,
    'аптеки': 3.0,
    'транспорт': 2.0,
    'кафе': 0.5,
    'развлечения': 1.5,
    'другое': 0.5
}


def calculate_cashback(purchases, bonuses, limit):
    details = {}
    total = 0.0

    for category, amount in purchases:
        base = BASE_RATES.get(category, BASE_RATES['другое'])
        extra = bonuses.get(category, 0.0)
        cash = amount * (base + extra) / 100.0
        details[category] = details.get(category, 0.0) + cash
        total += cash

    if total > limit:
        total = limit

    return {
        'details': details,
        'total': total,
        'limit_remaining': limit - total
    }