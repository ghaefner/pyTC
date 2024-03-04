from dataclasses import dataclass
from pytc.src.reader import Reader
from pytc.src.writer import Writer
from typing import Callable, List
import logging as log
from time import perf_counter

@dataclass
class Task:
    source: str
    func: Callable
    table: str


@dataclass
class Model:
    name: str
    name_long: str
    reader: Reader
    writer: Writer
    tasks: List[Task]
    column_map: dict = None

    def run(self):
        start = perf_counter()
        log.info(f"[I] Loading {self.name_long} data sequentially.")
        for task in self.tasks:
            self.run_task(task)
        log.info(
            f"[I] Finished {self.name_long} data in {perf_counter() - start:0.2f} seconds."
        )

    def run_task(self, task):
        log.info(f"Running {task.table}")
        
        for idx, data in enumerate(self.reader.read(task.source)):
            start = perf_counter()
            log.info(f"[I] Transforming {task.table} {idx + 1}.")
            data = task.func(data)
            log.info(
                f"[I] Transformed {task.table} {idx + 1} in {perf_counter() - start:0.2f} seconds."
            )
            # self.writer(data, task.table)