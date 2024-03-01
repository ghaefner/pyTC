from dataclasses import dataclass
from reader import Reader
from typing import Callable, List

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
    task: List[Task]
    column_map: dict = None