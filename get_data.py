from pmaw import PushshiftAPI
from pathlib import Path
import pandas as pd

REDDIT_ROOT_PATH = Path(__file__).parent.absolute()
USERS_DATA_PATH = "{}/data/user_data.txt".format(REDDIT_ROOT_PATH)
USERS_SORTED_100_PATH = "{}/data/users_sorted_100.txt".format(REDDIT_ROOT_PATH)

df = pd.read_csv(USERS_SORTED_100_PATH, sep='\t')
df['ucalgary'] = [1 for i in range(df.shape[0])]
df = df.drop('UCalgary_Submissions', 1)

api = PushshiftAPI()

jan_1_2020_epoch = 1577836800
dec_31_2020_epoch = 1609459199

user_activity = {}
unique_subreddits = set()
for row in df.itertuples(index=False):
    curr_subreddits = set()
    user = row.User
    posts = api.search_submissions(author=user, after=jan_1_2020_epoch, before=dec_31_2020_epoch, mem_safe=True)
    post_list = [post for post in posts]
    for post in post_list:
        subreddit = post['subreddit']
        if subreddit not in unique_subreddits:
            unique_subreddits.add(subreddit)
            curr_subreddits.add(subreddit)
            continue
        if subreddit not in curr_subreddits:
            curr_subreddits.add(subreddit)
    user_activity[user] = list(curr_subreddits)

for subreddit in unique_subreddits:
    df[subreddit] = [0 for i in range(df.shape[0])]

for index, user in enumerate(user_activity):
    for subreddit in user_activity[user]:
        df.at[index, subreddit] = 1

df.to_csv(USERS_DATA_PATH, sep="\t")
