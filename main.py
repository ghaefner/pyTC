from pytc.src.model import Model
from pytc.src.reader import UnifyReader
from pytc.src.writer import CsvWriter
from pytc.config import Config, Table, ColumnMap
from pytc.src.model import Task, dummy


print("Here.")
test = Model(
    name="ULD",
    name_long = "Unify Liquid Data",
    reader = UnifyReader(config=Config),
    writer = CsvWriter(file_path="./test.csv"),
    tasks = [ Task("", dummy, Table.TRANSACTION) ],
    column_map = ColumnMap.LD
)

print(test.reader.file_path)
print("Here.")
test.run()
print("Here.")