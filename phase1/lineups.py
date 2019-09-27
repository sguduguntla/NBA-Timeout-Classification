import pandas as pd
from game import Game
from player import Player

def get_players_and_games():

    # CSV file with all the players and every game they've played in
    gl = pd.read_csv('data/GameLineupNBA.csv')

    # Makes dictionary with key = game_id, value = Game object
    games = get_all_games(gl)

    # Makes dictionary with key = player_id, value = Player object
    players = get_all_players(gl)

    # Loops through all 240 players
    for player_id in players:
        # Populates all the games the player has played by updating the "ratings" dictionary in each Player
        # object with key = game_id, value = dictionary { "off": 0, "def": 0 } where "off" is the offensive 
        # rating and "def" is the defensive rating of the player in that particular game
        players = populate_player_games(gl, players, player_id)

        # Populates all the starting lineups in a game by updating the "teams" dictionary
        # in each Game object, with key = team_id, value = [list of player_ids on that team]
        # Every "teams" dictionary has two keys because two teams play in a game
        # Each key in the "teams" dictionary has a list of 5 players (starting lineup)
        games = populate_game_starting_lineups(gl, games, player_id)

    return games, players

def populate_game_starting_lineups(gl, games, player_id):
    """ Populates all the starting lineups in a game by updating the "teams" dictionary in each Game 
    object, with key = team_id, value = [list of player_ids on that team]
    Every "teams" dictionary has two keys because two teams play in a game
    Each key in the "teams" dictionary has a list of 5 players (starting lineup) 
    
    :param gl: Dataframe of GameLineupNBA.csv
    :param games: Dictionary mapping game_id's to Game objects 
    :param player_id: the unique id string of a player
    :return: updated games dictionary which maps game_id's to Game objects
    """

    # Filters the dataframe to find all players with the specified player_id and the starting
    # lineup denoted by period 1
    df = gl[(gl["Person_id"] == player_id) & (gl["Period"] == 1)]
    # Loop through each row of the df
    for index, row in df.iterrows():
        game_id = row["Game_id"]
        team_id = row["Team_id"]
        if team_id in games[game_id].teams:
            # If the team_id already exists in the "teams" dictionary
            # then just append the current player_id to the list of players
            # on the team
            games[game_id].teams[team_id]["players"].append(player_id)
        else:
            # If the team_id does not exist yet in the "teams" dictionary
            # then just create a new team_id key and set its value to be a new list with
            # the first player id on the team
            games[game_id].teams[team_id] = { "is_off": False, "players": [player_id] }

    # Returns the updated dictionary of games
    return games

def populate_player_games(gl, players, player_id):
    """ Populates all the games the player has played by updating the "ratings" dictionary in each Player
    object with key = game_id, value = dictionary { "off": 0, "def": 0 } where "off" is the offensive 
    rating and "def" is the defensive rating of the player in that particular game 
    
    :param gl: Dataframe of GameLineupNBA.csv
    :param players: Dictionary mapping player_id's to Player objects 
    :param player_id: the unique id string of a player
    :return: updated players dictionary which maps player_id's to Player objects
    """

    # Get rid of all the game_id duplicates because we're just looking for the one player with
    # the specified player_id. The player might have played in multiple Periods, 
    # so that's why we have to get rid of the duplicate rows.
    df = gl[gl["Person_id"] == player_id].drop_duplicates(subset="Game_id")
    # Loop through the filtered dataframe
    for index, row in df.iterrows():
        game_id = row["Game_id"]
        # Find the player object for the specified player_id and update the ratings dictionary
        # by setting the key to the game_id the player participated in and set the value
        # to a default dictionary of { "off": 0, "def": 0 }
        players[player_id].ratings[game_id] = { "off_pos": 0,"off_pts": 0, "def_pos": 0,"def_pts": 0 }
    
    # Returns the updated dictionary of players
    return players

def get_all_players(gl):
    """Takes in a game lineup dataframe and outputs dictionary of player ids mapped to Player objects
    
    :param gl: Dataframe of GameLineupNBA.csv
    :return: players dictionary which maps player_id's to Player objects
    """

    players = {}
    # Getting all the unique players in the csv
    for index, row in gl.drop_duplicates(subset ="Person_id").iterrows():
        players[row["Person_id"]] = Player(row['Person_id'], row["Team_id"])

    return players

def get_all_games(gl):
    """Takes in a game lineup dataframe and outputs dictionary of game ids mapped to Game objects
    
    :param gl: Dataframe of GameLineupNBA.csv
    :return: games dictionary which maps game_id's to Game objects
    """

    games = {}
    # Getting all the unique games in the csv
    for index, game_id in gl.drop_duplicates(subset ="Game_id")["Game_id"].iteritems():
        games[game_id] = Game(game_id)

    return games