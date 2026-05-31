import time
from src.algorithms.sorting import BubbleSort, QuickSort, BuiltInSortAdapter
from src.algorithms.factory import DataFactory
from src.algorithms.config import SettingsManager


class AlgorithmFacade:
    def __init__(self):
        self.settings = SettingsManager()

        self._algorithms = {
            "Bubble Sort": BubbleSort(),
            "Quick Sort": QuickSort(),
            "Python Built-in (Timsort)": BuiltInSortAdapter()
        }

    def get_available_algorithms(self) -> list:
        return list(self._algorithms.keys())

    def get_available_data_types(self) -> list:
        return ["random", "sorted", "reversed", "nearly_sorted"]

    def run_algorithm(self, algo_name: str, data_type: str = "random", tick_callback=None) -> dict:
        if algo_name not in self._algorithms:
            raise ValueError(f"Алгоритм {algo_name} не знайдено!")

        size = self.settings.array_size
        original_data = DataFactory.create_data(data_type, size)
        strategy = self._algorithms[algo_name]

        # Додаємо заміри часу для експорту
        start_time = time.perf_counter()
        sorted_data = strategy.execute(original_data, tick_callback)
        exec_time = time.perf_counter() - start_time

        return {
            "algorithm": algo_name,
            "data_type": data_type,
            "size": size,
            "original_data": original_data,
            "sorted_data": sorted_data,
            "execution_time": exec_time
        }