# 1. Создайте класс Soda (для определения типа газированной воды), принимающий  1 аргумент при инициализации (отвечающий за добавку к выбираемому лимонаду).
# В этом классе реализуйте метод show_my_drink(), выводящий на печать «Газировка и {ДОБАВКА}» в случае наличия добавки, а иначе отобразится следующая фраза: «Обычная газировка».

class Soda:

    def __init__(self, flavor: str):
        self.flavor = flavor

    def show_my_drink(self) -> str:
        print(f"{"Газировка и " + self.flavor if self.flavor else "Обычная газировка"}")

Soda("").show_my_drink()  # Обычная газировка
Soda("Карамель").show_my_drink()  # Газировка и Карамель

# 2. Требуется проверить, возможно ли из представленных отрезков условной длины сформировать треугольник.
# Для этого необходимо создать класс TriangleChecker, принимающий только положительные числа.
# С помощью метода is_triangle() возвращаются следующие значения (в зависимости от ситуации):
# – Ура, можно построить треугольник!; – С отрицательными числами ничего не выйдет!; – Нужно вводить только числа!; – Жаль, но из этого треугольник не сделать.

class TriangleChecker:

    def __init__(self, *args):
        self.args = args

    def is_triangle(self) -> str:
        if set(filter(lambda item: not isinstance(item, int | float), self.args)):
            return 'Нужно вводить только числа!'
        if min(self.args) < 0:
            return 'С отрицательными числами ничего не выйдет!'
        # если не 3 значения или если две стороны в сумме равны или меньше чем третья сторона
        if (len(self.args) != 3 or
                self.args[0] + self.args[1] <= self.args[2] or
                self.args[1] + self.args[2] <= self.args[0] or
                self.args[0] + self.args[2] <= self.args[1]):
            return 'Жаль, но из этого треугольник не сделать.'
        return 'Ура, можно построить треугольник!'

print(TriangleChecker(2, 2, "2").is_triangle())  # Нужно вводить только числа!
print(TriangleChecker(2, -2, 2).is_triangle())  # С отрицательными числами ничего не выйдет!
print(TriangleChecker(2, 2).is_triangle())  # Жаль, но из этого треугольник не сделать.
print(TriangleChecker(2, 2, 5).is_triangle())  # Жаль, но из этого треугольник не сделать.
print(TriangleChecker(2, 2, 2).is_triangle())  # Ура, можно построить треугольник!

# 3. Необходимо создать класс KgToPounds, в который принимает количество килограмм, а с помощью метода to_pounds() они переводятся в фунты.
# Необходимо закрыть доступ к переменной kg. Также, реализовать методы:
# - set_kg() - для задания нового значения килограммов (записывать только числовые значения),
# - get_kg() - для вывода текущего значения кг.
# Во второй версии необходимо использовать декоратор property для создания setter и getter взамен set_kg и get_kg.

class KgToPounds:

    def __init__(self, kg: float):
        self.set_kg(kg)

    def to_pounds(self) -> float:
        return self.get_kg() * 2.204623

    def get_kg(self) -> float:
        return self._kg

    def set_kg(self, kg) -> None:
        self._kg = kg

class KgToPounds2:

    def __init__(self, kg: float):
        self.kg = kg

    def to_pounds(self) -> float:
        return self.kg * 2.204623

    @property
    def kg(self) -> float:
        return self._kg

    @kg.setter
    def kg(self, kg) -> None:
        self._kg = kg

print(KgToPounds(1).to_pounds()) # 2.204623
print(KgToPounds2(1).to_pounds()) # 2.204623

# 4. Строки в Питоне сравниваются на основании значений символов. Т.е. если мы захотим выяснить, что больше: Apple или Яблоко, – то Яблоко окажется бОльшим.
# А все потому, что английская буква A имеет значение 65 (берется из таблицы кодировки), а русская буква Я – 1071.
# Надо создать новый класс RealString, который будет принимать строку и сравнивать по количеству входящих в них символов.
# Сравнивать между собой можно как объекты класса, так и обычные строки с экземплярами класса RealString.

class RealString:

    def __init__(self, s: str):
        self.s = s

    def __eq__(self, other) -> bool | None:
        if isinstance(other, RealString):
            return len(self.s) == len(other.s)
        elif isinstance(other, str):
            return len(self.s) == len(other)
        else:
            return None

print(RealString("123") == "1231") # False
print(RealString("123") == "122") # True
print(RealString("123") == RealString("111")) # True
print(RealString("123") == 1) # None

# 5. Напишите класс Rectangle, который имеет атрибуты: width (ширина) и height (высота). Класс должен иметь следующие методы:
# • Конструктор, который принимает два параметра: width и height, и инициализирует соответствующие атрибуты.
# • Метод str, который возвращает строковое представление объекта класса Rectangle в формате “Прямоугольник с шириной width и высотой height”.
# • Метод get_area, который возвращает площадь прямоугольника.
# • Метод get_perimeter, который возвращает периметр прямоугольника.
# • Метод is_square, который возвращает True, если прямоугольник является квадратом, и False в противном случае. Этот метод должен быть декорирован как property.

class Rectangle:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Прямоугольник с шириной {self.width} и высотой {self.height}"

    def get_area(self) -> int:
        return self.width * self.height

    def get_perimeter(self) -> int:
        return (self.width + self.height) * 2

    @property
    def is_square(self) -> bool:
        return self.width == self.height

# 6. Напишите класс Person, который имеет атрибуты name (имя), age (возраст) и gender (пол). Класс должен иметь следующие методы:
# • Конструктор, который принимает три параметра: name, age и gender, и инициализирует соответствующие атрибуты.
# • Метод str, который возвращает строковое представление объекта класса Person в формате “Имя: name, Возраст: age, Пол: gender”.
# • Метод get_name, который возвращает значение атрибута name.
# • Метод set_name, который принимает один параметр: new_name, и устанавливает значение атрибута name равным new_name. Этот метод должен быть декорирован как property.
# • Метод is_adult, который возвращает True, если возраст объекта больше или равен 18, и False в противном случае. Этот метод должен быть декорирован как staticmethod.
# • Метод create_from_string, который принимает один параметр: s, и создает и возвращает объект класса Person на основе строки s.
#  Строка s должна иметь формат “name-age-gender”, где name - имя, age - возраст и gender - пол. Этот метод должен быть декорирован как classmethod.

class Person:

    def __init__(self, name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Пол: {self.gender}"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @staticmethod
    def is_adult(self) -> bool:
        return True if self.age >= 18 else False

    @classmethod
    def create_from_string(cls, data: str) -> Person | None:
        lst = data.split('-')
        if len(lst) == 3 and isinstance(lst[0], str) and isinstance(lst[1], int) and isinstance(lst[2], str) :
            return Person(lst[0], int(lst[1]), lst[2])
        else:
            return None

person = Person("Igor", 10, "Male")
print(Person.is_adult(person))  # False
print(Person.create_from_string("Sergey-28-Male"))  # Имя: Sergey, Возраст: 28, Пол: Male