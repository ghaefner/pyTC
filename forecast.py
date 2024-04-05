import pandas as pd
from itertools import combinations
import numpy as np
from pytc.config import Columns
from pytc.src.util import filter_complete_time_series
from pytc.src.model import run_linear_model
from datetime import datetime

df = pd.read_csv("pytc/output/facts.csv")

res = run_linear_model(df=df)

print(res.head())