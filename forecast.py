import pandas as pd
from itertools import combinations
import numpy as np
from pytc.config import Columns
from pytc.src.util import filter_complete_time_series
from pytc.src.model import linear_regression_results


df = pd.read_csv("pytc/output/facts.csv")

# df = filter_complete_time_series(df)

TARGET_PRODUCT = "TAXOFIT"
TARGET_REGION = "NRW"
N_MAX = 2
N_MIN = 2


filtered_data = df[df['product'] == TARGET_PRODUCT]

print(filtered_data)

grouped_data = filtered_data.groupby(['market', 'metric'])

for group, group_data in grouped_data:
    market, metric = group
    cols = ['date', 'region', 'value']
    
    df = group_data[cols].pivot_table(index='date', columns='region', values='value', aggfunc='first').reset_index()
    
    complete_regions = group_data['region'].value_counts()[group_data['region'].value_counts() >= len(group_data['date'].unique())].index.tolist()

    for n in range(N_MIN,N_MAX+1):
        region_combinations = [comb for comb in combinations(complete_regions, n)]

        for region_comb in region_combinations:
            # Perform linear regression
            X = df[list(region_comb)].values.reshape(-1, len(region_comb))
            y = df[TARGET_REGION].values

            res = linear_regression_results(X,y,region_comb)
            print(res)