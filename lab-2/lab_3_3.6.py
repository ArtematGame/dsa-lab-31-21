import sys

print("Задание 3.6\n")

# Получение аргументов командной строки и преобразование в список целых чисел
# sys.argv[1:] - все аргументы после имени скрипта
numbers = [int(x) for x in sys.argv[1:]]

# Нахождение максимального элемента в массиве
max_number = max(numbers)

# Подсчет количества элементов, меньших максимального
# Генераторное выражение с условием x < max_number
count_less_than_max = sum(1 for x in numbers if x < max_number)

# Сумма элементов массива, которые больше 5
sum_greater_than_five = sum(x for x in numbers if x > 5)

# Вывод результатов
print("Максимальный элемент в массиве:", max_number)
print("Количество меньших значений, чем максимальный элемент:", 
      count_less_than_max)
print("Сумма чисел массива больше 5:", sum_greater_than_five)