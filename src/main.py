"""Главный модуль приложения."""

from src.input_module import input_purchases, input_bonus_categories, input_limit
from src.calc_module import calculate_cashback
from src.logger_module import log_result, log_start, log_error
from src.bonus_module import get_weekend_bonus
from src.model import find_best_card


def main():
    print("\n" + "=" * 60)
    print("   КАЛЬКУЛЯТОР КЭШБЭКА ПО БАНКОВСКОЙ КАРТЕ")
    print("=" * 60)

    log_start()

    try:
        purchases = input_purchases()
        if not purchases:
            print("\n⚠️ Не введено ни одной покупки.")
            return

        bonuses = input_bonus_categories()

        weekend_bonus = get_weekend_bonus()
        if weekend_bonus > 0:
            print(f"\n🎉 Сегодня выходной! +{weekend_bonus}% ко всем категориям")
            for cat in set([p[0] for p in purchases]):
                bonuses[cat] = bonuses.get(cat, 0) + weekend_bonus

        limit = input_limit()

        result = calculate_cashback(purchases, bonuses, limit)

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ РАСЧЁТА:")
        print("-" * 40)
        for category, cash in result['details'].items():
            print(f"  {category.capitalize()}: {cash:.2f} руб")
        print("-" * 40)
        print(f"  ИТОГО: {result['total']:.2f} руб")
        print(f"  Остаток лимита: {result['limit_remaining']:.2f} руб")

        log_result(purchases, result['total'], limit, result['limit_remaining'])

        # Математическая модель
        print("\n" + "=" * 50)
        print("МАТЕМАТИЧЕСКАЯ МОДЕЛЬ:")
        best = find_best_card(purchases)
        print(f"\n🏆 Лучшая карта: {best['best_card']}")
        print(f"   Кэшбэк: {best['best_cashback']:.2f} руб")

    except Exception as e:
        log_error(str(e))
        print(f"\n❌ Ошибка: {e}")


if __name__ == "__main__":
    main()