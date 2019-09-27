import pandas as pd
import numpy as np
import json

pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")
tm = pd.read_csv("../data/Timeouts-3.csv")

with open("myfile.json", 'r') as f:
    consecutive_timeouts = json.load(f)

consecutive_timeouts = {float(k):v for k,v in consecutive_timeouts.items()}

# i = 0
# with open("myfile.txt", "r") as f:
#     temp = list(np.abs(np.array(f.read().split(", ")).astype(float)))
temp = []
i = 0
last_row = None
for timeout_id in consecutive_timeouts:
    if i >= len(temp):
        if consecutive_timeouts[timeout_id]:
            consecutive_timeouts[timeout_id] = int(consecutive_timeouts[timeout_id])
        timeout_id = int(timeout_id)

        if not consecutive_timeouts[timeout_id]:
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
            
            if last_row.empty:
                last_row = pbp[(pbp["Period"] == period) & (pbp["Game_id"] == game_id) & (pbp["Event_Msg_Type"] == 13)]
                if len(last_row) > 1:
                    last_row = last_row.iloc[0]
        # try:
            
        # except TypeError as e:
        #     if first_row.empty:
        #         first_row = pbp[pbp["index"] == timeout_id]
        #         team_id = int(first_row["Team_id"])
        #     elif len(first_row) > 1:
        #         first_row = first_row.iloc[0]
        #         team_id = int(first_row["Team_id"])

        if isinstance(last_row, pd.DataFrame) and len(last_row) > 1:
            last_row = last_row.iloc[0]
                
        team_id = int(pbp.iat[timeout_id, 14])
        pc_time_start = int(pbp.iat[timeout_id, 7])

        # team_id = int(first_row["Team_id"])
        # pc_time_start = int(first_row["PC_Time"])

        if consecutive_timeouts[timeout_id]:
            pc_time_end = int(pbp.iat[consecutive_timeouts[timeout_id], 7])
        else:
            pc_time_end = int(last_row["PC_Time"])

        time_diff = abs((pc_time_end - pc_time_start)/10)
        
        temp.append(time_diff)

    i += 1
    print(len(temp))

tm["Time_diff"] = temp

tm.to_csv("../data/Timeouts-6.csv")