import pandas as pd 
import numpy as np 

pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")

pbp = pbp[pbp["Event_Msg_Type"] == 9]

tm = pd.read_csv("../data/Timeouts-3.csv")

temp = []
for index, row in pbp.iterrows():
    if row["index"] != 594182:
        point_diff = row["Point_diff"]
        team_id = row["Team_id"]
        leading_team = row["Leading_team"]

        if team_id != leading_team and point_diff >= 10:
            temp.append(1)
        else:
            temp.append(0)

    print(len(temp))
    
tm["Is_down"] = temp

tm.to_csv("../data/Timeouts-3.csv")



