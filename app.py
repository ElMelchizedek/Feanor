#!/usr/bin/python
import os
import openai
import pandas as pd
import flask
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

import sortData

app = flask.Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Here the code interacts with the OpenAI API, using the reformatted user-centric film data from the findSimilarFilms() function, to get text that helps market the recommended films 
# according to the user's assumed tastes.
def generateAIResponse(filmData):
    try:
        response = [openai.Completion.create(
            model = "text-davinci-003",
            prompt = "Recommend the film {recTitle} in a long paragraph, emphasising its attributes described following: {recAttr}. Make sure to relate the recommendation back\
                to the user-selected film {userTitle} and its attributes: {userAttr}. Do this all the while using your own knowledge as well, while keeping the response natural\
                and adressing the user directly.".format(
                recTitle = filmData[x][0], 
                recAttr = re.sub(r'[_,]', lambda x: ' ' if x.group() == '_' else ', ', filmData[x][1]),
                userTitle = filmData[0][0],
                userAttr = re.sub(r'[_,]', lambda x: ' ' if x.group() == '_' else ', ', filmData[0][1])
                ),
            temperature = 1,
            max_tokens = 500
        ) for x in range(1, len(filmData))]
        return(response)

    except openai.errors.InvalidRequestError as e:
        print("OpenAI API error: Invalid request - {0}".format(e.message))
        return None

    except openai.errors.AuthenticationError as e:
        print("OpenAI API error: Authentication failed - {0}".format(e.message))
        return None

    except openai.errors.APIConnectionError as e:
        print("OpenAI API error: Connection failed - {0}".format(e.message))
        return None

    except openai.errors.OpenAIError as e:
        print("OpenAI API error: {0}".format(e.message))
        return None

    except Exception as e:
        print("Unexpected error: {0}".format(e))
        return None

# This part of the code takes the data from the .csv file produced by the sortData script and refactors it into a more user-friendly form, before handing into a machine-learning alogirthm 
# created using SciKit to find the 5 most similar films to the film the user has inputed. This data is then handed to the generateAIResponse() function.
def findSimilarFilms(title):
    cv = CountVectorizer()
    try:
        if not os.path.isfile("data/complete.csv"):
            data = sortData.main()
        else:
            data = pd.read_csv("data/complete.csv")
    except FileNotFoundError as e:
        print("Error: Could not find the data file.")
        print(str(e))
        return []
    except pd.errors.ParserError as e:
        print("Error: Could not parse thSpecifically, it first grabs e data file.")
        print(str(e))
        return []
    except Exception as e:
        print("Error: Could not load the data file.")
        print(str(e))
        return []

    combinedData = []
    for dataI in data.index:
        try:
             cleanGenres = re.sub(r'[^\w\s]', '_', data["genres"][dataI])
        except Exception as e:
            print("Error: Could not clean genres for index {}.".format(dataI))
            print(str(e))
            continue            
        combinedData.append(str(data["tags"][dataI]))
    
    try:
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
    except KeyError as e:
        print("Error: Could not find title {} in data file.".format(title))
        print(str(e))
        return []
    except Exception as e:
        print("Error: Could not compute similarity scores.")
        print(str(e))
        return []

# Finally, here the code both obtains the form data from index.html while also outputting back the OpenAI text from generateAIResponse() via findSimilarFilms().
@app.route("/", methods=("POST", "GET"))
def index():
    if flask.request.method == "POST":
        film = flask.request.form["film"]
        try:
            similarFilms = findSimilarFilms(film)
        except ValueError as e:
            return flask.render_template("error.html", errorMessage=str(e))
        return flask.render_template("index.html", result=[film, similarFilms])
    else:
        result = flask.request.args.get("result")
        return flask.render_template("index.html", result=result)