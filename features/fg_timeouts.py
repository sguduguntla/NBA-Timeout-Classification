import pandas as pd
import numpy as np
import json

df = pd.read_csv("../data/Timeouts-3.csv")
pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")

with open("myfile.json", 'r') as f:
    consecutive_timeouts = json.load(f)

consecutive_timeouts = {float(k):v for k,v in consecutive_timeouts.items()}


def create_consecutive_timeouts():
    with open("labeled.txt", "r") as f:
        temp = list(np.array(f.read().split(", ")).astype(int))

    for index, row in df.iterrows():
        timeouts_remaining = row["Timeouts_remaining"]
        game_id = row["Game_id"]
        team_id = row["Team_id"]
        index1 = row["index"]

        cons_timeout_record = df[(df["Game_id"] == game_id) & (df["Team_id"] == team_id) & (df["Timeouts_remaining"] < timeouts_remaining)]
        
        if cons_timeout_record.empty:
            consecutive_timeouts[index1] = None
        else:
            if len(np.unique(cons_timeout_record["Timeouts_remaining"])) == 1:
                cons_timeout_record = cons_timeout_record.iloc[0]
            else:
                max_timeouts_remaining = cons_timeout_record["Timeouts_remaining"].max()
                cons_timeout_record = df[(df["Game_id"] == game_id) & (df["Team_id"] == team_id) & (df["Timeouts_remaining"] == max_timeouts_remaining)]
        
            consecutive_timeouts[index1] = int(cons_timeout_record["index"])

        print(index)

temp = []
for timeout_id in consecutive_timeouts:
    if consecutive_timeouts[timeout_id]:
        timeout_range = pbp[pbp["index"].between(timeout_id, consecutive_timeouts[timeout_id])]
    else:
        # first_row = pbp[pbp["index"] == timeout_id]
        # period = int(first_row["Period"])
        # game_id = int(first_row["Game_id"])
        # team_id = int(first_row["Team_id"])

        period = int(pbp.iat[timeout_id, 5])
        game_id = int(pbp.iat[timeout_id, 1])
        team_id = int(pbp.iat[timeout_id, 14])

        last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Event_Msg_Type"] == 13)]
        if len(last_row) > 1:
            last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Team_id"] == team_id) & (pbp["Event_Msg_Type"] == 13)]

        if len(last_row) > 1:
            last_row = last_row.iloc[0]
            
        if last_row.empty:
            last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Event_Msg_Type"] == 13)].iloc[0]
        
        last_index = int(last_row["index"])
        timeout_range = pbp[pbp["index"].between(timeout_id, last_index)]
    
    made_shots = 0
    total_shots = 0
    for index, row in timeout_range.iterrows():
        event_msg_type = row["Event_Msg_Type"]

        if event_msg_type == 1:
            made_shots += 1
            total_shots += 1
        elif event_msg_type == 2:
            total_shots += 1
    
    if total_shots == 0:
        temp.append(0)
    else:
        temp.append(made_shots/total_shots)

    print(len(temp))
    
df["Fg_percentage"] = temp

df.to_csv("../data/Timeouts-5.csv")