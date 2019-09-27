## Time Out Before Time is Up: A Classification Model to Determine Timeouts at Crucial Moments In a Game

### NBA Hackathon 2019, Secaucus, NJ

**Presented by: Sriharsha Guduguntla, Chinmay Gharpure, Jai Sankar**

In Phase 1, we completed a challenge to calculate the offensive ratings for every NBA player in the 2018 NBA Playoffs. For Phase 2, we authored a 2-page research proposal ([Link to paper](https://bit.ly/2n2FXGw)) for the model. For Phase 3, we built the classification model and presented it at the NBA Hackathon 2019 Conference in Secaucus, NJ. 

# Phase 3 - Classification Model

Among their many tough decisions, coaches often face immense criticism for choosing unnecessary or ineffective timeouts. This is seen in a recent incident from game five of the NBA finals. Raptors head coach Nick Nurse was heavily criticized for disrupting the Raptor's momentum in the fourth quarter by taking an unnecessary timeout and costing them the game. **To help decrease the frequency of these miscounts, we present a novel tool to predict whether a coach should take a timeout at a certain moment in the game. The model utilizes supervised machine learning techniques such as a SVM and neural networks to accurately formulate predictions about whether a timeout should be taken at any point in a game.**

The model was trained on a dataset of *270,132* timeouts that were taken from 2003 - 2019 and predicts at a **70.58% accuracy rate**. 

ADDITIONAL FEATURES & AREAS FOR IMPROVEMENT:

- Team Spurtability Metric - The number of games won for every player facing a 15 point deficit in a game
- Player Fatigue Score - Measure of the ratio of consecutive minutes played before and after a timeout. 
Scaling: If ratio >= 1.5, then the fatigue score is 1.
- Improve labeling by analyzing every stoppage in a game


# Phase 1 Documentation

## Plays (plays.py)

Make a new conda environment and set the python version to python3.7:

Run ```conda create --name nba-hackathon python=3.7``` to make a new conda environment called 'nba-hackathon'

Run ```conda activate nba-hackathon``` to activate the environment. 

Install **pandas** in your new environment: ```pip install pandas```

**plays.py** is the starting point for the program. Just run ```python plays.py``` in the terminal. 

Output is in **The_Big_Three_Q1_BBALL.csv**.

---

## Lineups (lineups.py)

Creates game starting lineups and initializes all games and players from **GameLineupNBA.csv**.

#### get_players_and_games()

Gets dictionary of **players** and **games** where **player_id**/**game_id** maps to a **Player**/**Game** object. 

---

## Event Codes (event_codes.py)

Creates dictionary of **Event_Msg_Type** mapping to **Event_Msg_Description** from **EventCodesNBA.csv**.

#### get_event_codes()

Gets dictionary of **Event_Msg_Type** mapping to **Event_Msg_Description**.

---

## Game Class (game.py)

The Game class keeps track of a single game and the players currently on the court for each team. 

#### Constructor
```python
def __init__(self, game_id):
     self.game_id = game_id # string game id
     self.teams = {} # dict(teamId: dict(is_off: Boolean, players: [playerIds]), teamId: dict(is_off: Boolean, players [playerIds]))
}
```
---

#### substitute(team_id, player_out, player_in)

Substitutes **player_in** with **player_out** on the team with **team_id**.

* **team_id** - the unique ID of the team
* **player_out** - the player that is substituted out
* **player_in** - the player that is substituted in

---

#### switch_possession()

Switch which team is offense. Sets "is_off" to True for the offensive team and False for the defensive team. 

---

#### other_team_id(team_id)

Gets the ID of the other team in the game besides **team_id**

* **team_id** - the unique ID of the team that the caller doesn't want.

---

#### update_all_players(team_id, period)

Resets the lineups for all the players on the team with **team_id** according the starting lineups for that **period**.

* **team_id** - the unique ID of the team
* **period** - the quarter to check for the player lineup

## Player Class (player.py)

The Player class keeps track of a single player and the offensive and defensive ratings for the player in each game. 

#### Constructor
```python
def __init__(self, player_id):
      self.player_id = player_id # string player id
      self.ratings = {} # dict(gameId: dict(off_pos: 0, def_pos: 0, off_pts: 0, def_pts: 0))
      self.team_id = team_id # string team id
```

---

## Tester (tester.py)

**tester.py** is in charge of performing all unit tests.

---

## Fix Plays (fix_plays.py)

Creates fixed **UpdatedPlayByPlayNBA.csv** by finding correct **team_ids** for all **Person1** ids in **PlayByPlayNBA.csv**. 
The Game class keeps track of a single game and the players currently on the court for each team. 
