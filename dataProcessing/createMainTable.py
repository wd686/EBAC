import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
main = pd.read_excel('../dataProcessing/outputOfJoinedTablexceptReleaseDate19862023.xlsx', sheet_name= 'Sheet1')
gameScore = pd.read_excel('../dataSources/videoGames/metascore-video-games-1986-2023.xlsx', sheet_name='Sheet1')
# 65 (0.07%) games have > 1 release date on same platform .. take the LATEST date!

gameScore_nodup = gameScore[['name', 'platform', 'release_date']].sort_values(by = ['name', 'platform', 'release_date']).drop_duplicates(keep = 'last')
a = gameScore_nodup[(gameScore_nodup.duplicated(subset=['name', 'platform'],keep = False))].sort_values(by = ['name', 'platform']).name.nunique()
print(f'{a} out of {gameScore.name.nunique()}: {round(a/gameScore.name.nunique()*100, 2)}%')

gameScore_final = gameScore[['name', 'platform', 'release_date']].sort_values(by = ['name', 'platform', 'release_date']).drop_duplicates(subset = ['name', 'platform'], keep = 'last')
gameScore.shape
gameScore_final.shape
main.platform.unique()
gameScore_final.platform.unique()
platformMap = {
'iOS': 'iOS',
'iOS (Apple Arcade)': 'iOS',
'PC': 'PC',
'PlayStation 4': 'PS4',
'PlayStation 5': 'PS5',
'Switch': 'Switch', # no mapping
'Xbox One': 'Xbox One', # no mapping
'Xbox Series X': 'Xbox Series X',
}

gameScore_final['platform'] = gameScore_final.platform.map(platformMap)
gameScore_final.platform.unique()
main.drop(columns= 'releasedate_1986-2023', inplace = True)
gameScore_final.rename(columns = {'release_date': 'releasedate_1986-2023', 'name': 'title'}, inplace = True)

mainDf = pd.merge(main, gameScore_final, how = 'left', on = ['title', 'platform'])
# Only 1421 release dates from 1986-2023 file can be mapped to main table (using title and platform as matching keys)!

mainDf['releasedate_1986-2023'].count()
mainDf.shape
mainDf.head()