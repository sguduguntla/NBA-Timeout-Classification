class Player:
    def __init__(self, player_id, team_id):
        self.player_id = player_id # string player id
        self.ratings = {} # dict(gameId: dict(off_pos: 0, def_pos: 0, off_pts: 0, def_pts: 0))
        self.team_id = team_id # string team id
    
    def __str__(self):
        return "{ player_id: " + self.player_id + ", team_id: " + self.team_id + ", ratings: " + str(self.ratings) + " }"
    
    def __repr__(self):
        return "{ player_id: " + self.player_id + ", team_id: " + self.team_id + ", ratings: " + str(self.ratings) + " }"
