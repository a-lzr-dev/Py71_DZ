import datetime
import random


# Задание 1. Класс «Игровой персонаж»
# Создай класс GameCharacter, который описывает персонажа игры.
# Требования:
# 1. У персонажа есть имя, здоровье и уровень.
# 2. Здоровье хранится в приватном атрибуте.
# 3. Сделай property для здоровья, чтобы при попытке установить здоровье выше 100 оно автоматически становилось 100.
# 4. Сделай защищённый метод _level_up(), который увеличивает уровень на 1.
# 5. Добавь метод attack(other_character), который уменьшает здоровье другого персонажа на 10.
# 6. Сделай classmethod, который создаёт персонажа с максимальным здоровьем (100) и уровнем 1.
# 7. Сделай staticmethod, который сравнивает двух персонажей по уровню и возвращает того, у кого уровень выше.
class GameCharacter:

    def __init__(self, name: str, health: int, level: int):
        self.name = name
        self.health = health
        self.level = level

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        if value > 100:
            self._health = 100
        else:
            self._health = value

    def _level_up(self) -> None:
        self.level += 1

    def attack(self, other_character: GameCharacter) -> None:
        other_character.health -= 10

    @classmethod
    def create_new_hear(cls, name: str):
        return cls(name, level=1, health=100)

    @staticmethod
    def compare_level(self, other: GameCharacter) -> GameCharacter:
        return other if self.level < other.level else self

    def __str__(self) -> str:
        return f"{self.name} level: {self.level} health: {self.health}"


hero1 = GameCharacter.create_new_hear("Hero1")
hero2 = GameCharacter("Hero2", 55, 3)
print(GameCharacter.compare_level(hero1, hero2))  # Hero2 level: 2 health: 20


# Задание 2. Класс «Магазин»
# Создай класс Store, описывающий магазин.
# Требования:
# 1. Атрибуты:
# o название магазина;
# o список товаров (список словарей вида {"name": ..., "price": ..., "quantity": ...}).
# 2. Методы:
# o add_product(name, price, quantity) — добавить товар в магазин.
# o remove_product(name) — удалить товар по имени.
# o update_price(name, new_price) — изменить цену товара.
# o sell_product(name, quantity) — продать указанное количество товара (уменьшить остаток, если хватает).
# o get_inventory() — вернуть список всех товаров и их количество.
# o find_most_expensive() — вернуть самый дорогой товар.
# o find_cheapest() — вернуть самый дешёвый товар.
class Store:

    def __init__(self, name: str, goods: list[dict]):
        self.name = name
        self.goods = goods

    def add_product(self, name: str, price: int | float, quantity: int) -> None:
        # добавить товар в магазин
        self.goods.append({"name": name, "price": price, "quantity": quantity})

    def remove_product(self, name: str) -> bool:
        # удалить товар по имени
        for good in self.goods:
            if good['name'].lower() == name.lower():
                self.goods.remove(good)
                return True
        return False

    def update_price(self, name: str, new_price: int | float) -> None:
        # изменить цену товара
        if not isinstance(new_price, int | float):
            raise TypeError(f"Тип атрибута new_price {type(new_price)} не поддерживается")
        for good in self.goods:
            if good["name"] == name:
                good["price"] = new_price

    def sell_product(self, name: str, quantity: int) -> None:
        # продать указанное количество товара (уменьшить остаток, если хватает)
        for good in self.goods:
            if good["name"] == name:
                if good["quantity"] >= quantity:
                    good["quantity"] -= quantity
                else:
                    raise ValueError("Единиц товара не достаточно для продажи")

    def get_inventory(self) -> list[dict]:
        # вернуть список всех товаров и их количество
        return [{"name": item["name"], "quantity": item["quantity"]} for item in self.goods]

    def find_most_expensive(self) -> dict | None:
        # вернуть самый дорогой товар
        if not self.goods:
            return None
        return max(self.goods, key=lambda good: good["price"])

    def find_cheapest(self) -> dict | None:
        # вернуть самый дешёвый товар
        if not self.goods:
            return None
        return min(self.goods, key=lambda good: good["price"])


