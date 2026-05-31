import sys
import os

# Додаємо корінь проєкту в sys.path, щоб Python бачив папку src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from src.algorithms.facade import AlgorithmFacade
from src.gui.app import AlgorithmVisualizerApp


def main():
    root = tk.Tk()
    root.geometry("850x550")

    # 1. Створюємо ядро (Facade)
    facade = AlgorithmFacade()

    # 2. Створюємо графічний інтерфейс
    app = AlgorithmVisualizerApp(root, facade)

    # 3. Запускаємо програму
    root.mainloop()


if __name__ == "__main__":
    main()