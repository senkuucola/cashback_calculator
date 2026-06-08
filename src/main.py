"""Главный модуль приложения."""

from src.input_module import input_purchases, input_bonus_categories, input_limit
from src.calc_module import calculate_cashback
from src.logger_module import log_result, log_start, log_error
from src.bonus_module import get_weekend_bonus
from src.model import find_best_card


def print_header(title):
    """Печать красивого заголовка."""
    print("\n" + "=" * 60)
    print(f"   {title}")
    print("=" * 60)


def main():
    """Основная функция."""
    print_header("КАЛЬКУЛЯТОР КЭШБЭКА ПО БАНКОВСКОЙ КАРТЕ")

    log_start()

    try:
        # 1. Ввод данных
        purchases = input_purchases()
        if not purchases:
            print("\n⚠️ Не введено ни одной покупки. Программа завершена.")
            return

        bonuses = input_bonus_categories()

        # Добавляем выходной бонус
        weekend_bonus = get_weekend_bonus()
        if weekend_bonus > 0:
            print(f"\n🎉 Сегодня выходной! +{weekend_bonus}% ко всем категориям")
            for cat in set([p[0] for p in purchases]):
                bonuses[cat] = bonuses.get(cat, 0) + weekend_bonus

        limit = input_limit()

        # 2. Расчёт
        result = calculate_cashback(purchases, bonuses, limit)

        # 3. Вывод результата
        print_header("РЕЗУЛЬТАТ РАСЧЁТА")
        print("┌" + "─" * 50 + "┐")
        for category, cash in result['details'].items():
            print(f"│ {category.capitalize():<30} {cash:>15.2f} руб │")
        print("├" + "─" * 50 + "┤")
        print(f"│ {'ИТОГО КЭШБЭК':<30} {result['total']:>15.2f} руб │")
        print(f"│ {'Остаток лимита':<30} {result['limit_remaining']:>15.2f} руб │")
        print("└" + "─" * 50 + "┘")

        # 4. Логирование
        log_result(purchases, result['total'], limit, result['limit_remaining'])

        # 5. Математическая модель
        print_header("МАТЕМАТИЧЕСКАЯ МОДЕЛЬ: ВЫБОР ЛУЧШЕЙ КАРТЫ")

        best = find_best_card(purchases)

        print("\n🏆 ЛУЧШАЯ КАРТА:")
        print(f"   {best['best_card']}")
        print(f"   Кэшбэк: {best['best_cashback']:.2f} руб")

        print("\n📊 Сравнение всех карт:")
        print("   " + "-" * 40)
        for res in best['all_results']:
            print(f"   • {res['name']:<30} {res['cashback']:>8.2f} руб (лимит: {res['limit']} руб)")

        print("\n" + "=" * 60)
        print("✅ Расчёт завершён!")

    except Exception as e:
        error_msg = f"Неожиданная ошибка: {str(e)}"
        print(f"\n❌ {error_msg}")
        log_error(error_msg)


if __name__ == "__main__":
    main()