import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold
from sklearn.externals import joblib

"""
	Here the extracted data is sent for regression
	and generating predictions.
"""

def getR2Score(df):
	df = df.sample(frac=1).reset_index(drop=True)
	Y = df["likesCount"].values
	X = df.iloc[:, 3:].values
	kf = KFold(n_splits=10)
	r2_scores = []
	for train_index, test_index in kf.split(X):
	    X_train, X_test = X[train_index], X[test_index]
	    Y_train, Y_test = Y[train_index], Y[test_index]
	    model = KNeighborsRegressor(n_neighbors=15, weights="distance")
	    model.fit(X_train, Y_train)
	    predicts = model.predict(X_test)
	    r2_scores.append(model.score(X_test, Y_test))
	print(sum(r2_scores)/len(r2_scores))

def getPickle(dataset):
	dataset = dataset.sample(frac=1).reset_index(drop=True)
	Y = dataset["likesCount"].values
	X = dataset.iloc[:, 3:].values
	model = KNeighborsRegressor(n_neighbors=15, weights="distance")
	model.fit(X, Y)
	joblib.dump(model, "likes_cls.pkl", compress=3)

def main():
	df = pd.read_csv("dataset.csv")
	getR2Score(df)
	getPickle(df)

if __name__ == '__main__':
	main()