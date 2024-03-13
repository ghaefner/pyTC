from dataclasses import dataclass
from pytc.src.reader import Reader
from pytc.src.writer import Writer
from typing import Callable, List, Optional
import logging
from time import perf_counter
from pytc.config import Columns
from pandas import concat

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Task:
    source: Optional[str]
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
    df[Columns.MARKET+Columns.VALUE] = df.groupby(columns_exl_product)[Columns.VALUE].transform('sum')
    df['share'] = df[Columns.VALUE] / df[Columns.MARKET+Columns.VALUE]

    df_long = []
    for metric_type in [Columns.VALUE, Columns.MARKET+Columns.VALUE, 'share']:
        cols = [ col for sublist in [ [ col for col in Columns.ALL if col is not Columns.VALUE ], [ metric_type ] ] for col in sublist ]
        subset_df = df[cols].rename(columns={metric_type: Columns.VALUE})
        subset_df[Columns.METRIC] = subset_df[Columns.METRIC] + "_" + metric_type if metric_type != Columns.VALUE else subset_df[Columns.METRIC]
        df_long.append(subset_df)
        
    return concat(df_long)