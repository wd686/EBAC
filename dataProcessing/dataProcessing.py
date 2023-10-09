### Import libraries and load datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from commonFunctions import hist

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
### Load datasets
# based on what columns we deem necessary, may need to rename df/ column names
# need to choose the impt Score/ Rating/ metacritic Matrix defined to be from Beta testers (we've too many)
# standardise release_date if it's impt

userComments1 = pd.read_csv('../dataSources/videoGames/metacritic_game_user_comments (0-100k).csv')
userComments2 = pd.read_csv('../dataSources/videoGames/metacritic_game_user_comments (100-200k).csv')
userComments3 = pd.read_csv('../dataSources/videoGames/metacritic_game_user_comments (200-300k).csv')

gameInfo = pd.read_csv('../dataSources/videoGames/metacritic_game_info.csv')
ratingsAndReleaseDate = pd.read_csv('../dataSources/videoGames/updatedVGOutput.csv')
gameScore = pd.read_excel('../dataSources/videoGames/metascore-video-games-1986-2023.xlsx', sheet_name='Sheet1')
gameSales = pd.read_excel('../dataSources/videoGames/Video game sales - 2000 - 2020.xlsx', sheet_name= 'Sheet1')
# userComments[~(userComments.Title.isin(gameSales.title))].groupby('Title').count().sort_values(by = 'Comment', ascending = False)
# can join via title/name
print(f"userComments1: {userComments1.columns}\n\ngameInfo:{gameInfo.columns}\n\nratingsAndReleaseDate: {ratingsAndReleaseDate.columns}\n\ngameScore: {gameScore.columns}\n\ngameSales: {gameSales.columns}")
# some users commented & gave rating more than once per game and platform (unique only when combine all cols)
userComments1.head()
# (gameInfo.Title + gameInfo.Year.astype(str) + gameInfo.Publisher + gameInfo.Genre + gameInfo.Platform).nunique()
gameInfo.head()
# ratingsAndReleaseDate.name.nunique()
ratingsAndReleaseDate.head()
# ratingsAndReleaseDate.shape = 209
gameScore.head()
gameSales.head()
### userComments
# userComments.groupby('Title').first().sort_values(by = 'Title').reset_index()
userComments3['Unnamed: 0'] = userComments3['Unnamed: 0'].astype('float64')
userComments3['Userscore'] = userComments3['Userscore'].astype('float64')

userComments = pd.concat([userComments1, userComments2, userComments3], axis = 0)
userComments.drop(columns = 'Unnamed: 0', inplace = True)
userComments.dropna(how = 'all', inplace = True)
# Comments >> 23 missing entries
# Username   >> 3 missing entries
userComments.info()
userComments.describe()
hist(userComments, 'Userscore')
userComments.head()
userComments.shape
# some users commented & gave rating more than once per game and platform
(userComments.Title + userComments.Platform + userComments.Username).nunique()
userComments[['Title', 'Comment']].groupby('Title').count().reset_index().sort_values(by = 'Comment', ascending = False).head(10)




### gameInfo
gameInfo.drop(columns = 'Unnamed: 0', inplace = True)
gameInfo.loc[gameInfo.Metascore == 'not specified', 'Metascore'] = -999
gameInfo['Metascore'] = gameInfo.Metascore.astype('float64')

gameInfo.loc[gameInfo.Avg_Userscore == 'not specified', 'Avg_Userscore'] = -999
gameInfo.loc[gameInfo.Avg_Userscore == 'tbd', 'Avg_Userscore'] = -998
gameInfo['Avg_Userscore'] = gameInfo.Avg_Userscore.astype('float64')

gameInfo.loc[gameInfo.Year == 'not specified', 'Year'] = -999
gameInfo['Year'] = gameInfo.Year.astype('int64')
gameInfo = gameInfo[gameInfo.Year != -999] # 11 rows removed (all Metascore = -999 are removed too)
gameInfo = gameInfo[gameInfo.Avg_Userscore != -999] # 1 row removed

gameInfo[gameInfo.Avg_Userscore == -998].shape # 75 rows .. keep? not sure if this col is impt
# No_Players >> 52 categories .. combine them??
gameInfo.No_Players.value_counts().shape
# gameInfo.No_Players.value_counts()
# gameInfo.No_Players.value_counts()
# No_Players .. 7 missing entries
gameInfo.info()
gameInfo.Metascore.describe()
for x in gameInfo.select_dtypes(include=['Int64', 'float64']):
    if x == 'Avg_Userscore':
        test = gameInfo[gameInfo[x] != -998]
        hist(test, x)
    else:
        hist(gameInfo, x)
gameInfo.head()
gameInfo.shape
gameInfo.Title.nunique()
(gameInfo.Title + gameInfo.Year.astype(str) + gameInfo.Developer + gameInfo.Genre + gameInfo.Platform).nunique()
### ratingsAndReleaseDate
ratingsAndReleaseDate.head()
# unique names!
ratingsAndReleaseDate.shape
ratingsAndReleaseDate.name.nunique()
### gameScore
gameScore.user_score.count()
gameScore.meta_score.count()
gameScore.shape
(gameScore.name + gameScore.platform + gameScore.release_date.astype(str)).nunique()
### gameSales
gameSales.shape
(gameSales.title + gameSales.platform + gameSales.genre + gameSales.publisher).nunique()