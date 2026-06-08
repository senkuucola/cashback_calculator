"""Модуль ввода данных пользователя."""

def input_purchases():
    """Ввод списка покупок. Возвращает list[(category, amount)]."""
    purchases = []
    print("\n" + "=" * 50)
    print("ВВОД ПОКУПОК")
    print("Формат: категория и сумма. Для завершения введите 'стоп'")
    print("Доступные категории: супермаркеты, аптеки, транспорт, кафе, развлечения, другое")
    print("-" * 50)

    while True:
        category = input("Категория: ").strip().lower()
        if category in ('стоп', 'stop', 'exit', 'конец'):
            break
        if not category:
            print("Категория не может быть пустой")
            continue
        try:
            amount = float(input("Сумма (руб): "))
            if amount <= 0:
                print("Сумма должна быть > 0")
                continue
            purchases.append((category, amount))
            print(f"✓ Добавлено: {category} - {amount:.2f} руб")
        except ValueError:
            print("Ошибка: введите число (например, 1500.50)")
    return purchases


def input_bonus_categories():
    """Ввод категорий с повышенным кэшбэком. Возвращает dict."""
    bonuses = {}
    print("\n" + "=" * 50)
    print("ПОВЫШЕННЫЙ КЭШБЭК")
    print("Введите категорию и дополнительный процент (например: транспорт 2)")
    print("Для завершения введите 'стоп'")
    print("-" * 50)

    while True:
        category = input("Категория: ").strip().lower()
        if category in ('стоп', 'stop', 'exit', 'конец'):
            break
        if not category:
            continue
        try:
            extra = float(input("Дополнительный процент (%): "))
            if extra < 0:
                print("Процент не может быть отрицательным")
                continue
            bonuses[category] = extra
            print(f"✓ Бонус: {category} +{extra}%")
        except ValueError:
            print("Ошибка: введите число")
    return bonuses


def input_limit():
    """Ввод месячного лимита кэшбэка."""
    print("\n" + "=" * 50)
    print("МЕСЯЧНЫЙ ЛИМИТ")
    while True:
        try:
            limit = float(input("Введите лимит (руб): "))
            if limit < 0:
                print("Лимит не может быть отрицательным")
                continue
            return limit
        except ValueError:
            print("Ошибка: введите число")