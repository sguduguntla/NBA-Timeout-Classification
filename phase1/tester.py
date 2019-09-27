import sys
import unittest
from game import Game
from player import Player
from lineups import get_players_and_games

# To add a new test, create a new function inside the Tester class
# and make sure the name of the function starts with the word "test"
# to tell the class that it will be a testing function

class Tester(unittest.TestCase):   

    def __init__(self, test_name):
        super(Tester, self).__init__(test_name)

    def test_games_populated_correctly(self):
        """ Checks whether the games dictionary was populated properly """
        games, players = get_players_and_games()

        self.assertIsNotNone(games)
        # Checks that there are 82 games total
        self.assertTrue(len(games) == 82)

        for id in games:
            self.assertIsInstance(obj=games[id], cls=Game)
            self.assertIsNotNone(games[id].teams)
            self.assertIsInstance(obj=games[id].teams, cls=dict)
            # Checks that there are only 2 teams in each game
            self.assertTrue(len(games[id].teams) == 2)
            team1 = list(games[id].teams.values())[0]["players"]
            team2 = list(games[id].teams.values())[1]["players"]
            # Checks that both teams in every game have 5 players
            self.assertTrue(len(team1) == 5 and len(team2) == 5)

    def test_players_populated_correctly(self):
        """ Checks whether the players dictionary was populated properly """
        games, players = get_players_and_games()

        self.assertIsNotNone(players)
        # Checks that there are 240 players total
        self.assertTrue(len(players) == 240)
        for id in players:
            self.assertIsInstance(obj=players[id], cls=Player)
            self.assertIsNotNone(players[id].ratings)
            self.assertIsInstance(obj=players[id].ratings, cls=dict)

            for game_id in players[id].ratings:
                # Checks that for each "ratings" dictionary in a Player object,
                # there is a dictionary with the "off" and "def" key/value pairs
                self.assertIsInstance(obj=players[id].ratings[game_id], cls=dict)
    
    def test_substitute(self):
        games, players = get_players_and_games()

        game_id = "006728e4c10e957011e1f24878e6054a"
        team_id = "01be0ad4af7aeb1f6d2cc2b6b6d6d811"
        player_out = "8d2127290c94bd41b82a2938734bc750"
        player_in = "ed95dff5440fadf3042b5acacea81eed"
        old_team = list(games[game_id].teams[team_id]["players"])
        games[game_id].substitute(team_id, player_out, player_in)
        new_team = list(games[game_id].teams[team_id]["players"])
        self.assertTrue(len(games[game_id].teams[team_id]["players"]) == 5)
        self.assertNotEqual(old_team, new_team)
        self.assertTrue(player_in in new_team)
        self.assertTrue(player_out not in new_team)
        self.assertTrue(player_out in old_team)
        self.assertTrue(player_in not in old_team)

    def test_update_all_players(self):
        games, players = get_players_and_games()

        game_id = "006728e4c10e957011e1f24878e6054a"
        team_id = "01be0ad4af7aeb1f6d2cc2b6b6d6d811"
        period = 2
        old_team = list(games[game_id].teams[team_id]["players"])
        games[game_id].update_all_players(team_id, period)
        new_team = list(games[game_id].teams[team_id]["players"])
        self.assertTrue(len(old_team) == 5 and len(new_team) == 5)
        self.assertNotEqual(old_team, new_team)

def run_tests():
    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(Tester)

    suite = unittest.TestSuite()
    print("TESTS: \n")
    for test_name in test_names:
        print(test_name)
        suite.addTest(Tester(test_name))

    result = unittest.TextTestRunner().run(suite)

    sys.exit(not result.wasSuccessful())
