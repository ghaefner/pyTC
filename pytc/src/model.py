from dataclasses import dataclass
from pytc.src.reader import Reader
from pytc.src.writer import Writer
from typing import Callable, List, Optional
import logging
from time import perf_counter
from pytc.config import Columns, Config
from pandas import concat, to_datetime, DataFrame
from sklearn.linear_model import LinearRegression
from statsmodels.api import add_constant, OLS 
from numpy import select
from itertools import combinations

# Configure logging
logging.basicConfig(level=logging.INFO)

@dataclass
class Task:
    source: Optional[str]
    func: Callable
    table: str


@dataclass
class Model:
    name: str
    name_long: str
    reader: Reader
    writer: Writer
    tasks: List[Task]
    column_map: dict = None

    def run(self):
        start = perf_counter()
        logging.info(f"Loading {self.name_long} data sequentially.")
        for task in self.tasks:
            self.run_task(task)
        logging.info(
            f"Finished {self.name_long} data in {perf_counter() - start:0.2f} seconds."
        )

    def run_task(self, task):
        logging.info(f"Running {task.table}")
        
        for idx, data in enumerate(self.reader.read()):
            start = perf_counter()
            logging.info(f"Transforming {task.table} {idx + 1}.")
            data = task.func(data)
            logging.info(
               f"Transformed {task.table} {idx + 1} in {perf_counter() - start:0.2f} seconds."
            )
            self.writer.write(data, task.table)

def calculate_share(df, columns=Columns.ALL):
    
    if Columns.MARKET not in df.columns:
        raise KeyError("No market in dataframe present. Cannot calculate share.")
    
    columns_exl_product = [ col for col in columns if col not in [Columns.PRODUCT, Columns.VALUE] ]
    df[Columns.MARKET+Columns.VALUE] = df.groupby(columns_exl_product)[Columns.VALUE].transform('sum')
    df['share'] = df[Columns.VALUE] / df[Columns.MARKET+Columns.VALUE]

    df_long = []
    for metric_type in [Columns.VALUE, 'share']:
        cols = [ col for sublist in [ [ col for col in Columns.ALL if col is not Columns.VALUE ], [ metric_type ] ] for col in sublist ]
        subset_df = df[cols].rename(columns={metric_type: Columns.VALUE})
        subset_df[Columns.METRIC] = subset_df[Columns.METRIC] + "_" + metric_type if metric_type != Columns.VALUE else subset_df[Columns.METRIC]
        df_long.append(subset_df)
        
    return concat(df_long)


def linear_regression_results(X, y, region_comb):
    # Fit the linear regression model
    model = LinearRegression().fit(X, y)

    # Calculate p-values
    X_with_const = add_constant(X)
    model_ols = OLS(y, X_with_const).fit()
    p_values = model_ols.pvalues[1:]

    # Create a DataFrame with coefficients and p-values
    results = DataFrame({'Coefficient': [*model.coef_, model.intercept_],
                            'P-value': [*p_values, model_ols.pvalues[0]]},
                           index=[*region_comb, "Intercept"])

    return results


def run_linear_model(df, config=Config.Model):
    
    df[Columns.DATE] = to_datetime(df[Columns.DATE])
    config.TEST_PERIOD = [ to_datetime(date_str) for date_str in config.TEST_PERIOD ]

    df['period'] = select([df[Columns.DATE] < min(config.TEST_PERIOD), df[Columns.DATE] > max(config.TEST_PERIOD)], ['Pre', 'Post'], default='Test')

    for tgt_region in config.TARGET_REGION:
        filtered_data = df[(df[Columns.PRODUCT] == config.TARGET_PRODUCT) & (df['period']=='Pre')]

        grouped_data = filtered_data.groupby([Columns.MARKET, Columns.METRIC])

        for _, group_data in grouped_data:
            cols = [Columns.DATE, Columns.REGION, Columns.VALUE]
        
            df = group_data[cols].pivot_table(index=Columns.DATE, columns=Columns.REGION, values=Columns.VALUE, aggfunc='first').reset_index()
        
            complete_regions = group_data[Columns.REGION].value_counts()[group_data[Columns.REGION].value_counts() >= len(group_data[Columns.DATE].unique())].index.tolist()

            for n in range(config.N_MIN,config.N_MAX+1):
                region_combinations = [comb for comb in combinations(complete_regions, n)]

                for region_comb in region_combinations:
                    # Perform linear regression
                    X = df[list(region_comb)].values.reshape(-1, len(region_comb))
                    y = df[tgt_region].values

                    res = linear_regression_results(X,y,region_comb)
                    print(res)
