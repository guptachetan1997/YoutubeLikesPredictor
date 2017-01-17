import json
from watson_developer_cloud import ToneAnalyzerV3
from .youtube_api import getComments
import time

IBM_TONE_ANALYSER_USERNAME = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
IBM_TONE_ANALYSER_PASSWORD = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

def analyseText(paragraph):
	emotional_analysis = dict()
	if paragraph == "":
		emotional_analysis = {'fear': 0, 'sadness': 0, 'joy': 0, 'disgust': 0, 'anger': 0}
	else:
		time.sleep(4)
		tone_analyzer = ToneAnalyzerV3(username=IBM_TONE_ANALYSER_USERNAME,password=IBM_TONE_ANALYSER_PASSWORD,version='2016-05-19')
		jsonToneObj = tone_analyzer.tone(text=paragraph)
		documentTone = jsonToneObj.get("document_tone")
		if documentTone is not None:
			emotions = documentTone["tone_categories"][0]["tones"]
			for emotion in emotions:
				emotional_analysis[emotion["tone_id"]] = emotion["score"]
	return emotional_analysis

def main():
	para = getComments("lBHqdKAlYq4")
	print(analyse(para))

if __name__ == '__main__':
	main()