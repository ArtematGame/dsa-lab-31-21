# triangle_func.py

class IncorrectTriangleSides(Exception):
    pass

def get_triangle_type(side_a, side_b, side_c):
    # Проверка, что все аргументы – числа (int или float)
    if not all(isinstance(x, (int, float)) for x in (side_a, side_b, side_c)):
        raise IncorrectTriangleSides("Все стороны должны быть числами")
    
    # Проверка на положительность
    if side_a <= 0 or side_b <= 0 or side_c <= 0:
        raise IncorrectTriangleSides("Стороны должны быть положительными")
    
    # Проверка неравенства треугольника
    if (side_a + side_b <= side_c) or (side_a + side_c <= side_b) or (side_b + side_c <= side_a):
        raise IncorrectTriangleSides("Нарушено неравенство треугольника")
    
    # Определение типа
    if side_a == side_b == side_c:
        return "equilateral"
    elif side_a == side_b or side_b == side_c or side_a == side_c:
        return "isosceles"
    else:
        return "nonequilateral"