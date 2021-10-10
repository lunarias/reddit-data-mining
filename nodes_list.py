#Create the .csv nodes list for use in Gephi
#.csv in format "ID;Label;Category"
import pandas as pd
from pathlib import Path

REDDIT_ROOT_PATH = Path(__file__).parent.absolute()
USERS_DATA_PATH = "{}/data/user_data_no_user_profiles.txt".format(REDDIT_ROOT_PATH)
NODES_CSV_PATH = "{}/data/subreddit_nodes.csv".format(REDDIT_ROOT_PATH)

#Get subreddit names
df = pd.read_csv(USERS_DATA_PATH, sep='\t')
subreddits = list(df.columns.values)[2:]

#Write to .csv nodes file
file = pd.DataFrame()
index = 0

for subreddit in subreddits:
    file = file.append({'Id':str(index), 'Label': '\"%s\"'%subreddit, 'Category':''}, ignore_index=True)
    index+=1

file.to_csv(NODES_CSV_PATH, sep=';', index=False, encoding='utf-8')