from abc import ABC, abstractmethod
import threading
from src.algorithms.report import JSONReportBuilder, ReportDirector


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class RunAlgorithmCommand(Command):
    def __init__(self, facade, algo_name: str, data_type: str, ui_callback, tick_callback=None):
        self.facade = facade
        self.algo_name = algo_name
        self.data_type = data_type
        self.ui_callback = ui_callback
        self.tick_callback = tick_callback

    def execute(self):
        # Виносимо всю важку роботу в окремий фоновий потік!
        thread = threading.Thread(target=self._run_in_background, daemon=True)
        thread.start()

    def _run_in_background(self):
        # Цей код працює у фоні і не блокує Tkinter
        result = self.facade.run_algorithm(self.algo_name, self.data_type, self.tick_callback)

        director = ReportDirector()
        builder = JSONReportBuilder()
        director.builder = builder

        director.make_report(result)
        report = builder.get_report()
        report.save_to_file("results.json")

        # Передаємо результат назад (через безпечну чергу в app.py)
        self.ui_callback(result)