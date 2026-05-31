import threading
from src.algorithms.base import SortStrategy
from src.algorithms.metrics import timing_decorator
from src.algorithms.config import SettingsManager


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


class ParallelMergeSort(SortStrategy):
    def __init__(self):
        super().__init__()
        self.name = "Parallel Merge Sort"

    @timing_decorator
    def _sort(self, data: list, tick_callback=None):
        # Отримуємо дозволену кількість потоків із Singleton
        threads_limit = SettingsManager().thread_count
        self._parallel_merge_sort(data, 0, len(data) - 1, threads_limit, tick_callback)

    def _parallel_merge_sort(self, data, left, right, threads_available, tick_callback):
        if left >= right:
            return

        mid = (left + right) // 2

        # Якщо є вільні потоки, розбиваємо задачу на два нових паралельних потоки
        if threads_available > 1:
            left_thread = threading.Thread(
                target=self._parallel_merge_sort,
                args=(data, left, mid, threads_available // 2, tick_callback)
            )
            right_thread = threading.Thread(
                target=self._parallel_merge_sort,
                args=(data, mid + 1, right, threads_available // 2, tick_callback)
            )

            left_thread.start()
            right_thread.start()

            # Чекаємо завершення обох потоків
            left_thread.join()
            right_thread.join()
        else:
            # Якщо ліміт потоків вичерпано, досортовуємо послідовно (в поточному потоці)
            self._parallel_merge_sort(data, left, mid, 1, tick_callback)
            self._parallel_merge_sort(data, mid + 1, right, 1, tick_callback)

        self._merge(data, left, mid, right, tick_callback)

    def _merge(self, data, left, mid, right, tick_callback):
        temp = []
        i, j = left, mid + 1

        while i <= mid and j <= right:
            if data[i] <= data[j]:
                temp.append(data[i])
                i += 1
            else:
                temp.append(data[j])
                j += 1

        while i <= mid:
            temp.append(data[i])
            i += 1
        while j <= right:
            temp.append(data[j])
            j += 1

        for idx, val in enumerate(temp):
            data[left + idx] = val
            if tick_callback:
                tick_callback(data)