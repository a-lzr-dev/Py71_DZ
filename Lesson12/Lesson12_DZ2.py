# Матрицы Создать класс Matrix, который будет реализовывать следующие возможности. Класс должен принимать список списков.
# Например:  m = Matrix([[-1, 3], [0, 1], [-2, 2]]) будет представлять матрицу
# Пункты синего цвета означают методы, которые должны возвращать новый экземпляр класса Matrix.
# Пункты зеленого цвета — это методы основанные на @classmethod
# • Сложение матриц (только одинаковых размерностей):
# • Вычитание матриц (точно так же).
# • Умножение матрицы на число.
# • Транспонирование матрицы:
# Пример:
# • Создает единичную матрицу размером m, n
# • Создает нулевую матрицу размером m, n
# • Создает диагональную матрицу из переданного списка
# • Возвращает размерность матрицы (кортеж)
# • Возвращает кол-во элементов в матрице
# • Возвращает сумму всех элементов матрицы
# • Возвращает новую матрицу, где вместо отрицательных чисел стоят нули
# • Возможность сравнения на равенство двух матриц
# • Переопределить метод __str__

class Matrix:

    def __init__(self, data: list[list]):
        self.data = data

    def __add__(self, other: Matrix | list[list]) -> Matrix:
        # Сложение матриц
        if isinstance(other, Matrix):
            if self.size() != other.size():
                raise ValueError(f"Размер матриц не совпадает")
            return Matrix(
                [[item1 + item2 for item1, item2 in zip(row1, row2)] for row1, row2 in zip(self.data, other.data)])

        if isinstance(other, list):
            if self.size() != Matrix(other).size():
                raise ValueError(f"Размер матриц не совпадает")
            return Matrix([[item1 + item2 for item1, item2 in zip(row1, row2)] for row1, row2 in zip(self.data, other)])

        raise TypeError(f"Тип атрибута {type(other)} не поддерживается")

    def __sub__(self, other: Matrix | list[list]) -> Matrix:
        # Вычитание матриц
        if isinstance(other, Matrix):
            if self.size() != other.size():
                raise ValueError(f"Размер матриц не совпадает")
            return Matrix(
                [[item1 - item2 for item1, item2 in zip(row1, row2)] for row1, row2 in zip(self.data, other.data)])

        if isinstance(other, list):
            if self.size() != Matrix(other).size():
                raise ValueError(f"Размер матриц не совпадает")
            return Matrix([[item1 - item2 for item1, item2 in zip(row1, row2)] for row1, row2 in zip(self.data, other)])

        raise TypeError(f"Тип атрибута {type(other)} не поддерживается")

    def __mul__(self, number: int | float) -> Matrix:
        # Умножение матрицы на число.
        if not isinstance(number, int | float):
            raise TypeError(f"Тип атрибута number ({type(number)}) не является числом")
        return Matrix([[item * number for item in row] for row in self.data])

    def __reversed__(self) -> Matrix:
        # Транспонирование матрицы
        return Matrix([list(row) for row in zip(*self.data)])

    @classmethod
    def identity_matrix(cls, m: int, n: int) -> Matrix | None:
        # Создает единичную матрицу размером m, n (на главной диагонали стоят единицы, а все остальные элементы равны нулю)
        if type(m) != int:
            raise TypeError(f"Тип атрибута m ({type(m)}) не является числом")
        if type(n) != int:
            raise TypeError(f"Тип атрибута n ({type(n)}) не является числом")
        return Matrix([[1 if i == j else 0 for j in range(n)] for i in range(m)])

    @classmethod
    def zero_matrix(cls, m: int, n: int) -> Matrix:
        # Создает нулевую матрицу размером m, n (все элементы которой равны нулю)
        if type(m) != int:
            raise TypeError(f"Тип атрибута m ({type(m)}) не является числом")
        if type(n) != int:
            raise TypeError(f"Тип атрибута n ({type(n)}) не является числом")
        return Matrix([[0 for _ in range(n)] for _ in range(m)])

    @classmethod
    def diagonal_matrix(cls, lst: list[int | float]) -> Matrix:
        # Создает диагональную матрицу из переданного списка
        if not isinstance(lst, list):
            raise TypeError(f"Тип атрибута lst ({type(lst)}) не является списком")
        return Matrix([[lst[i] if i == j else 0 for j in range(len(lst))] for i in range(len(lst))])

    def size(self) -> tuple:
        # Возвращает размерность матрицы (кортеж)
        return len(self.data), max([len(row) for row in self.data])

    def count(self) -> int:
        # Возвращает кол-во элементов в матрице
        return sum([len(row) for row in self.data])

    def sum(self) -> int:
        # Возвращает сумму всех элементов матрицы
        return sum([item for row in self.data for item in row])

    def zeroing_negative_numbers(self) -> Matrix:
        # Возвращает новую матрицу, где вместо отрицательных чисел стоят нули
        return Matrix([[0 if item < 0 else item for item in row] for row in self.data])

    def __eq__(self, other: Matrix | list[list]) -> bool | None:
        # Возможность сравнения на равенство двух матриц
        if isinstance(other, list):
            return self.data == other
        if isinstance(other, Matrix):
            return self.data == other.data
        raise TypeError(f"Тип атрибута {type(other)} не поддерживается")

    def __str__(self) -> str:
        return str(self.data)


matrix = Matrix([[-1, 3], [0, 1], [-2, 2]])
# Сложение матриц
print(matrix + [[1, 1], [1, 1], [1, 1]])  # [[0, 4], [1, 2], [-1, 3]]
print(matrix + Matrix([[1, 1], [1, 1], [1, 1]]))  # [[0, 4], [1, 2], [-1, 3]]
# Вычитание матриц
print(matrix - [[1, 1], [1, 1], [1, 1]])  # [[-2, 2], [-1, 0], [-3, 1]]
print(matrix - Matrix([[1, 1], [1, 1], [1, 1]]))  # [[-2, 2], [-1, 0], [-3, 1]]
# Умножение матрицы на число
print(matrix * 2)  # [[-2, 6], [0, 2], [-4, 4]]
# Транспонирование матрицы
print(matrix.__reversed__())  # [[-1, 0, -2], [3, 1, 2]]
# Размерность матрицы
print(matrix.size())  # (3, 2)
# Кол-во элементов матрицы
print(matrix.count())  # 6
# Сумма элементов матрицы
print(matrix.sum())  # 6
# Создание единичной матрицы
print(matrix.identity_matrix(3, 4))  # [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
# Создание нулевой матрицы
print(matrix.zero_matrix(3, 2))  # [[0, 0], [0, 0], [0, 0]]
# Создание диагональной матрицы
print(matrix.diagonal_matrix([1, 2, 3, 4]))  # [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]]
# Создание матрицы, где вместо отрицательных чисел стоят нули
print(matrix.zeroing_negative_numbers())  # [[0, 3], [0, 1], [0, 2]]
