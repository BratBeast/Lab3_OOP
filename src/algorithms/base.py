from abc import ABC, abstractmethod

class SortStrategy(ABC):
    def __init__(self):
        self.name = "Unknown Strategy"

    def execute(self, data: list, tick_callback=None) -> list:
        data_copy = data.copy()
        self._sort(data_copy, tick_callback)
        return data_copy

    @abstractmethod
    def _sort(self, data: list, tick_callback=None):
        pass