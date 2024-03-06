
class Config:
    # TODO (later): add main path for data and subdirectories for different readers (Unify, dm, etc.)
    PATH_TO_DATA ="pytc/data/Example_Unify.xlsx"
    PATH_TO_OUTPUT = "pytc/output/"


class Columns:
    MARKET = "market"
    PRODUCT = "product"
    REGION = "region"
    DATE = "date"
    METRIC = "metric"
    VALUE = "value"

class Table:
    TRANSACTION = "facts"


class ColumnMap:
    LD = {
    "Geography": Columns.REGION,
    "Product": Columns.MARKET,
    "MARKE": Columns.PRODUCT,
    "Verkauf 1.000 Euro": Columns.VALUE
}
    PTR_REGIO = {
        "KL3_LEV4": Columns.REGION,
        "BRANDS": Columns.PRODUCT,
        "Verkauf Euro 000": Columns.VALUE,
        "Relativer Monat": Columns.DATE
    }