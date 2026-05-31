import time
from typing import Callable, Any


def timing_decorator(func: Callable) -> Callable:
    """
    Патерн Decorator.
    Обгортає функцію для вимірювання часу її виконання.
    """

    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()

        # Виклик оригінальної функції
        result = func(*args, **kwargs)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        # Поки що просто виводимо в консоль, потім зможемо передавати це в GUI
        print(f"[Metrics] Виконання зайняло: {elapsed_time:.6f} секунд")

        return result

    return wrapper