from pytc.src.model import Model
from pytc.src.reader import UnifyReader, PTRReader
from pytc.src.writer import CsvWriter
from pytc.config import Config, Table
from pytc.src.model import Task, calculate_share


test = Model(
    name="ULD",
    name_long = "Unify Liquid Data",
    reader = PTRReader(config=Config),
    writer = CsvWriter(config=Config),
    tasks = [ 
        Task("", replace_na_value, Table.TRANSACTION),
        Task("", calculate_share, Table.TRANSACTION) 
        ],
).run()

