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
        prompt = "Recommend the film {recTitle} in a long paragraph, emphasising its attributes described following: {recAttr}. Make sure to relate the recommendation back\
            to the user-selected film {userTitle} and its attributes: {userAttr}. Do this all the while using your own knowledge as well, while keeping the response natural.".format(
            recTitle = filmData[x][0], 
            recAttr = re.sub(r'[_,]', lambda x: ' ' if x.group() == '_' else ', ', filmData[x][1]),
            userTitle = filmData[0][0],
            userAttr = re.sub(r'[_,]', lambda x: ' ' if x.group() == '_' else ', ', filmData[0][1])
            ),
        temperature = 0.6,
        max_tokens = 500
    ) for x in range(1, len(filmData))]
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
    filmData = [[data[data.title == title].title.values[0], combinedData[filmIndex]]]
    filmData.extend([[similarFilms[x][0], similarFilms[x][1]] for x in range(len(similarFilms))])
    response = generateAIResponse(filmData)
    return(response)

@app.route("/", methods=("POST", "GET"))
def index():
    if flask.request.method == "POST":
        film = flask.request.form["film"]
        return flask.render_template("index.html", result=[film, findSimilarFilms(film)])
    else:
        result = flask.request.args.get("result")
        return flask.render_template("index.html", result=result)