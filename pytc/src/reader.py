from datetime import datetime
import pandas as pd
from locale import setlocale, LC_ALL

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
        

def parse_ld_date(date_str):
    setlocale(LC_ALL, "de_DE")
    date_str = date_str.split("[")[0].strip()
    date_str = date_str.replace("Mär", "Mrz")
    return datetime.strptime(date_str, "%b, %y")
