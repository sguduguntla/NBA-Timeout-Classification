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
i = 0
last_row = None
for timeout_id in consecutive_timeouts:
    if consecutive_timeouts[timeout_id]:
        consecutive_timeouts[timeout_id] = int(consecutive_timeouts[timeout_id])
    timeout_id = int(timeout_id)

    if i >= len(temp):
        # if :            
        #     #first_row = pbp.iloc[timeout_id]
        #     last_row = pbp.iloc[consecutive_timeouts[timeout_id]]
        if not consecutive_timeouts[timeout_id]:
            #first_row = pbp.iloc[timeout_id]
            period = int(pbp.iat[timeout_id, 5])
            game_id = int(pbp.iat[timeout_id, 1])
            team_id = int(pbp.iat[timeout_id, 14])

            # period = int(first_row["Period"])
            # game_id = int(first_row["Game_id"])
            # team_id = int(first_row["Team_id"])
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

        if team_id == init_leading_team:
            if final_point_diff < init_point_diff:
                # Not successful
                temp.append(0)
            elif team_id == final_leading_team:
                # successful
                temp.append(1)
            else:
                temp.append(0)
        else:
            if final_point_diff < init_point_diff:
                # successful timeout
                temp.append(1)
            elif team_id == final_leading_team:
                # successful timeout
                temp.append(1)
            else:
                # Not successful timeout
                temp.append(0)

    i += 1
    print(len(temp))
        
df["Effectiveness"] = temp

df.to_csv("../data/Timeouts-3.csv")

    

        

