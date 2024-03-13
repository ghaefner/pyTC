from pytc.src.model import Model
from pytc.src.reader import UnifyReader, PTRReader
from pytc.src.writer import CsvWriter
from pytc.config import Config, Table
from pytc.src.model import Task, calculate_share
from pytc.src.util import convert_value_to_num


test = Model(
    name="ULD",
    name_long = "Unify Liquid Data",
    reader = UnifyReader(config=Config),
    writer = CsvWriter(config=Config),
    tasks = [ 
        Task("", convert_value_to_num, Table.TRANSACTION),
        Task("", calculate_share, Table.TRANSACTION) 
        ],
).run()

