from datetime import datetime
import pandas as pd
from locale import setlocale, LC_ALL
from abc import ABC, abstractmethod
import logging as log
from openpyxl import load_workbook
from pytc.src.util import apply_column_map, skip_incomplete_rows, use_first_row_as_header

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
        df = apply_column_map(df, ColumnMap.LD)
        df[Columns.DATE] = df[Columns.DATE].apply(self.parse_ld_date)

        yield df[Columns.ALL]

    def parse_ld_date(self, date_str):
        setlocale(LC_ALL, "de_DE")
        date_str = date_str.split("[")[0].strip()
        date_str = date_str.replace("Mär", "Mrz")
        return datetime.strptime(date_str, "%b, %y")
    

class PTRReader(Reader):
    def __init__(self, config=Config):
        self.file_path = config.PATH_TO_DATA

    def read(self):
        log.info(f"Reading file {self.file_path}.")

        wb = load_workbook(self.file_path, data_only=True)
        sheet = wb.active

        # Extract market
        selected_market = sheet["A2"].value.split(" = ")[1].strip()

        df = pd.read_excel(self.file_path)
        df = self.parse_cha_data(df)
        df = apply_column_map(df, ColumnMap.PTR_REGIO)
        df[Columns.MARKET] = selected_market
        df[Columns.DATE] = df[Columns.DATE].apply(self.parse_cha_data)
        df[Columns.REGION] = df[Columns.REGION].apply(self.parse_ptr_regions)

        yield df[Columns.ALL]

    def parse_cha_data(data):
        return(
            data.pipe(skip_incomplete_rows)
            .pipe(use_first_row_as_header)
        )

    def parse_cha_date(date_str):
        setlocale(LC_ALL, "de_DE")
        if "MAT" in date_str or "YTD":
            return datetime.strptime(date_str[4:], "%m/%y")
        else:
            return datetime.strptime(date_str, "%b %y")

    
    def parse_ptr_regions(subregion_int):
        region_int = ( subregion_int // 100 )*100 + (subregion_int % 10)
        return "Geb_" + str(region_int)
