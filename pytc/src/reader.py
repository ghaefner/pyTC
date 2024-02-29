from datetime import datetime
from pandas import read_excel


class DataReader:
    def __init__(self, data_source):
        self.data_source = data_source
        
    
    def read_data(self):
        if self.data_source == "csv":
            return self.read_csv()
        
    def read_unify_excel(self):
        df = read_excel()
        
    