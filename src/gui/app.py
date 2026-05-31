import tkinter as tk
from tkinter import ttk, messagebox
import time
from src.algorithms.facade import AlgorithmFacade
from src.gui.commands import RunAlgorithmCommand
from src.gui.memento import Caretaker


class AlgorithmVisualizerApp:
    def __init__(self, root, facade: AlgorithmFacade):
        self.root = root
        self.root.title("Algorithm Visualizer & Benchmarker")
        self.facade = facade
        self.caretaker = Caretaker()

        self._setup_ui()

    def _setup_ui(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Алгоритм:").pack(side=tk.LEFT, padx=5)
        self.algo_var = tk.StringVar()
        self.algo_cb = ttk.Combobox(control_frame, textvariable=self.algo_var, state="readonly")
        self.algo_cb['values'] = self.facade.get_available_algorithms()
        if self.algo_cb['values']: self.algo_cb.current(0)
        self.algo_cb.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Дані:").pack(side=tk.LEFT, padx=5)
        self.data_var = tk.StringVar()
        self.data_cb = ttk.Combobox(control_frame, textvariable=self.data_var, state="readonly")
        self.data_cb['values'] = self.facade.get_available_data_types()
        if self.data_cb['values']: self.data_cb.current(0)
        self.data_cb.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Кількість:").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.IntVar(value=self.facade.settings.array_size)
        self.size_spin = ttk.Spinbox(control_frame, from_=5, to=500, textvariable=self.size_var, width=5)
        self.size_spin.pack(side=tk.LEFT, padx=5)

        self.run_btn = ttk.Button(control_frame, text="Відсортувати", command=self._on_run)
        self.run_btn.pack(side=tk.LEFT, padx=10)

        self.undo_btn = ttk.Button(control_frame, text="Відмінити (Undo)", command=self._on_undo, state=tk.DISABLED)
        self.undo_btn.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _draw_array(self, data, color="blue"):
        self.canvas.delete("all")
        if not data: return

        self.canvas.update_idletasks()
        c_width = self.canvas.winfo_width() or 800
        c_height = self.canvas.winfo_height() or 400

        bar_width = c_width / len(data)
        max_val = max(data)

        for i, val in enumerate(data):
            x0 = i * bar_width
            y0 = c_height - (val / max_val * c_height)
            x1 = (i + 1) * bar_width
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def _on_run(self):
        try:
            self.facade.settings.update_size(int(self.size_var.get()))
        except ValueError:
            messagebox.showerror("Помилка", "Введіть ціле число!")
            return

        self.run_btn.config(state=tk.DISABLED)

        def tick(current_data):
            self._draw_array(current_data, color="orange")
            self.root.update()
            time.sleep(self.facade.settings.animation_speed / 50)

        cmd = RunAlgorithmCommand(
            facade=self.facade,
            algo_name=self.algo_var.get(),
            data_type=self.data_var.get(),
            ui_callback=self._handle_result,
            tick_callback=tick
        )
        cmd.execute()

    def _handle_result(self, result: dict):
        self.run_btn.config(state=tk.NORMAL)
        self.caretaker.backup(result["original_data"])
        self.undo_btn.config(state=tk.NORMAL)

        self._draw_array(result["sorted_data"], color="green")

    def _on_undo(self):
        previous_state = self.caretaker.undo()
        if previous_state is not None:
            self._draw_array(previous_state, color="red")
            if not self.caretaker._history:
                self.undo_btn.config(state=tk.DISABLED)