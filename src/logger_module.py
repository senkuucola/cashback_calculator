"""Модуль логирования результатов."""

import logging

# Настройка логгера
logging.basicConfig(
    filename='cashback.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_result(purchases, total_cashback, limit, remaining):
    """Запись результата в лог-файл."""
    purchases_str = ", ".join([f"{cat}:{amt:.2f}₽" for cat, amt in purchases])
    message = (f"Покупки: [{purchases_str}] | "
               f"Кэшбэк: {total_cashback:.2f}₽ | "
               f"Лимит: {limit:.2f}₽ | "
               f"Остаток: {remaining:.2f}₽")
    logging.info(message)
    print(f"\n📝 Результат сохранён в файл cashback.log")


def log_start():
    """Запись начала расчёта."""
    logging.info("=== НОВЫЙ РАСЧЁТ ===")


def log_error(error_msg):
    """Запись ошибки."""
    logging.error(f"ОШИБКА: {error_msg}")