from abc import ABC, abstractmethod
import json
import os
from datetime import datetime


class BenchmarkReport:
    def __init__(self):
        self.data = {}

    def save_to_file(self, filename="results.json"):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        else:
            history = []

        history.append(self.data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
        print(f"[Export] Дані бенчмарку збережено у {filename}")


class ReportBuilder(ABC):
    @abstractmethod
    def reset(self): pass

    @abstractmethod
    def build_header(self, algo_name: str, data_type: str): pass

    @abstractmethod
    def build_metrics(self, size: int, exec_time: float, threads: int): pass

    @abstractmethod
    def get_report(self) -> BenchmarkReport: pass


class JSONReportBuilder(ReportBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._report = BenchmarkReport()
        self._report.data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def build_header(self, algo_name: str, data_type: str):
        self._report.data["algorithm"] = algo_name
        self._report.data["data_type"] = data_type

    def build_metrics(self, size: int, exec_time: float, threads: int):
        self._report.data["array_size"] = size
        self._report.data["execution_time_sec"] = round(exec_time, 6)
        self._report.data["threads_used"] = threads

    def get_report(self) -> BenchmarkReport:
        report = self._report
        self.reset()
        return report


class ReportDirector:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> ReportBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ReportBuilder):
        self._builder = builder

    def make_report(self, result_dict: dict):
        self.builder.build_header(result_dict["algorithm"], result_dict["data_type"])
        self.builder.build_metrics(
            result_dict["size"],
            result_dict.get("execution_time", 0.0),
            result_dict.get("threads_used", 1)
        )