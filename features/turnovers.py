import pandas as pd 
import numpy as np

df = pd.read_csv("../data/New_Play_by_Play_data_2.csv")
tm = pd.read_csv("../data/Timeouts-3.csv")

df = df[(df["Event_Msg_Type"] == 9) | (df["Event_Msg_Type"] == 5) | ((df["Event_Msg_Type"] == 12) & (df["Period"] == 1))]

turnovers = {}
temp = []
indices = []
for index, row in df.iterrows():
    if row["index"] != 594182:
        event_msg_type = row["Event_Msg_Type"]
        team_id = row["Team_id"]

        if event_msg_type == 9:
            if team_id in turnovers:
                temp.append(turnovers[team_id])
                indices.append(row["index"])
            else:
                temp.append(0)
            
            turnovers[team_id] = 0

        elif event_msg_type == 5:
            if team_id in turnovers:
                turnovers[team_id] += 1
            else:
                turnovers[team_id] = 1
        elif event_msg_type == 12:
            turnovers = {}

    print(len(temp))

tm["Turnovers"] = temp

tm.to_csv("../data/Timeouts-3.csv")


