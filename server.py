from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from sklearn.externals import joblib
import numpy as np
from getDataFrame import YTVFeatures
from getRawDataFromAPI import insert_video
from extractBasicFeatures import pipe
from getAdvancedFeatures import run_pipeline



app = Flask(__name__)

@app.route("/predict", methods=["POST", "GET"])
def predict():
	if request.method == "GET":
		return redirect("/")
	_id = request.form.get("video_id")
	# _id = "ljrVdQCe07U"
	client = MongoClient("localhost:27017")
	db = client.PreCog
	collection = db.YoutubeProcessed
	check = collection.find_one({"ID":_id})
	main_flag = True
	if check is not None:
		df = YTVFeatures(check).getListofFeatures()
		X = df[3:]
		Y = df[2]
	else:
		flag = insert_video(_id)
		if flag:
			pipe()
			run_pipeline()
			check = collection.find_one({"ID":_id})
			if check is not None:
				df = YTVFeatures(check).getListofFeatures()
				X = df[3:]
				Y = df[2]
			else:
				main_flag = False
		else:
			main_flag = False

	if main_flag:
		clf = joblib.load('likes_cls.pkl')
		predicted_value = int(clf.predict([X]))
		error = ((np.absolute(predicted_value-Y))/Y)*100
		return render_template("predicted.html", payload = {"video" : check, "predict" : predicted_value, "actual" : Y, "error":int(error)})
	else:
		return redirect("/")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()