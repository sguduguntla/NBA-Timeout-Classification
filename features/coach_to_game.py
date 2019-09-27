#Match Coach to Every Game in GameLineup.csv
import pandas as pd
gameLineupData = pd.read_csv('../data/Updated_Game_Lineup.csv')
coachTeamSeasonData = pd.read_csv('../data/Coach_By_Team.csv')
#The following are dictionaries. The key is a tuple with (teamID, season) and the value is the coach's first name / last name.
teamIDAndSeasonToCoachFirstName = {}
teamIDAndSeasonToCoachLastName = {}
def populateIDToNameMap(coachTeamSeasonData):
    for i in range(len(coachTeamSeasonData)):
        firstName = coachTeamSeasonData['First_Name'][i]
        lastName = coachTeamSeasonData['Last_Name'][i]
        teamID = coachTeamSeasonData['Team_ID'][i]
        season = coachTeamSeasonData['Season'][i]
        teamIDAndSeasonToCoachFirstName[(teamID, season)] = firstName
        teamIDAndSeasonToCoachLastName[(teamID, season)] = lastName

populateIDToNameMap(coachTeamSeasonData)

def matchGameLineupDataToCoach(gameLineupData):
    listOfCoachesFirstName = []
    listOfCoachesLastName = []
    for j in range(len(gameLineupData)):
        teamID = gameLineupData['Team_id'][j]
        season = int('20' + str(gameLineupData['Game_id'][2])[1:3])
        
        tempFirstName = teamIDAndSeasonToCoachFirstName[(teamID, season)]
        tempLastName = teamIDAndSeasonToCoachLastName[(teamID, season)]
        listOfCoachesFirstName.append(tempFirstName)
        listOfCoachesLastName.append(tempLastName)
    gameLineupData['Coach First Name'] = listOfCoachesFirstName
    gameLineupData['Coach Last Name'] = listOfCoachesLastName
    return gameLineupData

gameLineupDataWithCoachInfo = matchGameLineupDataToCoach(gameLineupData)
print(gameLineupDataWithCoachInfo)


        





