#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:38:08 2019

@author: yamnihcg
"""

import pandas as pd
#@Jai and Sai - replace with '../data/Updated_Game_Lineup.csv' when running it on your computer
gameLineupData = pd.read_csv('../data/Updated_Game_Lineup.csv')
#@Jai and Sai - replace with '../data/Coach_Team_Season.csv' when running it on your computer
coachTeamSeasonData = pd.read_csv('../data/Coach_Team_Season.csv')
#@Jai and Sai - replace with '../data/Updated_Box_Score.csv' when running it on your computer
boxScoreData = pd.read_csv('../data/Updated_Box_Score.csv')
#The following are dictionaries. The key is a tuple with (teamID, season) and the value is the coach's first name / last name.
testBoxScore = boxScoreData.head(10000)
#The key in this map is a tuple of the format (teamID, season). The value in this map is the coachID
teamIDAndSeasonToCoachID = {}
coachIDToCoachName = {}
def populateIDToNameMap(coachTeamSeasonData):
    for i in range(len(coachTeamSeasonData)):
        teamID = coachTeamSeasonData['Team_ID'][i]
        season = coachTeamSeasonData['Season'][i]
        coachID = coachTeamSeasonData['Coach_ID'][i]
        teamIDAndSeasonToCoachID[(teamID, season)] = coachID

populateIDToNameMap(coachTeamSeasonData)

#Get Each Game By Itself
removeGameIDDuplicates = boxScoreData.drop_duplicates(subset=['Game_id'])
newTestBoxScore = removeGameIDDuplicates

    #Handle the dataframe indices
allIndices = newTestBoxScore.index
    
int64IndexToRegularIntArray = []

for index in range(len(allIndices)):
    temp = allIndices[index]
    int64IndexToRegularIntArray.append(temp)

def addCoachIDToBoxScoreData(newTestBoxScore, int64IndexToRegularIntArray):

    #Use the map in populateIDToNameMap to get the coachID and add them to the dataframe
    coachIDOneArr = []
    coachIDTwoArr = []
    for index in int64IndexToRegularIntArray:
        teamIDOne = newTestBoxScore['Team_id'][index]
        teamIDTwo = newTestBoxScore['vs_team_id'][index]
        season = newTestBoxScore['season_id'][index]
        coachIDOne = teamIDAndSeasonToCoachID[(teamIDOne, season)]
        coachIDTwo = teamIDAndSeasonToCoachID[(teamIDTwo, season)]
        coachIDOneArr.append(coachIDOne)
        coachIDTwoArr.append(coachIDTwo)

    newTestBoxScore['Coach_ID_1'] = coachIDOneArr
    newTestBoxScore['Coach_ID_2'] = coachIDTwoArr
    return newTestBoxScore

coachIDAddedToBoxScore = addCoachIDToBoxScoreData(newTestBoxScore, int64IndexToRegularIntArray)

coachIDAndSeasonToWins = {}
coachIDAndSeasonToLosses = {}

def getWinsAndLossesForEachSeason(coachIDAddedToBoxScore, int64IndexToRegularIntArray):
    for index in int64IndexToRegularIntArray:
        outcome = coachIDAddedToBoxScore['outcome'][index]
        season = coachIDAddedToBoxScore['season_id'][index]
        coachIDOne = coachIDAddedToBoxScore['Coach_ID_1'][index]
        coachIDTwo = coachIDAddedToBoxScore['Coach_ID_2'][index]
        
        if outcome == 'W':
            try:
                tempWins = coachIDAndSeasonToWins[(coachIDOne, season)]
                tempWins = tempWins + 1
                coachIDAndSeasonToWins[(coachIDOne, season)] = tempWins
            except KeyError:
                wins = 1
                coachIDAndSeasonToWins[(coachIDOne, season)] = wins
            try:
                tempLoss = coachIDAndSeasonToLosses[(coachIDTwo, season)]
                tempLoss = tempLoss + 1
                coachIDAndSeasonToLosses[(coachIDTwo, season)] = tempLoss
            except KeyError:
                losses = 1
                coachIDAndSeasonToLosses[(coachIDTwo, season)] = losses
        
        if outcome == 'L':
            try:
                tempLosses = coachIDAndSeasonToLosses[(coachIDOne, season)]
                tempLosses = tempLosses + 1
                coachIDAndSeasonToLosses[(coachIDOne, season)] = tempLosses
            except KeyError:
                losses = 1
                coachIDAndSeasonToLosses[(coachIDOne, season)] = losses
            try:
                tempWins = coachIDAndSeasonToWins[(coachIDTwo, season)]
                tempWins = tempWins + 1
                coachIDAndSeasonToWins[(coachIDTwo, season)] = tempWins
            except KeyError:
                wins = 1
                coachIDAndSeasonToWins[(coachIDTwo, season)] = wins

getWinsAndLossesForEachSeason(coachIDAddedToBoxScore, int64IndexToRegularIntArray)


#Maps work at this point!

coachRecordsData = []

for key in coachIDAndSeasonToWins:
    coachID = key[0]
    coachSeason = key[1]
    numberOfWins = coachIDAndSeasonToWins[key]
    numberOfLosses = coachIDAndSeasonToLosses[key]
    coachRecordsData.append([coachID, coachSeason, numberOfWins, numberOfLosses])
coachSeasonAndWinLossRecord = pd.DataFrame(coachRecordsData, columns = ['Coach ID', 'Coach Season', 'Wins', 'Losses'])
coachSeasonAndWinLossRecord.to_csv('Coach_Record_Data.csv')
        
                
            






