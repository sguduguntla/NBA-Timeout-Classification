import pandas as pd
import numpy as np

df = pd.read_csv("../data/Updated_Play_by_Play_data.csv")
column = np.arange(0,df.shape[0])
df["index"] = column

print(len(column))
df.to_csv("../data/New_Play_by_Play_data_2.csv")