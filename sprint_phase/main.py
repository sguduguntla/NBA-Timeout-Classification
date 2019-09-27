import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
# Substitution changes
# 
# END GOAL: Predict change in PPG per season in the future given the rule change of 1 free throw = 2 points and a 4 point basket

# 1 Free Throw = 2 points 
#Pace Would Be Faster - 1 FT instead of 2 FT for each foul w/ 2 freethrows after

#1st Step - Loop through and look at FT% for a player during a game. Then loop through all the FT data and find groups of two freethrows
#Use the FT% to judge whether they make the one shot

#df = pd.read_csv("data/Updated_Play_by_Play.csv")
#bs = pd.read_csv("data/Updated_Box_Score.csv")

# pbp = pbp[(pbp["Event_Msg_Type"] == 3) & (pbp["Action_Type"].isin([10, 11, 13, 16, 17, 18, 20, 21, 25, 27]))]
    
def plot_columns():
    df = pd.read_csv("data/Updated_Play_by_Play_data.csv", encoding="ISO-8859-1")
    df = df[df["Game_id"] == 1020000001]
    plt.plot(df.index, df["Team1_score"], df.index, df["Team2_score"], df.index, df["Team1_score_adjust"], df.index, df["Team2_score_adjust"])
    plt.title("Adjusted Score with Single Free Throw")
    plt.xlabel("Play Index")
    plt.ylabel("Game Score (points)")
    plt.legend(('Team 1', 'Team 2', 'Team 1 Adjust', 'Team 2 Adjust'))
    plt.show()

def add_score_columns():
    df = pd.read_csv("data/Updated_Play_by_Play_data.csv", encoding="ISO-8859-1")
    current_teams = []

    for index, row in df.iterrows():
        event_msg_type = row["Event_Msg_Type"]
        period = row["Period"]
        team_id = row["Team_id"]
        game_id = row["Game_id"]
        pbp_index = index
        
        if pbp_index in [339832, 394606]:
            continue

        if ((pbp_index == 900871 and event_msg_type == 10) or event_msg_type == 12) and period == 1:
            # Jump Ball and Period 1
            current_teams = list(df[df["Game_id"] == game_id].drop_duplicates(subset="Team_id")["Team_id"])

            if len(current_teams) > 2:
                current_teams = [id for id in current_teams if len(str(id)) == 10]
            
            for i in range(((pbp_index - len(temp[0]) - 1) if pbp_index > 0 else 0)):
                for j in range(len(temp)):
                    temp[j].append(temp[j][-1])

            temp[0].append(0)
            temp[1].append(0)
            temp[2].append(current_teams[0])
            temp[3].append(0)
        
        elif (event_msg_type == 1 or event_msg_type == 3) and len(current_teams) > 1:
            # Made Shot or Free Throw
            # if index in index_to_teamid:
            #     team_id = index_to_teamid[index]
            
            for i in range(pbp_index - len(temp[0]) - 1):
                for j in range(len(temp)):
                    temp[j].append(temp[j][-1])
            
            # if team_id == 1897:
            #     team_id = 1610612747
            # elif team_id == 101115:
            #     team_id = 1610612747
            # elif team_id == 202346:
            #     team_id = 1610612742

            points_made = row["Option1"]
            print("HIIII", index, current_teams)

            team_index = current_teams.index(team_id)

            # if team_index != 1 and team_index != 0:
            #     print("TEAM INDEX", team_index)
            #     break

            action_type = row["Action_Type"]
            
            if event_msg_type == 3:
                if action_type in [10,16,17,20]:
                    # 1 Free Throw
                    if points_made > 1:
                        points_made = 0
                    
                elif action_type in [11, 18, 21, 25]:
                    if points_made > 1:
                        points_made = 0
                    else:
                        points_made = 2
                elif action_type in [13, 27]:
                    if points_made > 1:
                        points_made = 0
                    else:
                        points_made = 3
                else:
                    points = 0
                
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

    df = pd.read_csv("data/Updated_Play_by_Play_data.csv", encoding="ISO-8859-1")

    df["Team1_score_adjust"] = temp[0]
    df["Team2_score_adjust"] = temp[1]
    df["Leading_team_adjust"] = temp[2]
    df["Point_diff_adjust"] = temp[3]

    df.to_csv("data/Updated_Play_by_Play_data.csv")
        
# with open("temp.txt", "r") as f:
#     temp = list([list(arr_str[1:-1].split(", ")) for arr_str in f.read().split(", ")])

#emp = [[], [], [], []]

#add_score_columns()

plot_columns()
8
