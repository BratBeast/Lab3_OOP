import random


class DataFactory:
    """
    Патерн Factory Method.
    Відповідає за створення різних наборів вхідних даних для алгоритмів.
    """

    @staticmethod
    def create_data(data_type: str, size: int) -> list:
        if data_type == "random":
            return [random.randint(1, 1000) for _ in range(size)]
        elif data_type == "sorted":
            return list(range(1, size + 1))
        elif data_type == "reversed":
            return list(range(size, 0, -1))
        elif data_type == "nearly_sorted":
            data = list(range(1, size + 1))
            # Міняємо місцями кілька елементів
            swaps = max(1, size // 10)
            for _ in range(swaps):
                idx1, idx2 = random.randint(0, size - 1), random.randint(0, size - 1)
                data[idx1], data[idx2] = data[idx2], data[idx1]
            return data
        else:
            raise ValueError(f"Невідомий тип даних: {data_type}")