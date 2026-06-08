"""Модуль бонусов и акций."""

import datetime

def get_weekend_bonus():
    today = datetime.datetime.now().weekday()
    if today >= 5:
        return 0.5
    return 0.0