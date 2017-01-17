import requests
import json
import pprint
import re
import time

DEVELOPER_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
API_URL = "https://www.googleapis.com/youtube/v3/videos?"

def cleanString(title):
	title = re.sub(r'[^\w\s]','',title)
	return title

def get_json_from_api(url):
	r = requests.get(url).json()
	return r

def youtube_search(ID):
	time.sleep(6)
	part = "id,snippet,contentDetails,statistics,topicDetails"
	url = API_URL + "part=" + part + "&id=" + ID + "&key=" + DEVELOPER_KEY
	return(get_json_from_api(url))

def getComments(ID):
	time.sleep(6)
	para = ""
	URL = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=50&order=relevance&textFormat=plainText&videoId={}&key={}".format(ID, DEVELOPER_KEY)
	jsonObj = get_json_from_api(URL)
	snippets = jsonObj.get("items")
	if snippets is not None:
		for snippet in snippets:
			deeper_snippet = snippet.get("snippet")
			if deeper_snippet is not None:
				topLevelComment = deeper_snippet.get("topLevelComment")
				if topLevelComment is not None:
					deepest_snippet = topLevelComment.get("snippet")
					if deepest_snippet is not None:
						text = deepest_snippet.get("textDisplay")
						para += " " + cleanString(text)
	return para


if __name__ == "__main__":
	ID = "7Qp5vcuMIlk"
	getComments(ID)