from dataclasses import dataclass
from pytc.src.reader import Reader
from pytc.src.writer import Writer
from typing import Callable, List
import logging
from time import perf_counter
from pytc.config import Columns
from pandas import melt,to_numeric

# Configure logging
logging.basicConfig(level=logging.INFO)

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
        logging.info(f"Loading {self.name_long} data sequentially.")
        for task in self.tasks:
            self.run_task(task)
        logging.info(
            f"Finished {self.name_long} data in {perf_counter() - start:0.2f} seconds."
        )

    def run_task(self, task):
        logging.info(f"Running {task.table}")
        
        for idx, data in enumerate(self.reader.read()):
            start = perf_counter()
            logging.info(f"Transforming {task.table} {idx + 1}.")
            data = task.func(data)
            logging.info(
               f"Transformed {task.table} {idx + 1} in {perf_counter() - start:0.2f} seconds."
            )
            self.writer.write(data, task.table)

def calculate_share(df, columns=Columns.ALL):
    
    if Columns.MARKET not in df.columns:
        raise KeyError("No market in dataframe present. Cannot calculate share.")
    
    columns_exl_product = [ col for col in columns if col not in [Columns.PRODUCT, Columns.VALUE] ]
    df[Columns.MARKET+Columns.SEP+Columns.VALUE] = df.groupby(columns_exl_product)[Columns.VALUE].transform('sum')
    df['share'] = df[Columns.VALUE] / df[Columns.MARKET+Columns.SEP+Columns.VALUE]

    df_long = melt(df, id_vars = [ col for col in columns if col not in [Columns.VALUE]],
                   value_vars = [ Columns.VALUE, 'share'],
                   var_name = 'type', value_name = Columns.VALUE )
    
    return df_long