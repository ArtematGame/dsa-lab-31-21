# test_func.py

import unittest
from triangle_func import get_triangle_type, IncorrectTriangleSides

class TestTriangleFunc(unittest.TestCase):
    
    # Позитивные тесты
    def test_equilateral(self):
        self.assertEqual(get_triangle_type(2, 2, 2), "equilateral")
    
    def test_isosceles_1(self):
        self.assertEqual(get_triangle_type(3, 3, 5), "isosceles")
    
    def test_isosceles_2(self):
        self.assertEqual(get_triangle_type(5, 3, 5), "isosceles")
    
    def test_nonequilateral_int(self):
        self.assertEqual(get_triangle_type(3, 4, 5), "nonequilateral")
    
    def test_nonequilateral_float(self):
        self.assertEqual(get_triangle_type(1.5, 2.0, 2.5), "nonequilateral")
    
    # Негативные тесты
    def test_zero_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(0, 1, 1)
    
    def test_negative_side(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(-1, 2, 3)
    
    def test_triangle_inequality_violation(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 1, 3)
    
    def test_non_numeric(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(1, 2, "a")
    
    def test_side_sum_too_small(self):
        with self.assertRaises(IncorrectTriangleSides):
            get_triangle_type(10, 2, 3)

if __name__ == '__main__':
    unittest.main()