store = Store("store",
              [{"name": "bread", "price": 1.5, "quantity": 18}, {"name": "milk", "price": 3.5, "quantity": 28}])
print(
    store.get_inventory())  # [{'name': 'bread', 'price': 1.5, 'quantity': 18}, {'name': 'milk', 'price': 3.5, 'quantity': 28}]
print(store.find_most_expensive())  # {'name': 'milk', 'price': 3.5, 'quantity': 28}
print(store.find_cheapest())  # {'name': 'bread', 'price': 1.5, 'quantity': 18}


# Задание 3. Класс «Библиотека» и класс «Книга»
# Создай два класса: Book и Library.
# Book:
# • Атрибуты: название, автор, год издания, статус (в библиотеке или выдана).
# • Метод info() — выводит информацию о книге.
# • Метод mark_as_taken() — меняет статус на «выдана».
# • Метод mark_as_returned() — меняет статус на «в библиотеке».
# Library:
# • Атрибуты: название библиотеки, список книг.
# • Методы:
# o add_book(book) — добавляет книгу в библиотеку.
# o remove_book(book) — удаляет книгу из библиотеки.
# o find_by_author(author) — находит все книги автора.
# o find_by_year(year) — находит все книги указанного года.
# o available_books() — возвращает список всех книг, которые в библиотеке.
# o taken_books() — возвращает список всех выданных книг.
class Book:

    def __init__(self, name: str, author: str, year: int, is_available: bool = True):
        self.name = name
        self.author = author
        self.year = year
        self.is_available = is_available  # True - в библиотеке, False - выдана

    def info(self) -> str:
        # выводит информацию о книге
        return f"{self.name} {self.author} {self.year} {"в библиотеке" if self.is_available else "вадана"}"

    def mark_as_taken(self) -> None:
        # меняет статус на «выдана»
        self.is_available = False

    def mark_as_returned(self) -> None:
        # меняет статус на «в библиотеке».
        self.is_available = True


class Library:

    def __init__(self, name: str, books: list[Book]):
        self.name = name
        self.books = books

    def add_book(self, book: Book) -> None:
        # добавляет книгу в библиотеку
        self.books.append(book)

    def remove_book(self, book: Book) -> bool:
        # удаляет книгу из библиотеки
        for _book in self.books:
            if _book == book:
                self.books.remove(book)
                return True
        return False

    def find_by_author(self, author: str) -> list[Book]:
        # находит все книги автора
        return list(filter(lambda book: book.author.lower() == author.lower(), self.books))

    def find_by_year(self, year: int) -> list[Book]:
        # находит все книги указанного года
        return list(filter(lambda book: book.year == year, self.books))

    def available_books(self) -> list[Book]:
        # возвращает список всех книг, которые в библиотеке
        return list(filter(lambda book: book.is_available, self.books))

    def taken_books(self) -> list[Book]:
        # возвращает список всех выданных книг
        return list(filter(lambda book: not book.is_available, self.books))

    def __str__(self) -> str:
        return f"{self.name} books: {[item.info() for item in self.books]}"


book1 = Book(name="Book1", author="Author1", year=1990)
book2 = Book(name="Book2", author="Author2", year=1995)
book3 = Book(name="Book3", author="Author2", year=2000)
library = Library(name="Library1", books=[book1, book2, book3])


# Задание 4. Класс «Кошелёк»
# Создай класс Wallet, описывающий электронный кошелёк.
# Требования:
# 1. Приватный атрибут _balance.
# 2. Методы:
# o deposit(amount) — пополнить кошелёк.
# o withdraw(amount) — снять деньги (если хватает).
# o transfer_to(other_wallet, amount) — перевести деньги другому кошельку.
# o __apply_bonus() (приватный метод) — добавить 1% бонуса к балансу, вызывается автоматически после каждой операции пополнения.
# 3. property balance — позволяет просматривать баланс.
# 4. Статический метод wallet_info(wallet) — выводит краткую информацию о кошельке.
class Wallet:

    def __init__(self, balance: float):
        self._balance = balance

    def deposit(self, amount: float) -> None:
        # пополнить кошелёк
        self._balance += amount
        self.__apply_bonus()

    def withdraw(self, amount: float) -> None:
        # снять деньги (если хватает)
        if self._balance >= amount:
            self._balance -= amount
        else:
            raise ValueError(f"Не достаточно средств для операции")

    def transfer_to(self, other_wallet: Wallet, amount: float) -> None:
        # перевести деньги другому кошельку.
        if self._balance >= amount:
            self._balance -= amount
            other_wallet._balance += amount
        else:
            raise ValueError(f"Не достаточно средств для операции")

    def __apply_bonus(self) -> None:
        # добавить 1% бонуса к балансу, вызывается автоматически после каждой операции пополнения.
        self._balance += self._balance * 0.01

    @property
    def balance(self) -> float:
        # позволяет просматривать баланс
        return self._balance

    @staticmethod
    def wallet_info(wallet: Wallet) -> str:
        # выводит краткую информацию о кошельке
        return f"Баланс вашего счета = {wallet.balance}"


