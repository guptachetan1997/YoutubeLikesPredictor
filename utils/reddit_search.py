import praw
import random
import time
import datetime

REDDIT_API_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXX'
REDDIT_API_CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXX'
REDDIT_ACCOUNT_PASSWORD = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
REDDIT_ACCOUNT_USERNAME = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def getRedditActivity(video_id):
	times = [4, 5, 6]
	time.sleep(random.choice(times))
	reddit = praw.Reddit(client_id=REDDIT_API_CLIENT_ID,
						 client_secret=REDDIT_API_CLIENT_SECRET,
						 password=REDDIT_ACCOUNT_PASSWORD,
						 user_agent='searchscript by /u/chetan1997',
						 username=REDDIT_ACCOUNT_USERNAME)
	url = "(and (field url \'https\') (field url \'www.youtube.com\') (field url \'watch\') (field url \'v\') (field url \'{}\'))".format(video_id)
	search = reddit.subreddit('all').search(query=url)
	num_posts = 0
	score = 0
	num_comments = 0
	for thing in search:
		num_posts += 1
		score += thing.score
		num_comments += thing.num_comments
	return (num_posts, score, num_comments, datetime.datetime.now().timestamp())

def main():
	print(getRedditActivity("1aVDefOvPJI"))

if __name__ == '__main__':
	main()
