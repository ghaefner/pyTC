from pytc.src.model import Model
from pytc.src.reader import UnifyReader
from pytc.src.writer import CsvWriter
from pytc.config import Config, ColumnMap


test = Model(
    name="ULD",
    name_long = "Unify Liquid Data",
    reader = UnifyReader(config=Config),
    writer = CsvWriter(file_path="./test.csv"),
    tasks = [],
    column_map = ColumnMap.LD
).run()