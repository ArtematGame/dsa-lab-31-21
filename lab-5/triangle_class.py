# triangle_class.py

class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон."""
    pass

class Triangle:
    """
    Класс, представляющий треугольник по трём сторонам.
    """
    def __init__(self, side_a, side_b, side_c):
        """
        Конструктор.
        Проверяет корректность сторон и сохраняет их.
        """
        # Проверка типа (числа)
        if not all(isinstance(x, (int, float)) for x in (side_a, side_b, side_c)):
            raise IncorrectTriangleSides("Все стороны должны быть числами")
        
        # Проверка положительности
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise IncorrectTriangleSides("Стороны должны быть положительными")
        
        # Неравенство треугольника
        if (side_a + side_b <= side_c) or (side_a + side_c <= side_b) or (side_b + side_c <= side_a):
            raise IncorrectTriangleSides("Нарушено неравенство треугольника")
        
        self.a = side_a
        self.b = side_b
        self.c = side_c
    
    def triangle_type(self):
        """Возвращает тип треугольника: equilateral, isosceles, nonequilateral."""
        if self.a == self.b == self.c:
            return "equilateral"
        elif self.a == self.b or self.b == self.c or self.a == self.c:
            return "isosceles"
        else:
            return "nonequilateral"
    
    def perimeter(self):
        """Возвращает периметр треугольника."""
        return self.a + self.b + self.c