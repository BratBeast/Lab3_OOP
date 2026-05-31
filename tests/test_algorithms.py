import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.algorithms.sorting import BubbleSort, QuickSort, BuiltInSortAdapter
from src.algorithms.factory import DataFactory


class TestSortingAlgorithms(unittest.TestCase):
    def setUp(self):
        self.algorithms = [BubbleSort(), QuickSort(), BuiltInSortAdapter()]

    def test_standard_array(self):
        """Перевірка стандартного невідсортованого масиву."""
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        for algo in self.algorithms:
            with self.subTest(algorithm=algo.name):
                self.assertEqual(algo.execute(data), expected)

    def test_empty_array(self):
        """Перевірка порожнього масиву."""
        for algo in self.algorithms:
            with self.subTest(algorithm=algo.name):
                self.assertEqual(algo.execute([]), [])

    def test_single_element(self):
        """Перевірка масиву з одним елементом."""
        for algo in self.algorithms:
            with self.subTest(algorithm=algo.name):
                self.assertEqual(algo.execute([42]), [42])

    def test_negative_numbers(self):
        """Перевірка масиву з від'ємними числами."""
        data = [3, -1, 4, -5, 9, 0]
        expected = [-5, -1, 0, 3, 4, 9]
        for algo in self.algorithms:
            with self.subTest(algorithm=algo.name):
                self.assertEqual(algo.execute(data), expected)

    def test_duplicates(self):
        """Перевірка масиву з дублікатами."""
        data = [5, 1, 5, 2, 1]
        expected = [1, 1, 2, 5, 5]
        for algo in self.algorithms:
            with self.subTest(algorithm=algo.name):
                self.assertEqual(algo.execute(data), expected)


class TestDataFactory(unittest.TestCase):
    def test_factory_random(self):
        data = DataFactory.create_data("random", 100)
        self.assertEqual(len(data), 100)

    def test_factory_sorted(self):
        data = DataFactory.create_data("sorted", 5)
        self.assertEqual(data, [1, 2, 3, 4, 5])

    def test_factory_reversed(self):
        data = DataFactory.create_data("reversed", 5)
        self.assertEqual(data, [5, 4, 3, 2, 1])


if __name__ == '__main__':
    unittest.main()