
class Config:
    # TODO (later): add main path for data and subdirectories for different readers (Unify, dm, etc.)
    PATH_TO_DATA ="pytc/data/Example_Unify.xlsx"


class Columns:
    MARKET = "market"
    PRODUCT = "product"
    REGION = "region"
    DATE = "date"
    METRIC = "metric"
    VALUE = "value"


class ColumnMap:

    LD = {
    "Geography": Columns.REGION,
    "Product": Columns.MARKET,
    "MARKE": Columns.PRODUCT,
    "Verkauf 1.000 Euro": Columns.VALUE
}