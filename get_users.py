"""
    This module gets a list of all users who made posts in r/UCalgary in 2020, 
    sorted by descending number of posts made.
"""
from pmaw import PushshiftAPI
from pathlib import Path
import pandas as pd

REDDIT_ROOT_PATH = Path(__file__).parent.absolute()
USERS_PATH = "{}/data/users.txt".format(REDDIT_ROOT_PATH)

users = {}

# start of day jan 1 2020
jan_1_2020_epoch = 1577836800
# end of day dec 
dec_31_2020_epoch = 1609459199
# get all posts made in ucalgary in 2020
posts = api.search_submissions(after=jan_1_2020_epoch, before=dec_31_2020_epoch, subreddit="UCalgary", mem_safe=True)
# track how many posts every user made
for post in posts:
    if post.author not in users:
        users[author] = 1
    else:
        users[author] += 1

user_activity = pd.DataFrame(users, columns=['User', 'UCalgary_Submissions'])
# sort table by desc posts made
df.sort_values(by=['UCalgary_Submissions'])
df.to_csv(USERS_PATH, sep="\t")