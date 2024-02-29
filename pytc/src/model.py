import datetime as dt
from config import Columns

class Model:
    def __init__(self, market, product, region, date, metric, value):
        
        self._validate_data_type({
            Columns.MARKET: (market, str),            
            Columns.PRODUCT: (product, str),
            Columns.REGION: (region, str),
            Columns.DATE: (date, dt.date),
            Columns.METRIC: (metric, str),
            Columns.VALUE: (value, float)
        })
        
        self.market = market
        self.product = product
        self.region = region
        self.date = date
        self.metric = metric
        self.value = value
        
    def _validate_data_types(self, data_types):
        for attr_name, (attr_value, expected_type) in data_types.items():
            if not isinstance(attr_value, expected_type):
                raise TypeError(f"{attr_name.capitalize()} must be of type {expected_type.__name__}.")
        