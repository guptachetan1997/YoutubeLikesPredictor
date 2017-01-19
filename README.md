YouTube Likes Count Prediction
-----------------------------
This method uses various OSM platforms' data to predict likes on a YouTube video
![alt tag](https://github.com/guptachetan1997/YoutubeLikesPredictor/blob/master/pipeline.jpg)

Steps to run (Assuming Ubuntu 16.04 with python3.X and mongoDB installed and setup):

First install all the requirements:

```
$ pip3 install -r requirements.txt
```

Next import the raw.json and processed.json as : 
```
$ mongoimport -d PreCog -c YoutubeRaw -h localhost:27017 raw.json
$ mongoimport -d PreCog -c YoutubeProcessed -h localhost:27017 processed.json
```
Now if you do not want to add the required API credentials, for testing purpose you can use the video IDS in 'testVideos.txt' via the Flask Web App.
```
$ python3 server.py
```

To run for any video add the following detials to the mentioned files : 

- Ibm Tone Analyser Credentials - utils/comments_analyser.py
- Facebook Graph API access token - utils/facebook_search.py
- Google Account Details - utils/google_trends.py
- Reddit API details - utils/reddit_search.py
- YouTubeAPI developer KEY - utils/youtube_api.py


Finally run : 
```
$ python3 server.py
```
You should now be able to use the flask webapp (http://localhost:5000/) to make predictions
