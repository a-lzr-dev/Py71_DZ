from time import sleep

# 1. Создать родительский класс auto, у которого есть атрибуты: brand, age, color, mark и weight. А так же методы: move, birthday и stop.
# Методы move и stop выводят сообщение на экран "move" и "stop", а birthday увеличивает атрибут age на 1.
# Атрибуты brand, age и mark являются обязательными при объявлении объекта.
class Auto:

    def __init__(self, brand: str, age: int, mark: str, color: str = None, weight: int = None):
        self.brand = brand
        self.age = age
        self.mark = mark
        self.color = color
        self.weight = weight

    def birthday(self):
        self.age += self.age

    def move(self):
        print("move")

    def stop(self):
        print("stop")

# 2. Создать 2 класса truck и car, которые являютя наследниками класса auto. Класс truck имеет дополнительный атрибут max_load.
# Переопределенный метод move, перед появлением надписи "move" выводит надпись "attention", его реализацию сделать при помощи оператора super.
# А так же дополнительный метод load. При его вызове происходит пауза 1 сек., затем выдается сообщение "load" и снова пауза 1 сек.
# Класс car имеет дополнительный обязательный атрибут max_speed и при вызове метода move, после появления надписи "move" должна появиться надпись
# "max speed is <max_speed>". Создать по 2 объекта для каждого из классов truck и сar, проверить все их методы и атрибуты.
class Truck(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_load: int, color: str = None, weight: int = None):
        super().__init__(brand, age, mark, color, weight)
        self.max_load = max_load

    def move(self):
        super().move()
        print(f"attention")

    def load(self):
        sleep(1)
        print(f"attention")
        sleep(1)

class Car(Auto):

    def __init__(self, brand: str, age: int, mark: str, max_speed: int, color: str = None, weight: int = None):
        super().__init__(brand, age, mark, color, weight)
        self.max_speed = max_speed

    def move(self):
        super().move()
        print(f"max speed is {self.max_speed}")

truck1 = Truck(brand="Volvo", age=5, mark="Volvo FH 4x2", max_load=1000)
truck2 = Truck(brand="Scania", age=8, mark="Scania R420", max_load=2000)
car1 = Car(brand="Mazda", age=8, mark="Mazda CX5", max_speed=260)
car2 = Car(brand="VW", age=5, mark="Tiguan", max_speed=240)

truck1.birthday()
truck1.move()
truck1.load()
truck1.stop()

car1.birthday()
car1.move()
car1.stop()

# 3. Для рассмотренного на уроке класса Circle реализовать метод производящий вычитание двух окружностей, вычитание радиусов проивести по модулю.
# Если вычитаются две окружности с одинаковым значением радиуса, то результатом вычитания будет точка класса Point.

class Point:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f'point=({self.x}, {self.y})'

class Circle(Point):

    def __init__(self, radius, x: int, y: int):
        super().__init__(x, y)
        self.radius = radius

    def __str__(self):
        return f'{super().__str__()}, radius={self.radius}'

    def __sub__(self, circle):
        x = self.x - circle.x
        y = self.y - circle.y
        radius = abs(self.radius - circle.radius)
        return Circle(radius, x, y) if radius else Point(x,y)

circle_base = Circle(radius=5, x=0, y=0)
print(circle_base.__sub__(Circle(radius=5, x=0, y=0))) # point=(0, 0)
print(circle_base.__sub__(Circle(radius=15, x=0, y=0))) # point=(0, 0), radius=10