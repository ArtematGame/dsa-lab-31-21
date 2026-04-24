# test_class.py

import pytest
from triangle_class import Triangle, IncorrectTriangleSides

# Позитивные тесты
def test_create_equilateral():
    t = Triangle(2, 2, 2)
    assert t.triangle_type() == "equilateral"
    assert t.perimeter() == 6

def test_create_isosceles():
    t = Triangle(3, 3, 5)
    assert t.triangle_type() == "isosceles"
    assert t.perimeter() == 11

def test_create_nonequilateral():
    t = Triangle(3, 4, 5)
    assert t.triangle_type() == "nonequilateral"
    assert t.perimeter() == 12

def test_float_sides():
    t = Triangle(1.5, 2.0, 2.5)
    assert t.triangle_type() == "nonequilateral"
    assert t.perimeter() == 6.0

# Негативные тесты (проверка исключений)
def test_zero_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(0, 1, 1)

def test_negative_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 2, 3)

def test_violated_inequality():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 1, 3)

def test_non_numeric():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, "a")

def test_large_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(10, 2, 3)