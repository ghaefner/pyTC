import pandas as pd
from itertools import combinations
from sklearn.linear_model import LinearRegression
import numpy as np
from pytc.config import Columns

df = pd.read_csv("pytc/output/facts.csv")

TARGET_PRODUCT = "TAXOFIT"
TARGET_REGION = "NRW"
N_MAX = 2

grouped_df = df.groupby([Columns.MARKET, Columns.METRIC])

for name, group in grouped_df:
    filtered_group = group[(group[Columns.PRODUCT]==TARGET_PRODUCT) & (group[Columns.REGION]==TARGET_REGION)]
    
    if filtered_group.empty:
        continue

    product_time_series = group[Columns.VALUE].tolist()

    # Select N_MAX number of other regions for correlation analysis
    other_regions = list(set(group[Columns.REGION]) - {TARGET_REGION})
    predictor_regions = list(combinations(other_regions, N_MAX))

    for predictor_region_combination in predictor_regions:
        predictor_regions_data = []
        max_length = max(len(df[(df['region'] == region) & (df['market'] == name[0]) & (df['metric'] == name[1])]['value'].tolist()) for region in predictor_region_combination)
        for region in predictor_region_combination:
            region_data = df[(df[Columns.REGION] == region) & (df[Columns.MARKET] == name[0]) & (df[Columns.METRIC] == name[1])][Columns.VALUE].tolist()
            # Pad or truncate the time series data to ensure uniform length
            region_data = region_data[:max_length] + [np.nan] * (max_length - len(region_data))
            predictor_regions_data.append(region_data)

    # Convert the time series data for each region into numpy arrays
    predictor_regions_data = [np.array(region_data) for region_data in predictor_regions_data]
    
    # Concatenate the numpy arrays to create the predictor regions data
    predictor_regions_data = np.vstack(predictor_regions_data)
    
    # Calculate correlation between the target region and predictor regions
    correlation_matrix = np.corrcoef(product_time_series, predictor_regions_data)
    correlation_coefficient = correlation_matrix[0, 1:]

    print(correlation_coefficient)
        
    # print(f"Market: {name[0]}, Metric: {name[1]}, Predictor Regions: {predictor_region_combination}, Correlation Coefficients: {correlation_coefficient}")

    # Create a forecast of the TARGET_REGION based on the predictor regions (Example using linear regression)
    # model = LinearRegression()
    # model.fit(predictor_regions_data, product_time_series)
    # forecast = model.predict(predictor_regions_data)

    