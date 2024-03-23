import pandas as pd
from itertools import combinations
from sklearn.linear_model import LinearRegression
import numpy as np
from pytc.config import Columns
import statsmodels.api as sm
from pytc.src.util import filter_complete_time_series


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

            model = LinearRegression()
            model.fit(X, y)
            # Print the coefficients
            print('Intercept:', model.intercept_)
            print('Coefficient:', model.coef_[0])