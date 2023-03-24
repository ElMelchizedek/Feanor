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
        data = sortData.main(False)
    else:
        data = pd.read_csv("data/complete.csv")
    combinedData = []
    i = 0
    for dataI in data.index:
        cleanTags = re.sub(r'[^\w\s]', '', data["tags"][i])
        cleanGenres = re.sub(r'[^\w\s]', '', data["genres"][i])
        combinedData.append(cleanTags + "_" + cleanGenres)
        i += 1
    countMatrix = cv.fit_transform(combinedData)
    similarityScores = cosine_similarity(countMatrix)
    filmIndex = data[data.title == title].index.values[0]
    similarFilms = list(enumerate(cosine_similarity(countMatrix)[filmIndex]))
    similarFilms = sorted(similarFilms, key=lambda x : x[1], reverse = True)[1:]
    return str(list([data[data.index == similarFilms[x][0]]["title"].values[0] for x in range(5)]))


@app.route("/", methods=("POST", "GET"))
def index():
    if flask.request.method == "POST":
        film = flask.request.form["film"]
        return flask.redirect(flask.url_for("index", result=findSimilarFilms(film)))
        return 
    else:
        result = flask.request.args.get("result")
        return flask.render_template("index.html", result=result)
        #return findSimilarFilms(result)