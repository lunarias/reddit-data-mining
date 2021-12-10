#Create the .csv edges list for use in Gephi
#.csv in format "Source;Target;Weight"
import pandas as pd
from pathlib import Path

REDDIT_ROOT_PATH = Path(__file__).parent.absolute()
USERS_DATA_PATH = "{}/data/user_data_no_user_profiles.txt".format(REDDIT_ROOT_PATH)
EDGES_CSV_PATH = "{}/data/subreddit_edges.csv".format(REDDIT_ROOT_PATH)

#read users data
df_user = pd.read_csv(USERS_DATA_PATH, sep='\t')

#parse the users data and get edges for subreddit nodes
file = pd.DataFrame()
edges_dict = {}
for user_index in range(len(df_user)):
    subreddits = df_user.loc[user_index][3:].to_frame().reset_index().rename(columns = {'index':'subreddit'})
    active_subreddits = subreddits.loc[subreddits[user_index]==1]
    active_subreddits_list = active_subreddits.index.tolist()

    for i in range(len(active_subreddits_list)):
        for j in range(i+1, len(active_subreddits_list)):
            key = (active_subreddits_list[i],active_subreddits_list[j])
            if key in edges_dict:
                value = edges_dict[key]
                edges_dict[key] = value + 1
            else:
                edges_dict[key] = 1

# formatting the result and creating the csv file
edges_list = sorted(edges_dict.items())
for edge in edges_list:
    file = file.append({'Source': str(edge[0][0]), 'Target': str(edge[0][1]), 'Weight':str(edge[1])}, ignore_index=True)

file.to_csv(EDGES_CSV_PATH, sep=';', index=False, encoding='utf-8')