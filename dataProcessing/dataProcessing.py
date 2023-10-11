### Import libraries and load datasets
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from commonFunctions import hist, detailSummary

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
userComments.sample(10)
userComments.shape
# some users commented & gave rating more than once per game and platform
(userComments.Title + userComments.Platform + userComments.Username).nunique()
df = userComments.copy()
platformList = df.groupby('Platform')['Comment'].count().reset_index().sort_values(by = 'Comment', ascending = False).head(6).Platform.to_list()
df = userComments[userComments.Platform.isin(platformList)]
# Create a facet grid with Seaborn
g = sns.FacetGrid(df, col='Platform', col_wrap=3)
g.map(sns.histplot, 'Userscore', kde=False)

# Add labels for mean, median, SD, and IQR
for platform, ax in zip(df['Platform'].unique(), g.axes):
    platform_data = df[df['Platform'] == platform]['Userscore']
    mean = platform_data.mean()
    median = platform_data.median()
    std_dev = platform_data.std()
    iqr = platform_data.quantile(0.75) - platform_data.quantile(0.25)
    
    ax.axvline(mean, color='red', linestyle='dashed', label=f'Mean: {mean:.2f}')
    ax.axvline(std_dev, color='green', linestyle='dashed', alpha= 0, label=f'SD: {std_dev:.2f}')
    ax.axvline(median, color='blue', linestyle='dashed', label=f'Median: {median:.2f}')
    ax.axvline(iqr, color='orange', linestyle='dashed', alpha = 0, label=f'IQR: {iqr:.2f}')
    ax.legend()

# Adjust plot aesthetics
g.set_axis_labels('Userscore', '')
g.fig.suptitle('Distribution of Userscores by Platform (Most Popular 6)', fontsize=16)
g.set(ylim=(0, None))

# Show the plot
plt.subplots_adjust(top=0.85)
plt.show()

# distribution of userscores are generally similar across various platforms (join by just title with MAIN?)
title_counts = userComments.groupby('Title')['Comment'].count().reset_index().sort_values(by = 'Comment', ascending = False).head(10)
title_platform_counts = userComments.groupby(['Title', 'Platform'])['Comment'].count().reset_index()
title_platform_counts = pd.merge(title_counts[['Title']], title_platform_counts, how = 'left', on = 'Title')

df = title_platform_counts.copy()
# Pivot the data to create a DataFrame suitable for a stacked bar chart
pivot_df = df.pivot(index='Title', columns='Platform', values='Comment')

# Sort by the total number of comments in descending order
sorted_titles = pivot_df.sum(axis=1).sort_values().index
pivot_df = pivot_df.loc[sorted_titles]

# Sort platforms by the total number of comments
sorted_platforms = pivot_df.sum().sort_values(ascending=False).index
pivot_df = pivot_df[sorted_platforms]

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Use a Seaborn color palette for better colors
colors = sns.color_palette("Set3", n_colors=len(pivot_df.columns))

# Plot the stacked bar chart
bars = pivot_df.plot(kind='barh', stacked=True, color=colors, alpha=0.8, ax=ax)

ax.set_xlabel('Number of Comments', fontsize=12)
ax.set_ylabel('Title', fontsize=12)
ax.set_title('Top 10 Most Commented Games (By Platform)', fontsize=14)
ax.spines[['right', 'top']].set_visible(False)

# Add data labels to the bars
for container in bars.containers:
    ax.bar_label(container, fmt='%.0f', label_type='center', fontsize=10, color='black')

# Add legends
ax.legend(loc='upper left', bbox_to_anchor=(0.99, 1), labels=sorted_platforms, fontsize=10)

plt.tight_layout()
plt.show()

# there are uneven distribution of platform comments per game (but that does not mean that within each platform, the comment sentiments are different) ..
# .. should we generalise that the comments are similar per platform (then join by just title with MAIN?)

df = userComments.copy()
noOfComments = df.groupby(['Username', 'Title']).count().reset_index()
noOfComments.drop(columns = ['Platform', 'Userscore'], inplace = True)
noOfComments['Comment'] = noOfComments.Comment.astype('string')
df = noOfComments.copy()
# Group by Platform and Comment and calculate percentage
grouped = df.groupby(['Comment']).size().reset_index(name='Count')
total_comments = grouped['Count'].sum()
grouped['Percentage'] = (grouped['Count'] / total_comments) * 100

# Create a treemap
fig = px.treemap(grouped, 
                 path=['Comment'], 
                 values='Percentage', 
                 title='Treemap of Comments by Platform and Comment',
                 hover_data=['Percentage'],  # Display percentage in hover
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 width=1300, height=400)

# Customize hover template to show percentage values
fig.update_traces(textinfo='label+percent parent')

# Update treemap layout
fig.update_layout(
    margin=dict(t=40, b=0, l=0, r=0),
    treemapcolorway=px.colors.qualitative.Pastel,
    uniformtext=dict(minsize=10),
    hoverlabel=dict(bgcolor='white', font_size=14),
    title=dict(text='No. of Comments from same Username per Game', font=dict(size=20, color='black'), x=0.5),
)

# Show the treemap
fig.show()

# most users just comment once per game, so the data collection is pretty consistent and not skewed to repeated sampling (from same person)
userComments.Platform.unique()
platformMap = {
'DS': 'DS',
'iOS': 'iOS',
'PC': 'PC',
'PlayStation': 'PS',
'PlayStation2': 'PS2',
'PlayStation3': 'PS3',
'PlayStation4': 'PS4',
'PlayStation5': 'PS5'
}

userComments['Platform_alignedNaming'] = userComments.Platform.map(platformMap)
userComments.loc[userComments.Platform_alignedNaming == 'not specified', 'Platform_alignedNaming'] = np.NaN
userComments.Platform_alignedNaming.unique()
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