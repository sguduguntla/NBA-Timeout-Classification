import pandas as pd
import numpy as np
import json

def read_from_file(filename, is_json=False):
    with open(filename, "r") as f:
        if is_json:
            return json.load(f)
        else:
            return f.read()

def write_to_file(filename, data, is_json=False):
    with open(filename, "w") as f:
        if is_json:
            json.dump(data, f)
        else:
            f.write(str(data))

df = pd.read_csv("../data/Timeouts-3.csv")
pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")

temp = []
i = 0
for index, row in df.iterrows():
    if i >= len(temp):
        game_id = row["Game_id"]
        team_id = row["Team_id"]
        index1 = row["index"]

        cur_point_diff = abs(int(pbp[(pbp["index"] == index1)]["Point_diff"]))

        largest_point_diff = abs(pbp[pbp["Game_id"] == game_id]["Point_diff"].max())

        temp.append(cur_point_diff - largest_point_diff)

    i += 1
    print(len(temp))

df["Lead_diff"] = temp

df.to_csv("../data/Timeouts-3.csv")