wallet1 = Wallet(0)
wallet1.deposit(1000)
print(Wallet.wallet_info(wallet1))  # Баланс вашего счета = 1010.0


# Задание 5. Класс «Система заказов»
# Создай класс Order и класс OrderSystem.
# Order:
# • Атрибуты: номер заказа, список товаров (список словарей {"name": ..., "price": ..., "quantity": ...}), статус заказа.
# • Методы:
# o calculate_total() — возвращает сумму заказа.
# o add_item(name, price, quantity) — добавляет товар в заказ.
# o remove_item(name) — удаляет товар из заказа.
# o change_status(status) — изменяет статус заказа (например, «новый», «в работе», «завершён»).
# OrderSystem:
# • Атрибуты: список всех заказов.
# • Методы:
# o create_order() — создаёт новый заказ.
# o get_order_by_id(order_id) — возвращает заказ по номеру.
# o get_total_revenue() — возвращает общую сумму по всем завершённым заказам.
# o list_orders_by_status(status) — возвращает все заказы с определённым статусом.
class Order:

    def __init__(self, order_id: int, goods: list[dict], status: str):
        self.order_id = order_id
        self.goods = goods
        self.status = status

    def calculate_total(self) -> float:
        # возвращает сумму заказа
        return sum(good["price"] * good["quantity"] for good in self.goods)

    def add_item(self, name: str, price: float, quantity: int) -> None:
        # добавляет товар в заказ
        self.goods.append({"name": name, "price": price, "quantity": quantity})

    def remove_item(self, name: str) -> bool:
        # удаляет товар из заказа
        for good in self.goods:
            if good['name'].lower() == name.lower():
                self.goods.remove(good)
                return True
        return False

    def change_status(self, status: str) -> None:
        # изменяет статус заказа (например, «новый», «в работе», «завершён»)
        self.status = status


class OrderSystem:

    def __init__(self, orders: list[Order]):
        self.orders = orders

    def create_order(self, goods: list[dict]) -> Order:
        # создаёт новый заказ
        order_id = max([order.order_id for order in self.orders]) + 1 if self.orders else 1
        new_order = Order(order_id, goods, status="новый")
        self.orders.append(new_order)
        return new_order

    def get_order_by_id(self, order_id: str) -> Order:
        # возвращает заказ по номеру
        found_orders = list(filter(lambda order: order.order_id.lower() == order_id.lower(), self.orders))
        if not found_orders:
            raise ValueError(f"Заказ с номером '{order_id}' не найден")
        return found_orders[0]

    def get_total_revenue(self) -> float:
        # возвращает общую сумму по всем завершённым заказам
        return sum(order.calculate_total() if order.status == "завершен" else 0 for order in self.orders)

    def list_orders_by_status(self, status: str) -> list[Order]:
        # возвращает все заказы с определённым статусом
        return list(filter(lambda order: order.status.lower() == status.lower(), self.orders))


my_orders = OrderSystem([])
order1 = my_orders.create_order([])
order1.add_item("good1", 100, 3)
order1.add_item("good2", 150, 2)
order1.add_item("good3", 200, 1)
order2 = my_orders.create_order([])
order2.add_item("good1", 100, 2)
order2.add_item("good2", 150, 5)
order2.add_item("good3", 200, 3)
order1.change_status(status="завершен")
print(my_orders.get_total_revenue())  # 800


