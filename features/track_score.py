import pandas as pd

df = pd.read_csv("../data/New_Play_by_Play_data_2.csv")

df = df[((df["Event_Msg_Type"] == 12) & (df["Period"] == 1)) | (df["Event_Msg_Type"] == 3) | (df["Event_Msg_Type"] == 1)]

# Team 1 Score, Team 2 Score, Leading Team ID, Point Differential
temp = [[], [], [], []]
# Both team ids in a game
current_teams = []
# All indexes where team id is 0 or some other random id
index_to_teamid = {
    3482956: 1610612751,
    4184919: 1610612744,
    4646834: 1610612738,
    4646835: 1610612738,
    7772116: 1610612755,
    7846733: 1610612741,
    9785700: 1610612759,
    3809253: 1610612747,
    3920181: 1610612747,
    5112468: 1610612742
}
num_times = 0

for index, row in df.iterrows():
    event_msg_type = row["Event_Msg_Type"]
    period = row["Period"]
    team_id = row["Team_id"]
    game_id = row["Game_id"]
    pbp_index = row["index"]
        
    if event_msg_type == 12 and period == 1:
        # Jump Ball and Period 1
        current_teams = list(df[df["Game_id"] == game_id].drop_duplicates(subset="Team_id")["Team_id"])

        if len(current_teams) > 2:
            current_teams = [id for id in current_teams if len(str(id)) == 10]
        
        for i in range(pbp_index - len(temp[0]) - 1):
            for j in range(len(temp)):
                temp[j].append(temp[j][-1])

        temp[0].append(0)
        temp[1].append(0)
        temp[2].append(current_teams[0])
        temp[3].append(0)
    
    elif event_msg_type == 1 or event_msg_type == 3:
        # Made Shot or Free Throw
        if index in index_to_teamid:
            team_id = index_to_teamid[index]
        
        for i in range(pbp_index - len(temp[0]) - 1):
            for j in range(len(temp)):
                temp[j].append(temp[j][-1])
        
        if team_id == 1897:
            team_id = 1610612747
        elif team_id == 101115:
            team_id = 1610612747
        elif team_id == 202346:
            team_id = 1610612742

        points_made = row["Option1"]
        team_index = current_teams.index(team_id)
        if team_index != 1 and team_index != 0:
            print("TEAM INDEX", team_index)
            break

        if event_msg_type == 3 and points_made > 1:
            points_made = 0
            
        temp[team_index].append(temp[team_index][-1]+points_made)
        temp[1 - team_index].append(temp[1-team_index][-1])

        point_differential = temp[0][-1] - temp[1][-1]

        if point_differential < 0:
            temp[2].append(current_teams[1])
        else:
            temp[2].append(current_teams[0])
        
        temp[3].append(point_differential)

    print(len(temp[0]), len(temp[2]),current_teams)

for i in range(6):
    for j in range(len(temp)):
        temp[j].append(temp[j][-1])

df = pd.read_csv("../data/New_Play_by_Play_data.csv")

df["Team1_score"] = temp[0]
df["Team2_score"] = temp[1]
df["Leading_team"] = temp[2]
df["Point_diff"] = temp[3]

df.to_csv("../data/New_Play_by_Play_data_2.csv")