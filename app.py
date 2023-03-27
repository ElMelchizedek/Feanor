#!/usr/bin/python
import os
import openai
import pandas as pd
import numpy as np
import flask
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import subprocess
import re

import sortData

app = flask.Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def findSimilarFilms(title):
    cv = CountVectorizer(token_pattern=r"(?<![^\s_|])[^\W_]{1,}(?![^\s|_])")
    if not os.path.isfile("data/complete.csv"):
        data = sortData.main()
    else:
        data = pd.read_csv("data/complete.csv")
    combinedData = []
    i = 0
    for dataI in data.index:
        try:
            cleanTags = re.sub(r'[^\w\s]', '', data["tags"][i])
        except:
            print("Could not get clean tag.", flush=True)
        try:
            cleanGenres = re.sub(r'[^\w\s]', '', data["genres"][i])
        except:
            print("Could not get clean genres.", flush=True)
        try:
            combinedData.append(str(cleanTags) + "_" + str(cleanGenres))
        except:
            print("Could not append to combinedData", flush=True)
        i += 1
    countMatrix = cv.fit_transform(combinedData)
    similarityScores = cosine_similarity(countMatrix)
    filmIndex = data[data.title == title].index.values[0]
    similarFilms = list(enumerate(cosine_similarity(countMatrix)[filmIndex]))
    similarFilms = sorted(similarFilms, key=lambda x : x[1], reverse = True)[1:]
    similarFilms = list([data[data.index == similarFilms[x][0]]["title"].values[0] for x in range(5)])
    print(similarFilms)
    return(similarFilms)

@app.route("/", methods=("POST", "GET"))
def index():
    if flask.request.method == "POST":
        film = flask.request.form["film"]
        return flask.render_template("index.html", result=findSimilarFilms(film))
    else:
        result = flask.request.args.get("result")
        return flask.render_template("index.html", result=result)