# Задание 6. Класс «Автомобиль»
# Создай класс Car, описывающий автомобиль.
# Требования:
# 1. Атрибуты: марка, модель, год, уровень топлива (в литрах), пробег.
# 2. Методы:
# o drive(distance) — увеличить пробег и уменьшить топливо (расход 0.1 л на 1 км).
# o refuel(liters) — заправить автомобиль.
# o info() — вывести состояние автомобиля.
# o __check_fuel() (приватный) — проверяет, хватит ли топлива для поездки.
# o age() (метод экземпляра) — возвращает возраст автомобиля.
# 3. classmethod from_string(cls, data) — создаёт объект из строки вида "Toyota, Corolla, 2015".
class Car:

    def __init__(self, mark: str, model: str, year: int, liters: float = 0, distance: int = 0):
        self.mark = mark
        self.model = model
        self.year = year
        self.liters = liters
        self.distance = distance

    def drive(self, distance: int) -> None:
        # увеличить пробег и уменьшить топливо (расход 0.1 л на 1 км)
        if self.__check_fuel(distance):
            raise ValueError(f"Для поездки не хватает топлива")
        self.distance += distance
        self.liters -= distance / 10

    def refuel(self, liters: float) -> None:
        # заправить автомобиль
        self.liters += liters

    def info(self) -> None:
        # вывести состояние автомобиля
        print(f"Пройдено:{self.distance} км, остаток топлива: {self.liters} л")

    def __check_fuel(self, distance: float) -> bool:
        # (приватный) — проверяет, хватит ли топлива для поездки
        return self.liters >= distance / 10

    def age(self) -> int:
        # (метод экземпляра) — возвращает возраст автомобиля
        current_year = datetime.datetime.now().year
        return current_year - self.year if self.year <= current_year else 0

    @classmethod
    def from_string(cls, data: str) -> Car | None:
        # создаёт объект из строки вида "Toyota, Corolla, 2015"
        lst = data.split('-')
        if len(lst) == 3 and isinstance(lst[0], str) and isinstance(lst[1], str) and isinstance(lst[2], int):
            return Car(data[0], data[1], int(data[2]))
        raise ValueError("Создание невозможно: значение атрибута data некорректно")

# Задание 7. Класс «Игровой инвентарь»
# Создай класс Inventory, представляющий инвентарь игрока.
# Требования:
# 1. Атрибуты: список предметов (каждый предмет — словарь с полями name, weight, value).
# 2. Методы:
# o add_item(name, weight, value) — добавить предмет.
# o remove_item(name) — удалить предмет.
# o get_total_weight() — вернуть общий вес.
# o get_total_value() — вернуть общую стоимость.
# o find_heaviest() — найти самый тяжёлый предмет.
# o find_most_valuable() — найти самый дорогой предмет.
# o sort_by_value() — вернуть предметы, отсортированные по стоимости

class Inventory:

    def __init__(self, items: list[dict]):
        self.items = items

    def add_item(self, name: str, weight: float, value: float) -> dict:
        # добавить предмет
        new_item = {"name": name, "weight": weight, "value": value}
        self.items.append(new_item)
        return new_item

    def remove_item(self, name: str) -> bool:
        # удалить предмет
        for item in self.items:
            if item['name'].lower() == name.lower():
                self.items.remove(item)
                return True
        return False

    def get_total_weight(self) -> float:
        # вернуть общий вес
        return sum(item["weight"] for item in self.items)

    def get_total_value(self) -> float:
        # вернуть общую стоимость
        return sum(item["value"] for item in self.items)

    def find_heaviest(self) -> dict | None:
        # найти самый тяжёлый предмет
        if not self.items:
            return None
        return max(self.items, key=lambda item: item["weight"])

    def find_most_valuable(self) -> dict | None:
        # найти самый дорогой предмет
        if not self.items:
            return None
        return max(self.items, key=lambda item: item["value"])

    def sort_by_value(self) -> list[dict] | None:
        # вернуть предметы, отсортированные по стоимости
        if not self.items:
            return None
        return sorted(self.items, key=lambda item: item["value"])


