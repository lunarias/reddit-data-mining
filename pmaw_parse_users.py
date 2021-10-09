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
        posts = api.search_submissions(author=user, after=1577836800, before=1609459199, mem_safe=True)
        post_list = [post for post in posts]
        for post in post_list:
            subreddit = post['subreddit']
            if subreddit not in subreddits:
                subreddits.add(subreddit)
        done_users += 1
    except Exception as e:
        print("{} users processed for {} unique subreddits".format(done_users, len(subreddits)-1))
        continue

print("Unique subreddits: {}".format(len(subreddits)-1))
