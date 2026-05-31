from abc import ABC, abstractmethod
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
        result = self.facade.run_algorithm(self.algo_name, self.data_type, self.tick_callback)

        # --- Реалізація Патерну Builder (Збереження у файл) ---
        director = ReportDirector()
        builder = JSONReportBuilder()
        director.builder = builder

        # Директор покроково формує звіт з отриманих даних
        director.make_report(result)
        report = builder.get_report()

        # Зберігаємо файл у корінь проєкту
        report.save_to_file("results.json")
        # -----------------------------------------------------

        self.ui_callback(result)