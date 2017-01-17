"""
Use LokLak to get approxiamated twitter feed of 100 tweets

Then get following features from it:
Search using the cleaned titles:
so first clean the title
    1. Number of HITS
    2. Number of Countries using "place_country_code"
"""
import requests
import json
import time
import random
import datetime


def getTwitterActivity(search_string):
	times = [2,3,4,5]
	time.sleep(random.choice(times))
	search_string = "+".join(search_string.split(" "))
	BASE_URL = "http://api.loklak.org/api/search.json?&count=100&q="
	URL = BASE_URL + search_string
	jsonTA = requests.get(URL).json()
	countrySet = set()
	hits = jsonTA.get("search_metadata").get("hits")
	max_hits = jsonTA.get("search_metadata").get("maximumRecords")
	for status in jsonTA["statuses"]:
		place_country_code = status.get("place_country_code")
		if place_country_code is not None:
			countrySet.add(place_country_code)
	return(hits, max_hits, list(countrySet), datetime.datetime.now().timestamp())

def main():
	print(getTwitterActivity("Aditya and Shraddha Kapoor In Kapil Show"))

if __name__ == '__main__':
	main()