import pandas as pd
import numpy as np
import json

df = pd.read_csv("../data/Timeouts-3.csv")
pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")

with open("myfile2.json", 'r') as f:
    consecutive_timeouts = json.load(f)

consecutive_timeouts = {float(k):v for k,v in consecutive_timeouts.items()}

def create_consecutive_timeouts():
    for index, row in df.iterrows():
        index1 = row["index"]
        if index < len(df) - 1:
            consecutive_timeouts[index1] = int(df.iloc[index + 1]["index"])
        else:
            consecutive_timeouts[index1] = None

    with open("myfile2.json", 'w') as f:
        json.dump(consecutive_timeouts, f)

temp = []
i = 0
last_row = None
for timeout_id in consecutive_timeouts:
    if consecutive_timeouts[timeout_id]:
        consecutive_timeouts[timeout_id] = int(consecutive_timeouts[timeout_id])
    timeout_id = int(timeout_id)

    if i >= len(temp):
        if not consecutive_timeouts[timeout_id]:
            period = int(pbp.iat[timeout_id, 5])
            game_id = int(pbp.iat[timeout_id, 1])
            team_id = int(pbp.iat[timeout_id, 14])

            last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Event_Msg_Type"] == 13)]

            if len(last_row) > 1:
                last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Team_id"] == team_id) & (pbp["Event_Msg_Type"] == 13)]
            
            if last_row.empty:
                last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Event_Msg_Type"] == 13)].iloc[0]
                
        team_id = int(pbp.iat[timeout_id, 14])

        if isinstance(last_row, pd.DataFrame) and len(last_row) > 1:
            last_row = last_row.iloc[0]

        init_point_diff = abs(int(pbp.iat[timeout_id, 23]))

        if consecutive_timeouts[timeout_id]:
            final_point_diff = int(pbp.iat[consecutive_timeouts[timeout_id], 23])
        else:
            final_point_diff = abs(int(last_row["Point_diff"]))
        

        init_leading_team = int(pbp.iat[timeout_id, 22])

        if consecutive_timeouts[timeout_id]:
            final_leading_team = int(pbp.iat[consecutive_timeouts[timeout_id], 22])
        else:
            final_leading_team = int(last_row["Leading_team"])

        print(timeout_id, consecutive_timeouts[timeout_id], final_point_diff, final_leading_team)

        if team_id != init_leading_team:
            init_point_diff *= -1
        if team_id != final_leading_team:
            final_point_diff *= -1

        print(init_point_diff, final_point_diff)
        temp.append(final_point_diff - init_point_diff)

    i += 1
    print(len(temp))

df["Point_diff"] = temp

df.to_csv("../data/Timeouts-3.csv")

    

        




