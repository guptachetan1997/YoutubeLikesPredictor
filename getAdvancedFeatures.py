from pymongo import MongoClient
from utils.tin_eye import image_popularity
from utils.google_trends import SessionGoogle, trend
from utils.reddit_search import getRedditActivity
from utils.loklak_search import getTwitterActivity
from utils.facebook_search import getFacebookActivity
from utils.youtube_api import getComments
from utils.comments_analyser import analyseText
from utils.channelStats import getChannelDetails
import datetime
import random
import re

"""
	These functions are used to update/insert
	advanced features in the DataSet in the 
	MongoDB collection.
"""

def cleanString(title):
	title = re.sub(r'[^\w\s]','',title)
	return title

def updateChannelStats(collection):
	cursor = collection.find({'channelSubscribers': -1, 'channelViews' : -1})
	print("Found {} videos with missing Uploader Statistics details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		_channelID = video["channelID"]
		subs, views = getChannelDetails(_channelID)
		result = collection.update(
						{"ID":_id},
						{"$set":{"channelSubscribers":subs, "channelViews":views}}
						)
		print(_id, datetime.datetime.now())

def updateCommentsSentiment(collection):
	cursor = collection.find({'commentSentiment': {"$exists": False }})
	print("Found {} videos with missing Comment Sentiment details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		para = getComments(_id)
		if para is not None:
			sentiment = analyseText(para)
		result = collection.update(
						{"ID":_id},
						{"$set":{"commentSentiment":sentiment}}
						)
		print(_id, datetime.datetime.now())

def updateFacebookActivity(collection):
	cursor = collection.find({'facebookActivity': {"$exists": False }})
	print("Found {} videos with missing Facebook Activity details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		url = "http://www.youtube.com/watch?v=" + _id
		(shares, comments, timestamp) = getFacebookActivity(url)
		facebook = dict()
		facebook['shares'] = shares
		facebook['comments'] = comments
		facebook['timestamp'] = timestamp
		result = collection.update(
						{"ID":_id},
						{"$set":{"facebookActivity":facebook}}
						)
		print(_id, datetime.datetime.now())

def updateTwitterActivity(collection):
	cursor = collection.find({'twitterActivity': {"$exists": False }})
	print("Found {} videos with missing Twitter Activity details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		_title = cleanString(video["title"])
		(hits, max_hits, countries, timestamp) = getTwitterActivity(_title) #(random.randint(0,50), 100, [], datetime.datetime.now().timestamp())
		twitter = dict()
		twitter['hits'] = hits
		twitter['max_hits'] = max_hits
		twitter['countries'] = countries
		twitter['countries_count'] = len(countries)
		twitter['timestamp'] = timestamp
		result = collection.update(
						{"ID":_id},
						{"$set":{"twitterActivity":twitter}}
						)
		print(_id, datetime.datetime.now())

def updateRedditActivity(collection):
	cursor = collection.find({'redditActivity': {"$exists": False }})
	print("Found {} videos with missing Reddit Activity details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		(posts, score, comments, timestamp) = getRedditActivity(_id)
		reddit = dict()
		reddit['posts'] = posts
		reddit['score'] = score
		reddit['comments'] = comments
		reddit['timestamp'] = timestamp
		result = collection.update(
						{"ID":_id},
						{"$set":{"redditActivity":reddit}}
						)
		print(_id, datetime.datetime.now())

def updateThumbnailPopularity(collection):
	cursor = collection.find({'thumbnailPopularity': -1})
	print("Found {} videos with missing thumbnailPopularity details".format(cursor.count()))
	for video in cursor:
		_id = video["ID"]
		url = video['thumbnail']
		popularity = image_popularity(url)
		# if popularity != 0:
		result = collection.update(
					{"ID":_id},
					{"$set":{"thumbnailPopularity":popularity}}
					)
		print(_id, datetime.datetime.now())

def updateGoogleTrends(collection):
	cursor = collection.find({'googleTrends':-1, 'mainTopic': {"$ne":"-"}})
	print("Found {} videos with missing googleTrends details".format(cursor.count()))
	if cursor.count() != 0:
		url_login = "https://accounts.google.com/ServiceLogin"
		url_auth = "https://accounts.google.com/ServiceLoginAuth"
		session = SessionGoogle(url_login, url_auth)
	for video in cursor:
		_id = video['ID']
		mainTopic = video['mainTopic']
		trending = trend(session, mainTopic)
		result = collection.update(
					{"ID":_id},
					{"$set":{"googleTrends":trending}}
					)
		print(_id, datetime.datetime.now())

def find_dups(collection):
	cursor = collection.aggregate([
		{"$group" : {"_id": "$ID", "count":{"$sum":1}}},
		{"$match" : {"count" : {"$gte":2}}}
	])
	j=1
	to_delete = []
	for video in cursor:
		j+=1
		for i in range(video['count']-1):
			to_delete.append(video["_id"])
	print("Found {} duplicate videos with {} total duplications.".format(j, len(to_delete)))
	for _id in to_delete:
		result = collection.delete_one({"ID":_id, "thumbnailPopularity":0})

def run_pipeline():
	client = MongoClient('localhost:27017')
	db = client['PreCog']
	collection = db['YoutubeProcessed']
	from_collection = db['YoutubeRaw']
	find_dups(collection)
	updateChannelStats(collection)
	updateFacebookActivity(collection)
	updateRedditActivity(collection)
	updateTwitterActivity(collection)
	updateGoogleTrends(collection)
	updateThumbnailPopularity(collection)
	updateCommentsSentiment(collection)

if __name__ == '__main__':
	run_pipeline()
