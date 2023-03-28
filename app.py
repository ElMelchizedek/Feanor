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


def generateAIResponse(filmData):
    response = [openai.Completion.create(
        model = "text-davinci-003",
        prompt = "Recommend the film {title} in a paragraph, emphasising its attributes described following: {attributes}.".format(title = filmData[x][0], 
            attributes = re.sub(r'[_,]', lambda x: ' ' if x.group() == '_' else ', ', filmData[x][1])),
        temperature = 0.6,
        max_tokens = 250
    ) for x in range(len(filmData))]
    return(response)

def findSimilarFilms(title):
    cv = CountVectorizer()
    if not os.path.isfile("data/complete.csv"):
        data = sortData.main()
    else:
        data = pd.read_csv("data/complete.csv")
    combinedData = []
    for dataI in data.index:
        try:
             cleanGenres = re.sub(r'[^\w\s]', '_', data["genres"][dataI])
        except:
            pass
        combinedData.append(str(data["tags"][dataI]))
        
    countMatrix = cv.fit_transform(combinedData)
    similarityScores = cosine_similarity(countMatrix)
    filmIndex = data[data.title == title].index.values[0]
    weightedSimilarityScores = []
    for i in range(len(similarityScores)):
        ratingRaw = data.loc[i, "rating"]
        ratingClean = re.sub(r'[^\d\.]', '', ratingRaw)
        ratingProper = float(ratingClean)
        weightedSimilarity = similarityScores[filmIndex][i] * ratingProper
        weightedSimilarityScores.append(weightedSimilarity)
    
    similarFilms = sorted(list(enumerate(weightedSimilarityScores)), key=lambda x: x[1], reverse=True)[1:6]
    similarFilms = [[data.iloc[i[0]]['title'], combinedData[i[0]]] for i in similarFilms]
    response = generateAIResponse(similarFilms)
    return(response)

@app.route("/", methods=("POST", "GET"))
def index():
    if flask.request.method == "POST":
        film = flask.request.form["film"]
        return flask.render_template("index.html", result=[film, findSimilarFilms(film)])
    else:
        result = flask.request.args.get("result")
        return flask.render_template("index.html", result=result)