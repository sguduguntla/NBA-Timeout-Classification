import pandas as pd 

df = pd.read_csv("data/New_Play_by_Play_data_2.csv")

timeout_df = pd.DataFrame(columns=["Game_id", "Period", "Team_id", "Time_remaining", "Timeouts_remaining", "Season", "Effectiveness", "index"])

num_timeouts_regulation  = 7
num_timeouts_OT = 2
num_timeouts_in_last_3_mins = 2
num_timeouts_in_last_2_mins = 3
df = df[df["Event_Msg_Type"] == 9]
timeouts_left = {}
temp = []
for index in range(df.shape[0]):
    row = df.iloc[index]
    period = row["Period"]
    game_id = row["Game_id"]
    team_id = row["Team_id"]
    pc_time = row["PC_Time"]
    event_msg_type = row["Event_Msg_Type"]
    index1 = row["index"]
    season = int(str(game_id)[1:3]) + 2000

    if team_id == 0:
        if game_id == 21000640:
            team_id = 1610612742
        elif game_id == 21100652:
            team_id = 1610612747
        elif game_id == 21200203:
            team_id = 1610612740
    
    if event_msg_type == 9:

        if season < 2017:
            num_timeouts_regulation = 9
        else:
            num_timeouts_regulation = 7
        
        if game_id not in timeouts_left:
            timeouts_left[game_id] = {}
        if period > 4:
            timeouts_left[game_id][team_id] = timeouts_left[game_id].get(team_id, num_timeouts_OT) - 1
            period = 4
        else:
            if season < 2017:
                if period == 4 and pc_time <= 1200 and timeouts_left[game_id].get(team_id, num_timeouts_regulation) > num_timeouts_in_last_2_mins:
                    # If the game is in the last 2 minutes, you can only take 3 timeouts
                    timeouts_left[game_id][team_id] = num_timeouts_in_last_2_mins - 1
                else:
                    timeouts_left[game_id][team_id] = timeouts_left[game_id].get(team_id, num_timeouts_regulation) - 1
            else:
                if period == 4 and pc_time <= 1800 and timeouts_left[game_id].get(team_id, num_timeouts_regulation) > num_timeouts_in_last_3_mins:
                    # If the game is in the last 3 minutes, you can only take 2 timeouts
                    timeouts_left[game_id][team_id] = num_timeouts_in_last_3_mins - 1
                else:
                    timeouts_left[game_id][team_id] = timeouts_left[game_id].get(team_id, num_timeouts_regulation) - 1

        if timeouts_left[game_id][team_id] < 0:
            timeouts_left[game_id][team_id] = 0
    
        time_remaining = (pc_time + (4 - period) * 7200)/10

        temp.append([game_id, period, team_id, time_remaining, timeouts_left[game_id][team_id], season, -1,index1])

        print("timeouts:", index)

    print(index)
    
timeout_df = timeout_df.append(pd.DataFrame(temp, columns=["Game_id", "Period", "Team_id", "Time_remaining", "Timeouts_remaining", "Season", "Effectiveness","index"]))
timeout_df.to_csv("data/Timeouts-1.csv", index=False)