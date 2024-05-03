import pandas as pd
from pytc.src.util import filter_complete_timeseries
from pytc.src.model import run_linear_model

df = pd.read_csv("pytc/output/facts.csv")

df = filter_complete_timeseries(df)
res = run_linear_model(df=df)

print(res.head())