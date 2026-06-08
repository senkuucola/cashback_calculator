"""
Графический интерфейс для калькулятора кэшбэка (Tkinter)
Не требует установки дополнительных библиотек
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from src.calc_module import calculate_cashback, BASE_RATES
from src.logger_module import log_result, log_start
from src.model import find_best_card


class CashbackCalculator:
    """Главный класс приложения"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💰 Калькулятор кэшбэка по банковской карте")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Данные
        self.purchases = []  # Список покупок [(категория, сумма), ...]
        self.bonuses = {}    # Словарь бонусов {категория: доп_процент}

        # Настройка стилей
        self.setup_styles()

        # Создание интерфейса
        self.create_widgets()

    def setup_styles(self):
        """Настройка цветов и стилей"""
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#4CAF50',
            'primary_dark': '#45a049',
            'blue': '#2196F3',
            'blue_dark': '#0b7dda',
            'red': '#f44336',
            'red_dark': '#d32f2f',
            'text': '#333333',
            'white': '#ffffff'
        }

        # Настройка стилей для ttk
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TNotebook.Tab', font=('Arial', 11, 'bold'), padding=[20, 5])
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10), background=self.colors['bg'])
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground=self.colors['blue'])
        style.configure('Total.TLabel', font=('Arial', 18, 'bold'), foreground=self.colors['primary'])

    def create_widgets(self):
        """Создание всех виджетов"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        header = ttk.Label(main_frame, text="КАЛЬКУЛЯТОР КЭШБЭКА ПО БАНКОВСКОЙ КАРТЕ", style='Header.TLabel')
        header.pack(pady=10)

        # Создаём вкладки
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)

        # Вкладка покупок
        self.purchases_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.purchases_frame, text="📋 Покупки")
        self.setup_purchases_tab()

        # Вкладка бонусов
        self.bonus_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.bonus_frame, text="🎁 Бонусы")
        self.setup_bonus_tab()

        # Вкладка результатов
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="💰 Результат")
        self.setup_result_tab()

        # Вкладка модели
        self.model_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.model_frame, text="📊 Сравнение карт")
        self.setup_model_tab()

        # Кнопка расчёта
        calc_button = tk.Button(main_frame, text="🧮 РАССЧИТАТЬ КЭШБЭК",
                                bg=self.colors['blue'], fg='white',
                                font=('Arial', 12, 'bold'),
                                command=self.calculate)
        calc_button.pack(fill=tk.X, pady=10)

        # Статусная строка
        self.status_var = tk.StringVar(value="✅ Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def setup_purchases_tab(self):
        """Настройка вкладки покупок"""
        # Панель добавления
        add_frame = ttk.LabelFrame(self.purchases_frame, text="➕ Добавить покупку", padding="10")
        add_frame.pack(fill=tk.X, pady=5, padx=5)

        # Категория
        ttk.Label(add_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_entry = ttk.Entry(add_frame, width=20)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)
        self.category_entry.bind('<Return>', lambda e: self.add_purchase())

        # Сумма
        ttk.Label(add_frame, text="Сумма (руб):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.amount_var = tk.StringVar(value="1000")
        self.amount_entry = ttk.Entry(add_frame, textvariable=self.amount_var, width=15)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)
        self.amount_entry.bind('<Return>', lambda e: self.add_purchase())

        # Кнопка добавления
        add_btn = tk.Button(add_frame, text="➕ Добавить", bg=self.colors['primary'],
                            fg='white', command=self.add_purchase)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Таблица покупок
        columns = ("Категория", "Сумма", "Действия")
        self.purchases_tree = ttk.Treeview(self.purchases_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.purchases_tree.heading(col, text=col)
            self.purchases_tree.column(col, width=200 if col == "Категория" else 100)

        self.purchases_tree.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Справочник категорий
        info_frame = ttk.LabelFrame(self.purchases_frame, text="📖 Базовые проценты кэшбэка", padding="10")
        info_frame.pack(fill=tk.X, pady=5, padx=5)

        info_text = tk.Text(info_frame, height=6, wrap=tk.WORD, bg=self.colors['bg'], font=('Arial', 10))
        info_text.pack(fill=tk.X)
        info_text.insert(tk.END, "Доступные категории:\n")
        for cat, rate in BASE_RATES.items():
            info_text.insert(tk.END, f"  • {cat}: {rate}%\n")
        info_text.insert(tk.END, "  • другие категории: 0.5%")
        info_text.config(state=tk.DISABLED)

    def setup_bonus_tab(self):
        """Настройка вкладки бонусов"""
        # Панель добавления
        add_frame = ttk.LabelFrame(self.bonus_frame, text="🎯 Добавить повышенный кэшбэк", padding="10")
        add_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(add_frame, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.bonus_category_entry = ttk.Entry(add_frame, width=20)
        self.bonus_category_entry.grid(row=0, column=1, padx=5, pady=5)
        self.bonus_category_entry.bind('<Return>', lambda e: self.add_bonus())

        ttk.Label(add_frame, text="Доп. %:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.bonus_percent_var = tk.StringVar(value="2")
        self.bonus_percent_entry = ttk.Entry(add_frame, textvariable=self.bonus_percent_var, width=10)
        self.bonus_percent_entry.grid(row=0, column=3, padx=5, pady=5)
        self.bonus_percent_entry.bind('<Return>', lambda e: self.add_bonus())

        add_btn = tk.Button(add_frame, text="🎁 Добавить бонус", bg=self.colors['primary'],
                            fg='white', command=self.add_bonus)
        add_btn.grid(row=0, column=4, padx=10, pady=5)

        # Таблица бонусов
        columns = ("Категория", "Дополнительный %", "Действия")
        self.bonus_tree = ttk.Treeview(self.bonus_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.bonus_tree.heading(col, text=col)
            self.bonus_tree.column(col, width=200 if col == "Категория" else 120)

        self.bonus_tree.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Лимит
        limit_frame = ttk.LabelFrame(self.bonus_frame, text="💰 Месячный лимит кэшбэка", padding="10")
        limit_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(limit_frame, text="Лимит (руб):").pack(side=tk.LEFT, padx=5)
        self.limit_var = tk.StringVar(value="3000")
        self.limit_entry = ttk.Entry(limit_frame, textvariable=self.limit_var, width=15)
        self.limit_entry.pack(side=tk.LEFT, padx=5)

    def setup_result_tab(self):
        """Настройка вкладки результатов"""
        # Таблица результатов
        columns = ("Категория", "Кэшбэк (руб)")
        self.result_tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=10)

        self.result_tree.heading("Категория", text="Категория")
        self.result_tree.heading("Кэшбэк (руб)", text="Кэшбэк (руб)")
        self.result_tree.column("Категория", width=300)
        self.result_tree.column("Кэшбэк (руб)", width=150)

        self.result_tree.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        # Итоговые метки
        self.total_label = tk.Label(self.result_frame, text="💰 Итого кэшбэк: 0.00 руб",
                                    font=('Arial', 16, 'bold'), fg=self.colors['primary'])
        self.total_label.pack(pady=10)

        self.remaining_label = tk.Label(self.result_frame, text="📊 Остаток лимита: 0.00 руб",
                                        font=('Arial', 12), fg=self.colors['text'])
        self.remaining_label.pack(pady=5)

    def setup_model_tab(self):
        """Настройка вкладки математической модели"""
        # Лучшая карта
        self.best_card_label = tk.Label(self.model_frame, text="🏆 ЛУЧШАЯ КАРТА: ",
                                        font=('Arial', 14, 'bold'), fg=self.colors['blue'])
        self.best_card_label.pack(pady=10)

        self.best_cashback_label = tk.Label(self.model_frame, text="Кэшбэк: 0.00 руб",
                                            font=('Arial', 12), fg=self.colors['primary'])
        self.best_cashback_label.pack(pady=5)

        # Таблица сравнения
        columns = ("Карта", "Кэшбэк (руб)", "Лимит карты (руб)")
        self.model_tree = ttk.Treeview(self.model_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.model_tree.heading(col, text=col)
            self.model_tree.column(col, width=250)

        self.model_tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)

    def add_purchase(self):
        """Добавление покупки"""
        category = self.category_entry.get().strip().lower()
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму (положительное число)")
            return

        if not category:
            messagebox.showerror("Ошибка", "Введите категорию покупки")
            return

        self.purchases.append((category, amount))

        # Добавляем в таблицу
        item_id = len(self.purchases) - 1
        self.purchases_tree.insert("", tk.END, iid=item_id,
                                   values=(category, f"{amount:.2f} руб", ""))

        # Добавляем кнопку удаления
        self.purchases_tree.column("Действия", width=80)
        del_btn = tk.Button(self.purchases_tree, text="🗑", bg=self.colors['red'],
                            fg='white', command=lambda: self.delete_purchase(item_id))
        self.purchases_tree.set(item_id, column="Действия", value="")
        self.purchases_tree.item(item_id, tags=('deletable',))

        # Очищаем поля
        self.category_entry.delete(0, tk.END)
        self.amount_var.set("1000")

        self.status_var.set(f"✅ Добавлено: {category} - {amount:.2f} руб")

    def delete_purchase(self, item_id):
        """Удаление покупки"""
        if 0 <= item_id < len(self.purchases):
            del self.purchases[item_id]
            self.purchases_tree.delete(item_id)
            # Обновляем статус
            self.status_var.set("✅ Покупка удалена")

    def add_bonus(self):
        """Добавление бонуса"""
        category = self.bonus_category_entry.get().strip().lower()
        try:
            percent = float(self.bonus_percent_var.get())
            if percent < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный процент (неотрицательное число)")
            return

        if not category:
            messagebox.showerror("Ошибка", "Введите категорию для бонуса")
            return

        self.bonuses[category] = self.bonuses.get(category, 0) + percent

        # Обновляем таблицу
        for item in self.bonus_tree.get_children():
            self.bonus_tree.delete(item)

        for cat, pct in self.bonuses.items():
            item_id = cat
            self.bonus_tree.insert("", tk.END, iid=item_id, values=(cat, f"{pct:.1f}%", ""))

            del_btn = tk.Button(self.bonus_tree, text="🗑", bg=self.colors['red'],
                                fg='white', command=lambda c=cat: self.delete_bonus(c))
            self.bonus_tree.set(item_id, column="Действия", value="")

        # Очищаем поля
        self.bonus_category_entry.delete(0, tk.END)
        self.bonus_percent_var.set("2")

        self.status_var.set(f"✅ Бонус добавлен: {category} +{percent}%")

    def delete_bonus(self, category):
        """Удаление бонуса"""
        if category in self.bonuses:
            del self.bonuses[category]
            self.bonus_tree.delete(category)
            self.status_var.set(f"✅ Бонус для {category} удалён")

    def calculate(self):
        """Основной расчёт"""
        if not self.purchases:
            messagebox.showwarning("Предупреждение", "Добавьте хотя бы одну покупку")
            return

        try:
            limit = float(self.limit_var.get())
            if limit < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный лимит")
            return

        # Логируем
        log_start()

        # Расчёт
        result = calculate_cashback(self.purchases, self.bonuses, limit)

        # Очищаем таблицу результатов
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

        # Заполняем таблицу результатов
        for category, cash in result['details'].items():
            self.result_tree.insert("", tk.END, values=(category.capitalize(), f"{cash:.2f} руб"))

        # Обновляем метки
        self.total_label.config(text=f"💰 Итого кэшбэк: {result['total']:.2f} руб")
        self.remaining_label.config(text=f"📊 Остаток лимита: {result['limit_remaining']:.2f} руб")

        # Логируем
        log_result(self.purchases, result['total'], limit, result['limit_remaining'])

        # Запускаем модель
        self.run_model()

        # Переключаемся на вкладку результатов
        self.notebook.select(self.result_frame)

        self.status_var.set(f"✅ Расчёт выполнен! Кэшбэк: {result['total']:.2f} руб")

    def run_model(self):
        """Запуск математической модели"""
        best = find_best_card(self.purchases)

        # Обновляем метки
        self.best_card_label.config(text=f"🏆 ЛУЧШАЯ КАРТА: {best['best_card']}")
        self.best_cashback_label.config(text=f"Кэшбэк: {best['best_cashback']:.2f} руб")

        # Очищаем таблицу
        for item in self.model_tree.get_children():
            self.model_tree.delete(item)

        # Заполняем таблицу
        for res in best['all_results']:
            self.model_tree.insert("", tk.END, values=(res['name'], f"{res['cashback']:.2f} руб", f"{res['limit']:.0f} руб"))

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


def main():
    """Главная функция"""
    app = CashbackCalculator()
    app.run()


if __name__ == "__main__":
    main()