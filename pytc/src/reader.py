from datetime import datetime
import pandas as pd
from locale import setlocale, LC_ALL
import re

from config import Columns

class DataReader:
    def __init__(self, data_source):
        self.data_source = data_source
        
    
    def read_data(self):
        if self.data_source == "csv":
            return self.read_csv()
        
    def read_unify_excel(self):
        df = pd.read_excel("your_file_path.xlsx")

        df[Columns.DATE] = df["Time"].apply(parse_ld_date)

        # df["Time"].apply(lambda x: datetime.strptime(x.split("[")[0].strip(), "%b, %y"))

        # df = df.pivot_table(index=["date", "Geography", "Product", "MARKE"], columns="Metric", values="Verkauf 1.000 Euro").reset_index()

        # Rename the columns
        # df.columns = ["date", "region", "market", "product", "metric", "value"]

        return df
        

def parse_ld_date(date, locale='de_DE'):
    setlocale(LC_ALL, locale=locale)
    date = re.sub(r"\[W \d\d-\d\d]", "", date)
    date = re.sub(r"MAT |YTD ", "", date)
    date = date.replace("Mär", "Mrz")
    date = date.replace(",","")
    date = datetime.strptime(date, "%b %y")
    return date