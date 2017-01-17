import datetime
from bson.objectid import ObjectId
import re

def get_no_of_links(desc):
	http = "(http://|https://|ftp://|www)[a-zA-Z0-9\\./]+"
	matches = re.finditer(http, desc)
	return(len(list(matches)))

class YTVideo(object):
	"""
		This class extracts the basic features
		from the raw youtube data, initialises the
		advanced features and inserts into 
		new collection.
	"""
	def __init__(self, video):
		self.ID = video['id']
		self.title = video['snippet']['title']
		self.channelID = video['snippet']['channelId']
		self.channelTitle = video['snippet']['channelTitle']
		self.description = video['snippet']['description']
		self.categoryID = video['snippet']['categoryId']
		self.publishDate = video['snippet']['publishedAt']
		try:
			self.thumbnail = video['snippet']['thumbnails']['standard']['url']
		except KeyError:
			self.thumbnail = video['snippet']['thumbnails']['default']['url']
		self.duration = video['contentDetails']['duration']
		self.viewCount = video['statistics']['viewCount']
		try:
			self.commentCount = video['statistics']['commentCount']
		except:
			self.commentCount = 0
		self.likeCount = video['statistics']['likeCount']

		self.linkCount = get_no_of_links(self.description)

		str_to_bool = lambda word: 0 if word == 'false' else 1
		self.caption = str_to_bool(video['contentDetails']['caption'])

		self.thumbnailPopularity = -1

		self.channelSubscribers, self.channelViews = (-1, -1)

		try:
			self.mainTopic = video["topicDetails"]["topicIds"][0]
		except:
			self.mainTopic = "-"

		self.googleTrends = -1

	def dump(self):
		return [self.ID,self.description,self.title,self.channelID,self.channelTitle,
			self.categoryID,self.publishDate,self.thumbnail,
			self.duration,self.viewCount,self.commentCount,self.likeCount,
			self.mainTopic, self.linkCount, self.caption, self.thumbnailPopularity,
			self.channelSubscribers, self.channelViews, self.googleTrends]

	def getDICT(self):
		attribs = ["ID",
		"description",
		"title",
		"channelID",
		"channelTitle",
		"categoryID",
		"publishDate",
		"thumbnail",
		"duration",
		"viewCount",
		"commentCount",
		"likeCount",
		"mainTopic",
		"linkCount",
		"caption",
		"thumbnailPopularity",
		"channelSubscribers",
		"channelViews",
		"googleTrends"]
		attrib_values = self.dump()
		videoJsonObj = dict()
		for attrib, attrib_value in zip(attribs, attrib_values):
			videoJsonObj[attrib] = attrib_value
		return videoJsonObj

	def print(self):
		print(self.ID, self.title, self.channelTitle, self.categoryID, self.publishDate,
						self.viewCount, self.commentCount, self.likeCount)

def exportVideoMongo(video, collection):
	jsonObj = video.getDICT()
	result = collection.insert_one(jsonObj)
	print(result.inserted_id, datetime.datetime.now())

def pipe():
	objs = []
	from pymongo import MongoClient
	client = MongoClient('localhost:27017')
	db = client['PreCog']
	collection = db['YoutubeRaw']
	target_collection = db['YoutubeProcessed']
	cursor = collection.find()
	for video in cursor:
		try:
			video_data = video['items'][0]
			flag = (target_collection.find({'ID':video_data['id']})).count()
			if flag is 0:
				yt = YTVideo(video_data)
				exportVideoMongo(yt, target_collection)
		except Exception as e:
			print(e, video_data['id'], video["_id"])

if __name__ == '__main__':
	pipe()

