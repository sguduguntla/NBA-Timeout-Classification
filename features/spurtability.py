import pandas as pd 
import numpy as np 
from lineups import get_all_players, get_all_games
import json
import logging
import threading
import time

temp = []
players_not_in_bs = []
seen = {}

def main():
    
    #print(pbp[0])
    for game_id in timeouts:
        for index in timeouts[game_id]:
            
            team_id = timeouts[game_id][index]
            season = int(str(game_id)[1:3]) + 2000
            print(season)

            if game_id not in seen:
                seen[game_id] = {}
            
            if season not in seen[game_id]:
                seen[game_id][season] = {}
            
            if team_id not in seen[game_id][season]:
                
                players_per_game = game_lineup[game_id][team_id]

                num_games = []
                avg_scores = []
                total_score = 0
                spurt_dict = {}

                for player in players_per_game: 
                    scoring_average = get_player_scoring_average(player, season)
                    num_games.append(scoring_average[1])
                    avg_scores.append(scoring_average[0])
                for n in range(len(num_games)):
                    if sum(num_games) != 0:
                        total_score += num_games[n]/sum(num_games) * (avg_scores[n]/num_games[n])
                
                temp.append(total_score)
                seen[game_id][season][team_id] = total_score
            else:
                temp.append(seen[game_id][season][team_id])

            write_to_file("players_no_bs.json", players_not_in_bs, is_json=True)

            print(len(temp), scoring_average, total_score)
            
    write_to_file("spurt.txt",temp)

def get_player_scoring_average(person_id, final_season):
    if final_season == 2003:
        final_season = 2004
    season_upper_bound = (final_season - 2000)

    relevant_games = [g for g in list(players[person_id].keys()) if int(str(g)[1:3]) <= season_upper_bound]
    
    all_games = pbp[pbp["Game_id"].isin(relevant_games)]
    # all_games = all_games.to_dict(orient="records")
    is_in = lambda x: int(x["Game_id"]) in relevant_games
    
    # get_all_games = fnc.compose((fnc.filter,is_in))
    # all_games = list(get_all_games(pbp))

    mask_fn = lambda x : int(x["Leading_team"]) != players[person_id][int(x["Game_id"])]

    # get_deficit_games = fnc.compose((fnc.filter, mask_fn))
    # deficit_games = list(get_deficit_games(all_games))
    # deficit_games = fnc.sequences.duplicatesby('Game_id', deficit_games)

    deficit_games = all_games[all_games.apply(mask_fn, axis=1)].drop_duplicates(subset="Game_id")

    total_points = 0
    num_games = 0
    for index, row in deficit_games.iterrows():
        game_id = row["Game_id"]
        player_record = bs[(bs["Game_id"] == game_id) & (bs["Person_id"] == person_id)]
        if player_record.empty:
            points_scored = 0
            players_not_in_bs.append({
                "Game_id": game_id,
                "Person_id": person_id
            })
        else:
            points_scored = int(player_record["Points"])

        total_points += points_scored
        num_games += 1
    
    return (total_points,num_games)

def get_timeouts_data():
    # timeouts_data = pd.read_csv("../data/Timeouts-3.csv")

    # timeouts = {}
    # for index, row in timeouts_data.iterrows():
    #     game_id = row["Game_id"]
    #     team_id = row["Team_id"]
    #     idx = row["index"]

    #     if game_id not in timeouts:
    #         timeouts[game_id] = {}
        
    #     timeouts[game_id][idx] = int(team_id)

    # write_to_file("timeouts.json", timeouts, is_json=True)

    timeouts = read_from_file("timeouts.json", is_json=True)

    timeouts = {float(k):v for k,v in timeouts.items()}

    for game_id in timeouts:
        record = {}
        for index in timeouts[game_id]:
            record[float(index)] = timeouts[game_id][index]

        timeouts[game_id] = record

    return timeouts

def get_box_score_data():
    # box_score_data = pd.read_csv("../data/Updated_Box_Score.csv")
    
    # box_score = {}
    # for index, row in box_score_data.iterrows():
    #     game_id = row["Game_id"]
    #     person_id = row["Person_id"]
    #     points = int(row["Points"])

    #     if game_id not in box_score:
    #         box_score[game_id] = {}
        
    #     box_score[game_id][index] = {}
    #     box_score[game_id][index][person_id] = points
    
    # write_to_file("box_score.json", box_score, is_json=True)

    box_score = read_from_file("box_score.json", is_json=True)

    box_score = {float(k):v for k,v in box_score.items()}

    for game_id in box_score:
        record = {}
        for person_id in box_score[game_id]:
            record[int(person_id)] = box_score[game_id][person_id]

        box_score[game_id] = record

    return box_score
    
def get_games():
    games = read_from_file("game_lineup.json", is_json=True)

    games = {float(k):v for k,v in games.items()}
    for game_id in games:
        teams = {}
        for team_id in games[game_id]:
            teams[int(team_id)] = games[game_id][team_id]

        games[game_id] = teams

    return games

def get_players():
    players = {float(k):v for k,v in get_all_players().items()}

    for person_id in players:
        games = {}
        for game_id in players[person_id]:
            games[int(game_id)] = players[person_id][game_id]

        players[person_id] = games
    
    return players
    
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

def write_game_data_to_file():

    games = get_all_games()

    game_lineup = {}
    for game_id in games:
        game_lineup[game_id] = {}

        for team_id in games[game_id].teams:

            game_lineup[game_id][team_id] = games[game_id].teams[team_id]["players"]

    write_to_file("game_lineup.json", game_lineup, is_json=True)

if __name__ == '__main__':
    #gl = pd.read_csv("../data/Updated_Game_Lineup.csv")

    players = get_players()
    pbp = pd.read_csv("../data/New_Play_by_Play_data_2.csv")
    pbp = pbp[pbp["Point_diff"] >= 15]
    #pbp = read_from_file("pbp.json", is_json=True)
    bs = pd.read_csv("../data/Updated_Box_Score.csv")
    #bs = get_box_score_data()
    timeouts = get_timeouts_data()
    game_lineup = get_games()
    spurt_dict = {}

    main()



