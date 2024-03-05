from abc import ABC, abstractmethod
from time import perf_counter
import logging as log
import os
import pandas as pd
from pytc.config import Config

class Writer(ABC):
    @abstractmethod
    def write(data):
        return None
    

class CsvWriter(Writer):
    def __init__(self, config=Config, mode="a"):
        self.file_path = config.PATH_TO_OUTPUT
        self.counter = 0
        self.mode = mode

    def write(
            self,
            data_df,
            file_name
    ):
        start = perf_counter()
        log.info(f"[I] Writing {data_df.shape[0]}")
        log.info(f"[I] Columns: {data_df.columns.tolist()}")
        log.info(f"\n{data_df.head(1)}")

        if self.mode == "a":
            path = os.path.join(self.file_path, f"{file_name}.csv")
            data_df.sort_index(axis=1).to_csv(
                path, index=False, mode="a", header=not os.path.isfile(path)
            )
        elif self.mode == "w":
            path = os.path.join(self.file_path, f"{file_name}.csv")
            self.counter += 1
            data_df.sort_index(axis=1).to_csv(path, index=False, mode="w")
        
        log.debug(
            f"Finished writing {data_df.shape[0]} rows to {path} in {perf_counter()-start:0.2f} seconds."
        )