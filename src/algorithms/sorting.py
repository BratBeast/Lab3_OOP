from src.algorithms.base import SortStrategy
from src.algorithms.metrics import timing_decorator


class BubbleSort(SortStrategy):
    def __init__(self):
        super().__init__()
        self.name = "Bubble Sort"

    @timing_decorator
    def _sort(self, data: list, tick_callback=None):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    if tick_callback:
                        tick_callback(data)


class QuickSort(SortStrategy):
    def __init__(self):
        super().__init__()
        self.name = "Quick Sort"

    @timing_decorator
    def _sort(self, data: list, tick_callback=None):
        self._quick_sort_recursive(data, 0, len(data) - 1, tick_callback)

    def _quick_sort_recursive(self, data, low, high, tick_callback):
        if low < high:
            pi = self._partition(data, low, high, tick_callback)
            self._quick_sort_recursive(data, low, pi - 1, tick_callback)
            self._quick_sort_recursive(data, pi + 1, high, tick_callback)

    def _partition(self, data, low, high, tick_callback):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                if tick_callback:
                    tick_callback(data)

        data[i + 1], data[high] = data[high], data[i + 1]
        if tick_callback:
            tick_callback(data)
        return i + 1


class BuiltInSortAdapter(SortStrategy):
    def __init__(self):
        super().__init__()
        self.name = "Python Built-in Sort (Timsort)"

    @timing_decorator
    def _sort(self, data: list, tick_callback=None):
        data.sort()
        if tick_callback:
            tick_callback(data)