inventory = Inventory([])
print(inventory.find_heaviest())  # None
inventory.add_item("item1", 10, 300)
inventory.add_item("item2", 20, 200)
inventory.add_item("item2", 30, 500)
print(inventory.get_total_value())  # 1000
print(
    inventory.sort_by_value())  # [{'name': 'item2', 'weight': 20, 'value': 200}, {'name': 'item1', 'weight': 10, 'value': 300}, {'name': 'item2', 'weight': 30, 'value': 500}]


# Задание 8. Класс «Тренажёрный зал»
# Создай класс Gym.
# Требования:
# 1. Атрибуты: название зала, список клиентов (имя, возраст, абонемент активен/не активен).
# 2. Методы:
# o add_client(name, age) — добавить клиента.
# o remove_client(name) — удалить клиента.
# o activate_membership(name) — активировать абонемент клиента.
# o deactivate_membership(name) — деактивировать абонемент.
# o get_active_members() — вернуть список клиентов с активным абонементом.
# o find_youngest_client() — вернуть самого молодого клиента.
# o find_oldest_client() — вернуть самого старшего клиента.
# o average_age() — средний возраст клиентов.

class Gym:

    def __init__(self, name: str, clients: list[dict]):
        self.name = name
        self.clients = clients

    def add_client(self, name: str, age: int) -> dict:
        # добавить клиента
        new_client = {"name": name, "age": age, "status": False}
        self.clients.append(new_client)
        return new_client

    def remove_client(self, name: str) -> bool:
        # удалить клиента
        for client in self.clients:
            if client['name'].lower() == name.lower():
                self.clients.remove(client)
                return True
        return False

    def activate_membership(self, name: str) -> None:
        # активировать абонемент клиента
        for client in self.clients:
            if client['name'].lower() == name.lower():
                client['status'] = True

    def deactivate_membership(self, name: str) -> None:
        # деактивировать абонемент
        for client in self.clients:
            if client['name'].lower() == name.lower():
                client['status'] = False

    def get_active_members(self) -> list[dict]:
        # вернуть список клиентов с активным абонементом.
        return list(filter(lambda client: client["status"], self.clients))

    def find_youngest_client(self) -> dict | None:
        # вернуть самого молодого клиента
        if not self.clients:
            return None
        return min(self.clients, key=lambda client: client["age"])

    def find_oldest_client(self) -> dict | None:
        # вернуть самого старшего клиента
        if not self.clients:
            return None
        return max(self.clients, key=lambda client: client["age"])

    def average_age(self) -> float | None:
        # средний возраст клиентов.
        if self.clients:
            return sum(client["age"] for client in self.clients) / len(self.clients)
        else:
            return None


gym = Gym("", [])
print(gym.find_youngest_client())  # None
print(gym.find_oldest_client())  # None
print(gym.average_age())  # None


# Задание 9. Класс «Музыкальный плейлист»
# Цель: много методов для управления коллекцией и сортировки.
# Описание:
# Создай класс Playlist.
# Требования:
# 1. Атрибуты: название плейлиста, список треков (название, исполнитель, длительность в секундах).
# 2. Методы:
# o add_track(name, artist, duration) — добавить трек.
# o remove_track(name) — удалить трек.
# o total_duration() — общая длительность всех треков.
# o find_by_artist(artist) — найти все треки исполнителя.
# o longest_track() — найти самый длинный трек.
# o shortest_track() — найти самый короткий трек.
# o shuffle() — перемешать треки в случайном порядке.
# o sort_by_duration(reverse=False) — сортировать треки по длительности.

