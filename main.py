from pytc.src.model import Model
from pytc.src.reader import UnifyReader
from pytc.src.writer import CsvWriter


test = Model(
    name="ULD",
    name_long = "Unify Liquid Data",
    reader = UnifyReader
)