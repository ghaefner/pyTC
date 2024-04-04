
class Config:
    # TODO (later): add main path for data and subdirectories for different readers (Unify, dm, etc.)
    PATH_TO_DATA ="pytc/data/"
    PATH_TO_OUTPUT = "pytc/output/"

    class Model:
        TARGET_PRODUCT = "TAXOFIT"
        TARGET_REGION = ["NRW", "BAY"]
        N_MAX = 2
        N_MIN = 2
        TEST_PERIOD = ["2023-11-01", "2023-12-01"]


class Columns:
    MARKET = "market"
    PRODUCT = "product"
    REGION = "region"
    DATE = "date"
    METRIC = "metric"
    VALUE = "value"
    SEP = "_"
    ALL = [MARKET, PRODUCT, REGION, DATE, METRIC, VALUE]

class Table:
    TRANSACTION = "facts"
    MODEL = "model"


class ColumnMap:
    LD = {
    "Geography": Columns.REGION,
    "Product": Columns.MARKET,
    "MARKE": Columns.PRODUCT,
    "Verkauf 1.000 Euro": Columns.VALUE,
    "Time": Columns.DATE
}
    PTR_REGIO = {
        "KL3_LEV4": Columns.REGION,
        "BRANDS": Columns.PRODUCT,
        "Verkauf Euro 000": Columns.VALUE,
        "Relativer Monat": Columns.DATE
    }