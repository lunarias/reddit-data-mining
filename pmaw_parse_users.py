from pmaw import PushshiftAPI
from pathlib import Path

REDDIT_ROOT_PATH = Path(__file__).parent.absolute()
USERS_PATH = "{}/data/users.txt".format(REDDIT_ROOT_PATH)

users = None
with open(USERS_PATH, 'r') as stream:
    users = set([line.split("\t")[0] for line in stream.readlines()])

api = PushshiftAPI()


subreddits = {''}
done_users = 0
for user in users:
    try:
        comments = api.search_submissions(author=user, after=1577836800, before=1609459199, mem_safe=True)
        comment_list = [comment for comment in comments]
        for comment in comment_list:
            subreddit = comment['subreddit']
            if subreddit not in subreddits:
                subreddits.add(subreddit)
        done_users += 1
    except Exception as e:
        print("{} users processed for {} unique subreddits".format(done_users, len(subreddits)-1))
        continue

print("Unique subreddits: {}".format(len(subreddits)-1))
