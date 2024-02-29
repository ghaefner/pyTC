
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