from datetime import datetime
import pandas as pd
from locale import setlocale, LC_ALL
from abc import ABC, abstractmethod
import logging as log

from pytc.config import Columns, ColumnMap, Config

class Reader(ABC):
    @abstractmethod
    def read(self):
        yield None

class UnifyReader(Reader):
    def __init__(self, config=Config):
        self.config = config
        self.file_path = self.config.PATH_TO_DATA
    
    def read(self):
        log.info(f"Reading file {self.file_path}.")

        df = pd.read_excel(self.file_path)
        df[Columns.DATE] = df["Time"].apply(self.parse_ld_date)
        df.rename(columns=ColumnMap.LD, inplace=True)
        df[Columns.METRIC] = "KEUR"
    
        df.drop(columns=set(df.columns) - set(vars(Columns).values()), inplace=True, errors="ignore")
        
        yield df

    def parse_ld_date(self, date_str):
        setlocale(LC_ALL, "de_DE")
        date_str = date_str.split("[")[0].strip()
        date_str = date_str.replace("Mär", "Mrz")
        return datetime.strptime(date_str, "%b, %y")
