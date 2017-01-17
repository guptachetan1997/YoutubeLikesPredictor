# import facebook
import json
import requests
import time
import random
import datetime

GRAPH_ACCESS_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def getFacebookActivity(url):
	times = [5,6,7]
	time.sleep(random.choice(times))
	URL = "https://graph.facebook.com/v2.8/?id={}&access_token=".format(url) + GRAPH_ACCESS_TOKEN
	jsonFBObj = requests.get(URL).json()
	shares, comments = 0,0
	error_check = jsonFBObj.get("error")
	if error_check is None:
		if jsonFBObj.get("id") == url:
			share_obj = jsonFBObj.get("share")
			if share_obj is not None:
				shares = share_obj.get("share_count")
				comments = share_obj.get("comment_count")

	return (shares, comments, datetime.datetime.now().timestamp())

def main():
	print(getFacebookActivity("http://www.youtube.com/watch?v=Jrvfoybj98Q"))

if __name__ == '__main__':
	main()