class Playlist:

    def __init__(self, name: str, tracks: list[dict]):
        self.name = name
        self.tracks = tracks

    def add_track(self, name: str, artist: str, duration: int) -> dict:
        # добавить трек
        new_track = {"name": name, "artist": artist, "duration": duration}
        self.tracks.append(new_track)
        return new_track

    def remove_track(self, name: str) -> bool:
        # удалить трек
        for track in self.tracks:
            if track['name'].lower() == name.lower():
                self.tracks.remove(track)
                return True
        return False

    def total_duration(self) -> int:
        # общая длительность всех треков
        return sum(track["duration"] for track in self.tracks)

    def find_by_artist(self, artist: str) -> list[dict]:
        # найти все треки исполнителя
        return list(filter(lambda track: track["artist"].lower() == artist.lower(), self.tracks))

    def longest_track(self) -> dict | None:
        # найти самый длинный трек
        if not self.tracks:
            return None
        return max(self.tracks, key=lambda track: track["duration"])

    def shortest_track(self) -> dict | None:
        # найти самый короткий трек
        if not self.tracks:
            return None
        return min(self.tracks, key=lambda track: track["duration"])

    def shuffle(self) -> None:
        # перемешать треки в случайном порядке
        random.shuffle(self.tracks)

    def sort_by_duration(self, reverse: bool = False) -> list[dict] | None:
        # сортировать треки по длительности
        if not self.tracks:
            return None
        return sorted(self.tracks, key=lambda track: track["duration"], reverse=reverse)


playlist = Playlist("playlist1", [{"name": "track1", "artist": "artist1", "duration": 65},
                                  {"name": "track2", "artist": "artist2", "duration": 95},
                                  {"name": "track3", "artist": "artist3", "duration": 75},
                                  {"name": "track5", "artist": "artist5", "duration": 70}])
playlist.shuffle()
print(playlist.tracks)
playlist.shuffle()
print(playlist.tracks)
print(playlist.sort_by_duration()) # [{'name': 'track1', 'artist': 'artist1', 'duration': 65}, {'name': 'track5', 'artist': 'artist5', 'duration': 70}, {'name': 'track3', 'artist': 'artist3', 'duration': 75}, {'name': 'track2', 'artist': 'artist2', 'duration': 95}]

# Задание 10. Класс «Учебная группа»
# Цель: объединение нескольких объектов в один класс-менеджер.
# Описание:
# Создай класс Student и класс StudyGroup.
# Student:
# • Атрибуты: имя, оценки (список чисел).
# • Методы:
# o add_grade(grade) — добавить оценку.
# o average_grade() — вернуть среднюю оценку.
# o info() — вывести информацию об ученике.
# StudyGroup:
# • Атрибуты: название группы, список студентов.
# • Методы:
# o add_student(student) — добавить ученика.
# o remove_student(name) — удалить ученика по имени.
# o find_best_student() — найти ученика с лучшей средней оценкой.
# o group_average() — средняя оценка по группе.
# o list_students() — вывести список всех студентов.

class Student:

    def __init__(self, name: str, grades: list[int]):
        self.name = name
        self.grades = grades

    def add_grade(self, grade: int) -> None:
        # добавить оценку
        self.grades.append(grade)

    def average_grade(self) -> float | None:
        # вернуть среднюю оценку
        if not self.grades:
            return None
        return sum(self.grades) / len(self.grades)

    def info(self) -> None:
        # вывести информацию об ученике
        print(f'Имя: {self.name}, средняя оценка: {self.average_grade()}')


class StudyGroup:

    def __init__(self, name: str, students: list[Student]):
        self.name = name
        self.students = students

    def add_student(self, student: Student) -> None:
        # добавить ученика
        self.students.append(student)

    def remove_student(self, name: str) -> bool:
        # удалить ученика по имени
        for student in self.students:
            if student.name.lower() == name.lower():
                self.students.remove(student)
                return True
        return False

    def find_best_student(self) -> Student | None:
        # найти ученика с лучшей средней оценкой
        if not self.students:
            return None
        return max(self.students, key=lambda student: student.average_grade())

    def group_average(self) -> float | None:
        # средняя оценка по группе
        if self.students:
            return sum(student.average_grade() for student in self.students) / len(self.students)
        else:
            return None

    def list_students(self) -> None:
        # вывести список всех студентов
        if not self.students:
            print("Список студентов пуст")
        else:
            for student in self.students:
                print(student)

group = StudyGroup("group1", [])
group.add_student(Student("student1", [5, 2, 4, 5]))
group.add_student(Student("student2", [2, 4, 3, 3]))
group.add_student(Student("student3", [5, 4, 4, 4]))

print(group.find_best_student().name) # student3
print(group.group_average()) # 3.75