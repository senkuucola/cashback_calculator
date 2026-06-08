"""Модуль бонусов и акций."""

import datetime


def get_weekend_bonus():
    """
    Возвращает дополнительный процент в выходные дни.
    Суббота (5) или Воскресенье (6) → +0.5%
    """
    today = datetime.datetime.now().weekday()
    if today >= 5:  # 5 = суббота, 6 = воскресенье
        return 0.5
    return 0.0


def apply_special_offer(bonuses, offer_category, extra_percent):
    """Добавляет специальную акцию для конкретной категории."""
    new_bonuses = bonuses.copy()
    new_bonuses[offer_category] = new_bonuses.get(offer_category, 0) + extra_percent
    return new_bonuses