"""Модуль основной логики расчёта кэшбэка."""

# Базовые проценты по категориям
BASE_RATES = {
    'супермаркеты': 1.0,
    'аптеки': 3.0,
    'транспорт': 2.0,
    'кафе': 0.5,
    'развлечения': 1.5,
    'другое': 0.5
}


def calculate_cashback(purchases, bonuses, limit):
    """
    Рассчитывает кэшбэк.

    Args:
        purchases: list of (category, amount)
        bonuses: dict {category: extra_percent}
        limit: float

    Returns:
        dict: {'details': dict, 'total': float, 'limit_remaining': float}
    """
    details = {}
    total = 0.0

    for category, amount in purchases:
        base = BASE_RATES.get(category, BASE_RATES['другое'])
        extra = bonuses.get(category, 0.0)
        cash = amount * (base + extra) / 100.0
        details[category] = details.get(category, 0.0) + cash
        total += cash

    # Применяем лимит
    if total > limit:
        total = limit

    return {
        'details': details,
        'total': total,
        'limit_remaining': limit - total
    }