import pandas as pd
from itertools import combinations
from sklearn.linear_model import LinearRegression
import numpy as np
from pytc.config import Columns
import statsmodels.api as sm
from pytc.src.util import filter_complete_time_series


df = pd.read_csv("pytc/output/facts.csv")

df = filter_complete_time_series(df)

TARGET_PRODUCT = "TAXOFIT"
TARGET_REGION = "NRW"
N_MAX = 2
N_MIN = 2

def perform_regression(data, target_region, target_product, n_min, n_max):
    # Filter data for target product
    filtered_data = data[data['product'] == target_product]
    
    # Group data by market and metric
    grouped_data = filtered_data.groupby(['market', 'metric'])
    
    # Dictionary to store results
    results = {}
    
    # Iterate over groups
    for group, group_data in grouped_data:
        market, metric = group
        
        # Select relevant columns for regression
        cols = ['date', 'region', 'value']
        group_data = group_data[cols]
        
        print(group_data)
        # Filter out regions with incomplete time series
        complete_regions = group_data['region'].value_counts()[group_data['region'].value_counts() >= len(group_data['date'].unique())].index.tolist()
        print(complete_regions)
        # Generate combinations of regions
        for n in range(n_min, n_max + 1):
            region_combinations = [comb for comb in combinations(complete_regions, n)]
        
            # Perform regression for each combination
            for region_combination in region_combinations:
                # Filter data for the selected regions
                reg_data = group_data[group_data['region'].isin(region_combination)]
                
                # Check for and remove duplicate entries
                reg_data = reg_data.drop_duplicates(subset=['date', 'region'], keep='first')
                
                # Pivot data for regression
                pivot_data = reg_data.pivot(index='date', columns='region', values='value').dropna()
                
                # Check if enough data points are available for regression
                if len(pivot_data) >= 2:
                    # Add constant for regression
                    pivot_data = sm.add_constant(pivot_data)
                    
                    # Fit regression model
                    model = sm.OLS(pivot_data[target_region], pivot_data.drop(columns=[target_region]))
                    result = model.fit()
                    
                    # Store results
                    results[(market, metric, region_combination)] = result
                    
    return results


reg_results = perform_regression(data=df, target_region=TARGET_REGION, target_product=TARGET_PRODUCT, n_min=N_MIN, n_max=N_MAX)

for key, result in reg_results.items():
    print("Market:", key[0])
    print("Metric:", key[1])
    print("Regions:", key[2])
    print(result.summary())
    print("\n")
