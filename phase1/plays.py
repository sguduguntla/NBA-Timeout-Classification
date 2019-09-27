import pandas as pd
from lineups import get_players_and_games
from event_codes import get_event_codes
from tester import run_tests

def main():
    """ Starting point of the program """

    games, players = get_players_and_games()
    event_codes = get_event_codes()

    # Unit tests to make sure all data is populated and is being passed through correctly.
    # See tester.py for specific testing implementation. 
    # Comment out this line to skip running unit tests.
    #run_tests()

    df = pd.read_csv('data/UpdatedPlayByPlayNBA.csv')

    df = df.drop(columns=['Event_Num', 'Team_id_type', 'WC_Time', 'PC_Time'])

    substitutions = []

    for index, row in df.iterrows():
        game_id = row["Game_id"]
        event_type = row["Event_Msg_Type"]
        action_type = row["Action_Type"]
        points_made = float(row["Option1"])
        game = games[game_id] # Game Object
        if row["Team_id"] == '1473d70e5646a26de3c52aa1abd85b1f':
            # If the row is at the start of the first period
            team_id, other_team_id = list(games[game_id].teams.keys())
        else:
            team_id = row["Team_id"]
            other_team_id = game.other_team_id(team_id)
        
        team = game.teams[team_id] # Dictionary of Team Info
        other_team = game.teams[other_team_id] # Dictionary of Other Team Info

        period = row["Period"]

        if event_type not in [8, 3] and substitutions:
            substitute_players(game, substitutions)
            
        if event_type == 10:
            # Jump Ball
            for id in game.teams:
                if id == team_id:
                    team["is_off"]  = True
                else:
                    other_team["is_off"] = False
            
        elif event_type == 1:
            # Made Shot
            players = update_player_ratings(game_id, team, other_team, players, points_made, possession_ended=True)
            game.switch_possession()
        elif event_type == 4:
            # Rebound

            # Defensive Rebound 
            if not team["is_off"]:
                players = update_player_ratings(game_id, other_team, team, players, 0, possession_ended=True)
            game.switch_possession()
            
        elif event_type == 3:
            # Free Throw 
            ft_value = 1
            possession_ended = False

            if points_made != 1:
                ft_value = 0
            
            if action_type in [10, 12, 15, 16, 17, 20, 22, 26, 29]:
                # When any kind of free throws end
                possession_ended = True
                if action_type in [10, 12, 15] and ft_value == 1:
                    game.switch_possession()
                    
                players = update_player_ratings(game_id, team, other_team, players, ft_value, possession_ended)
                substitute_players(game, substitutions)
            else:
                players = update_player_ratings(game_id, team, other_team, players, ft_value, possession_ended)

        elif event_type == 5:
            # Turn Over
            players = update_player_ratings(game_id, team, other_team, players, 0, possession_ended=True)
            game.switch_possession()
        elif event_type == 12:
            # Start Period
            game.update_all_players(team_id, period)
            game.update_all_players(other_team_id, period)

            if not team["is_off"]:
                game.switch_possession()

        elif event_type == 8:
            # Substitution (8)
            player_out = row["Person1"]
            player_in = row["Person2"]
            sub = (team_id, player_out, player_in)

            substitutions.append(sub)
        elif event_type == 13:
            # End of a period
            players = update_player_ratings(game_id, team, other_team, players, points_made, possession_ended=True)
        
    export_to_csv(games, players)    

def substitute_players(game, substitutions):
    """ Loops through list of substitutions to be made and completes all necessary
    substitutions. Clears all substitutions after finished. 
    
    :param games: Dictionary mapping game_id's to Game objects 
    :param substitutions: List of substitution tuples: (team_id, player_out, player_in)
    """
    for sub in substitutions:
        game.substitute(sub[0], sub[1], sub[2])
    
    substitutions.clear()
    
def export_to_csv(games, players):
    """ Exports final offensive and defensive rating for every players in each game. 
    The csv file is called "The_Big_Three_Q1_BBALL.csv". 
    
    :param games: Dictionary mapping game_id's to Game objects 
    :param players: Dictionary mapping player_id's to Player objects
    """
    df = pd.DataFrame(columns=["Game_ID", "Player_ID", "OffRtg", "DefRtg"])
    
    for player in players.values():
        for game_id in player.ratings:
            off_rtg = 0
            def_rtg = 0

            if player.ratings[game_id]["off_pos"] != 0:
                off_rtg = player.ratings[game_id]["off_pts"] / player.ratings[game_id]["off_pos"] * 100
                
            if player.ratings[game_id]["def_pos"] != 0:
                def_rtg = player.ratings[game_id]["def_pts"] / player.ratings[game_id]["def_pos"] * 100
            
            df = df.append({"Game_ID":game_id, "Player_ID": player.player_id, "OffRtg": off_rtg, "DefRtg": def_rtg }, ignore_index=True)

    df.to_csv("The_Big_Three_Q1_BBALL.csv", index=False)

def update_player_ratings(game_id, off_team, def_team, players, points_made, possession_ended):
    """ Update the offensive and defensive rating for every player on the court. 
    
    :param game_id: the unique ID of the game
    :param off_team: the offensive team's Dictionary
    :param def_team: the defensive team's Dictionary
    :param players: Dictionary mapping player_id's to Player objects
    :param points_made: number of points made on certain play
    :param possession_ended: Boolean that determines if possession is ended
    """

    for player_id in off_team["players"]:
        if possession_ended:
            players[player_id].ratings[game_id]["off_pos"] += 1    
        players[player_id].ratings[game_id]["off_pts"] += points_made
    for player_id in def_team["players"]:
        if possession_ended:
            players[player_id].ratings[game_id]["def_pos"] += 1
        players[player_id].ratings[game_id]["def_pts"] += points_made
    
    return players
    
if __name__ == '__main__':
    main()