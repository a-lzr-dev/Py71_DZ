from enum import StrEnum
from typing import Callable

from ..models import User
from ..repositories.order import InsufficientPointsError, InsufficientProductError, OrderRepository
from ..repositories.product import Products
from ..repositories.ticket import Tickets
from ..repositories.user import Users


class Action(StrEnum):
    # список доступных команд
    show_products = "Товары"
    buy_product = "Купить"
    show_profile = "Профиль"
    use_ticket = "Тикет"
    registry = "Зарегистрироваться"
    authentification = "Войти"


class Menu:
    _user: User | None = None
    actions: dict[Action, Callable]

    @staticmethod
    def show_logo() -> None:
        # вывод заголовка программы
        print('              === Добро пожаловать в "Не магазин" ===')
        print('Здесь вы можете обменивать тикеты для того, чтобы приобретать товары\n')
        print('Для взаимодейсвтия используйте команды:\n')

    def init_actions(self) -> None:
        # инициализация меню
        if self._user:  # если осуществлен вход
            self.actions = {
                Action.show_products: self.action_show_products,
                Action.buy_product: self.action_buy_product,
                Action.show_profile: self.action_show_profile,
                Action.use_ticket: self.action_use_ticket
            }
        else:
            self.actions = {
                Action.show_products: self.action_show_products,
                Action.registry: self.action_registry,
                Action.authentification: self.action_authentification
            }

    def show_actions(self) -> None:
        # вывод списка элементов меню
        for i, action in enumerate(self.actions.keys(), 1):
            print(f"{i}. {action.value}")
        print("")

    def select_action(self) -> Action:
        # выбор меню
        while True:
            value = input("Выберите пункт: ")
            if value.isdigit():  # если введено числовое значение
                value = int(value)
                lst = list(self.actions.keys())
                if value <= 0 or value > len(lst):
                    action = None
                else:
                    action = list(self.actions.keys())[value - 1]
            elif value in Action:
                action = self.actions[Action(value)]
            else:
                action = None

            if action:
                return action

            print(f"Введите название или номер команды (от 1 до {len(list(self.actions.keys()))})")

    def action(self, action) -> None:
        # вызов события
        self.actions[action]()

    @staticmethod
    def action_finish() -> None:
        # ожидание завершения
        input("Нажмите Enter для продолжения...")

    def action_show_products(self):
        # отображение списка доступных товаров
        products = Products.get_products()
        print(f"{"ID":<8}{"Стоимость":<12}{"Кол-во":<10}{"Название":<10}")
        print("=" * 49)
        for product in products:
            print(f"{product.id:<8}{product.cost:<12}{product.count:<10}{product.name:<10}")
        self.action_finish()

    def action_registry(self) -> None:
        # регистрация
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        if Users.is_exist(login):
            print("Пользователь с таким именем уже зарегистрирован")
        else:
            self._user = Users.registry(login, password)
            print("Регистрация успешно завершена")
        self.action_finish()

    def action_authentification(self) -> None:
        # вход
        login = input("Введите логин: ")
        password = input("Введите пароль: ")
        self._user = Users.authentification(login, password)
        if self._user:
            print("Вход успешно завершен")
        else:
            print("Вход невозможен")
        self.action_finish()

    def action_buy_product(self):
        # купить
        value = input("Введите ID товара и кол-во (через пробел): ").strip()
        parts = value.split()
        if len(parts) != 2:
            print("Необходимо ввести два значения: ID товара и количество через пробел.")
        elif not parts[0].isdigit() or not parts[1].isdigit():
            print("ID товара и количество должны быть целыми числами.")
        else:
            product_id = int(parts[0])
            count = int(parts[1])

            product = Products.get_by_id(product_id)
            if product: # если товар найден
                try:
                    order_id = OrderRepository.create_order(self._user, product, count) # осуществление покупки
                    print(f"Заказ успешно создан, ID={order_id}")
                    print(f"У вас осталось - {self._user.points} поинтов")
                except InsufficientProductError as e:
                    print(e)
                except InsufficientPointsError as e:
                    print(e)
            else:
                print("Товара с указанным ID не найдено.")
        self.action_finish()

    def action_show_profile(self):
        # профиль
        print(f"=== {self._user.username} ===")
        print(f"Поинтов: {self._user.points}")
        print("\nЗаказы\n")
        orders = Users.orders(self._user)
        print(f"{"Дата заказа":<20} {"Кол-во":<12} {"Сумма":<10} {"Название":<10}")
        print("-" * 55)
        for order in orders:
            order_datetime, order_count, order_sum, product_name = order
            print(
                f"{order_datetime.strftime('%H:%M %d.%m.%Y'):<20} {order_count:<12} {order_sum:<10} {product_name:<10}")
        self.action_finish()

    def action_use_ticket(self):
        # обмен тикета
        uuid = input("Введите тикет: ")
        ticket = Tickets.get_ticket(uuid)  # получение тикета
        if Tickets.valid_ticket(ticket):  # проверка актуальности тикета
            points = Tickets.change_ticket(ticket, self._user)
            print("Вы успешно обменяли тикет на 20 поинтов!")
            print(f"Теперь у вас - {points} поинтов")
        else:
            print("Тикет с таким номером не доступен")
        self.action_finish()

    def run(self) -> None:
        self.show_logo()  # вывод заголовка программы
        self.init_actions()  # настройка меню
        self.show_actions()  # вывод меню
        self.action(self.select_action())  # выбор и вызов события
