import pandas as pd

class Game:
    def __init__(self, game_id):
        self.game_id = game_id # int game id
        self.teams = {} # dict(teamId: dict(is_off: Boolean, players: [playerIds]), teamId: dict(is_off: Boolean, players: [playerIds]))
    
    def substitute(self, team_id, player_out, player_in):
        """ Substitutes player_in with player_out on the team with team_id. 
    
        :param team_id: the unique ID of the team
        :param player_out: the player id of the player that is substituted out 
        :param player_in: the player id of the player that is substituted in
        """

        self.teams[team_id]["players"].remove(player_out)
        self.teams[team_id]["players"].append(player_in)

    def switch_possession(self):
        """ Switch which team is offense. Sets "is_off" to True for the offensive team and False for the defensive team. """
        
        for team_id in self.teams:
            self.teams[team_id]["is_off"] = not self.teams[team_id]["is_off"]
    
    def other_team_id(self, team_id):
        """ Gets the ID of the other team in the game besides team_id
        
        :param team_id: the unique ID of the team
        """
        for key in self.teams:
            if key != team_id:
                return key
                
    def update_all_players(self, team_id, period):
        """ Resets the lineups for all the players on the team with team_id according the starting lineups for that period.

        :param team_id: the unique ID of the team
        :param period: the quarter to check for the player lineup
        """ 
        df = pd.read_csv("data/GameLineupNBA.csv")
        new_player_rows = df.loc[(df['Game_id'] == self.game_id) & (df['Period'] == period) & (df['Team_id'] == team_id)]
        self.teams[team_id]["players"].clear()
        for index, player_id in new_player_rows['Person_id'].iteritems():
            self.teams[team_id]["players"].append(player_id)
    
    def __str__(self):
        return "{ game_id: " + str(self.game_id) + ", teams: " + str(self.teams) + " }"
    
    def __repr__(self):
        return "{ game_id: " + str(self.game_id) + ", teams: " + str(self.teams) + " }"