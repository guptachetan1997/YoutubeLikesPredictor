from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime
import re

"""
	Using this class the processed database is
	exported into a csv using pandas for running
	machine learning algorithms
"""

def convertDuration(duration):
	regex = "\d+"
	matches = re.finditer(regex, duration)
	length = len(list(matches))
	if length == 3:
		starter = 3600
	elif length == 2:
		starter = 60
	else:
		starter = 1
	matches = re.finditer(regex, duration)
	seconds = 0
	for match in matches:
		seconds += int(match.group(0))*starter
		starter/=60
	return(seconds)

def elapsed_days(time1, time2):
	diff = np.absolute(time1-time2)
	days = diff/86400
	if days < 1:
		return 1
	elif days>20:
		return 20
	else:
		return days

class YTVFeatures(object):

	def __init__(self, video):

		self.id = video["ID"]
		self.title = video["title"]
		self.likesCount = int(video["likeCount"])
		self.duration = convertDuration(video["duration"])
		self.viewCount = int(video["viewCount"])
		self.caption = video["caption"]
		self.thumbnailPopularity = int(video["thumbnailPopularity"])
		self.categoryID = int(video["categoryID"])
		self.descriptionLinkCount = int(video["linkCount"])
		self.googleTrends = int(video["googleTrends"])

		self.channelSubs = video["channelSubscribers"]
		self.channelViews = video["channelViews"]
		try:
			self.ViewPerSubs = int(self.channelViews)/int(self.channelSubs)
		except Exception as e:
			print(e)
			self.ViewPerSubs = 0

		self.publishDate =  datetime.datetime.strptime(video["publishDate"][:10], "%Y-%m-%d").timestamp()

		self.redditPosts = video["redditActivity"]["posts"]/elapsed_days(video["redditActivity"]["timestamp"], self.publishDate)
		self.redditScore = video["redditActivity"]["score"]/elapsed_days(video["redditActivity"]["timestamp"], self.publishDate)
		self.redditComments = video["redditActivity"]["comments"]/elapsed_days(video["redditActivity"]["timestamp"], self.publishDate)

		self.twitterHits = video["twitterActivity"]["hits"]/elapsed_days(video["twitterActivity"]["timestamp"], self.publishDate)
		self.twitterCountries = video["twitterActivity"]["countries_count"]/elapsed_days(video["twitterActivity"]["timestamp"], self.publishDate)

		self.facebookShares = video["facebookActivity"]["shares"]/elapsed_days(video["facebookActivity"]["timestamp"], self.publishDate)

		self.commentCount = int(video["commentCount"])

		self.commentAnger = video["commentSentiment"]["anger"]
		self.commentDisgust = video["commentSentiment"]["disgust"]
		self.commentFear = video["commentSentiment"]["fear"]
		self.commentJoy = video["commentSentiment"]["joy"]
		self.commentSadness = video["commentSentiment"]["sadness"]

	def getListofFeatures(self):
		return [self.id, self.title, self.likesCount, self.duration, self.viewCount, 
				self.caption,self.thumbnailPopularity, self.categoryID, 
				self.descriptionLinkCount, self.googleTrends, self.ViewPerSubs,
				self.redditPosts, self.redditScore,
				self.redditComments, self.twitterHits, self.twitterCountries,
				self.facebookShares, self.commentCount, self.commentAnger,
				self.commentDisgust, self.commentFear, self.commentJoy,
				self.commentSadness]

def exportCSV(videos):
	cols = ["id",
			"title",
			"likesCount",
			"duration",
			"viewCount",
			"caption",
			"thumbnailPopularity",
			"categoryID",
			"descriptionLinkCount",
			"googleTrends",
			"viewPerSubs",
			"redditPosts",
			"redditScore",
			"redditComments",
			"twitterHits",
			"twitterCountries",
			"facebookShares",
			"commentCount",
			"commentAnger",
			"commentDisgust",
			"commentFear",
			"commentJoy",
			"commentSadness"]
	df = pd.DataFrame(columns = cols)
	for video in videos:
		videoObj = YTVFeatures(video)
		df = df.append(pd.DataFrame([videoObj.getListofFeatures()], columns=cols))
	filename = "dataset"
	df.to_csv(filename + ".csv", index=False)

def main():
	client = MongoClient("localhost:27017")
	db = client["PreCog"]
	collection = db["YoutubeProcessed"]
	cursor = collection.find()
	exportCSV(cursor)

if __name__ == '__main__':
	main()
