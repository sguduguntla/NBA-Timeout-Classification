import pandas as pd
from lineups import get_games

def main():
    #get_points_per_game()
    #get_num_stars_per_game()
    add_to_timeouts()

def get_points_per_game():
    df = pd.read_csv("../data/Updated_Box_Score.csv")

    players = {}

    stars_df = pd.DataFrame(columns=["Person_id", "season", "points_per_game"])

    for index, row in df.iterrows():
        person_id = row["Person_id"]
        season_id = row["season_id"]
        points = row["Points"]
        
        #stars_df[("Person_id" == person_id) & ("season" == season_id)]["points"][0] +=   
        if person_id in players:
            if season_id in players[person_id]:
                players[person_id][season_id]["points"] += points
                players[person_id][season_id]["games_played"] += 1
            else:
                players[person_id][season_id] = {
                    "points": points,
                    "games_played": 1
                }
        else: 
            players[person_id] = {}
            players[person_id][season_id] = {
                "points": points,
                "games_played": 1
            }
        
        print(index)

    for person_id in players:
        for season in players[person_id]:
            stars_df = stars_df.append({
                "Person_id": person_id,
                "season": season,
                "points_per_game": players[person_id][season]["points"] / players[person_id][season]["games_played"]
            }, ignore_index=True)

    stars_df.to_csv("../data/stars.csv", index=False)

def get_num_stars_per_game():
    df = pd.read_csv("../data/Timeouts.csv")
    num_stars = {} # Game id => Team id => Num stars
    points_threshold = 20
    num_stars_df = pd.DataFrame(columns=["Game_id", "Team_id", "num_stars"])
    games = get_games()

    #print(games[20400029].teams)
    stars_df = pd.read_csv("../data/stars.csv")

    c = 0

    completed_games = {} # Game id => (Team id1, Team id2)

    for index, row in df.iterrows():
        game_id = row["Game_id"]
        team_id = row["Team_id"]

        if (game_id not in completed_games) or (team_id not in completed_games[game_id]):
            season_id = row["Season"]
            player_ids = games[game_id].teams[team_id]["players"]

            for id in player_ids:
                player_record = stars_df[(stars_df["Person_id"] == id) & (stars_df["season"] == season_id - 1)]
                if player_record.empty:
                    player_record = stars_df[(stars_df["Person_id"] == id) & (stars_df["season"] == season_id)]
                
                if game_id not in num_stars:
                    num_stars[game_id] = {}

                if not player_record['points_per_game'].empty and float(player_record['points_per_game']) >= points_threshold:
                    num_stars[game_id][team_id] = num_stars[game_id].get(team_id, 0) + 1
                else:
                    num_stars[game_id][team_id] = num_stars[game_id].get(team_id, 0)
            if game_id not in completed_games:
                completed_games[game_id] = (team_id,)
            else:
                completed_games[game_id] += (team_id,)
        
        print(index)

    temp = []
    for game_id in num_stars:
        for team_id in num_stars[game_id]:
            temp.append([game_id, team_id, num_stars[game_id][team_id]])

    num_stars_df = num_stars_df.append(pd.DataFrame(temp, columns=["Game_id", "Team_id", "num_stars"]))
    num_stars_df.to_csv("../data/Num_Stars.csv", index=False)

def add_to_timeouts():
    df = pd.read_csv("../data/Timeouts-3.csv")
    num_stars_df = pd.read_csv("../data/Num_Stars.csv")
    temp = []
    for index, row in df.iterrows():
        game_id = row["Game_id"]
        team_id = row["Team_id"]
        num_star = num_stars_df[(num_stars_df["Game_id"] == game_id) & (num_stars_df["Team_id"] == team_id)]["num_stars"]
        temp.append(int(num_star))

        print(len(temp))

    df["Num_stars"] = temp
    df.to_csv("../data/Timeouts-3.csv")

if __name__ == '__main__':
    main()


    

        