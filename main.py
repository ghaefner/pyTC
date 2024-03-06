from pytc.src.model import Model
from pytc.src.reader import UnifyReader, PTRReader
from pytc.src.writer import CsvWriter
from pytc.config import Config, Table, ColumnMap
from pytc.src.model import Task, dummy


test = Model(
    name="PTR",
    name_long = "Pharmatrend Regio",
    reader = PTRReader(config=Config),
    writer = CsvWriter(config=Config),
    tasks = [ Task("", dummy, Table.TRANSACTION) ],
).run()

