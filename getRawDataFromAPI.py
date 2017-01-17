from pymongo import MongoClient
from utils.youtube_api import youtube_search
import datetime

true = True
false = False

def insert_video(ID):
	"""
		The function gets a valid YouTube ID,
		checks for its existence in database,
		if not found calls YouTube API and 
		inserts into the MongoDB database.
	"""
	client = MongoClient('localhost:27017')
	db = client['PreCog']
	collection = db['YoutubeRaw']
	check_collection = db['YoutubeProcessed']
	check = check_collection.find_one({"ID" : ID})
	if check == None:
		video = youtube_search(ID)
		if video is not None:
			result = collection.insert_one(video)
			print(result.inserted_id, datetime.datetime.now())
			return True
	else:
		print("Already in DataBase")
	return False

def main():
	pass

if __name__ == '__main__':
	main()