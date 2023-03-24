#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
import statistics as stat
import re

os.system("")

class Debug():
    def __init__(self):
        self.toggle = False
    
    def enable(self):
        self.toggle = True
        self.alert("enabled", None, None)

    def alert(self, option, x, y):
        if self.toggle == True:
            if option == "index":
                print("\033[37m" + "INDEX " + str(x) + " OF " + str(y) + ": " + movie["title"][x])
            elif option == "noRating":
                print("\033[31m" + "NO RATING FOUND.")
            elif option == "rating":
                print("\033[32m" + "RATING FOUND.")
            elif option == "noTag":
                print("\033[31m" + "NO TAGS FOUND.")
            elif option == "tag":
                print("\033[32m" + "TAGS FOUND.")
            elif option == "enabled":
                print("\033[36m" + "DEBUG ENABLED.")
            print("\033[37m", end="")

def main(z):
    debug = Debug()
    if z == True:
        debug.enable()
    else:
        pass
    print("Loading data files...")
    global movie
    movie = pd.read_csv("data/movies.csv")
    rating = pd.read_csv("data/ratings.csv")
    tag = pd.read_csv("data/tags.csv")
    i = 0
    ratingCol = []
    tagCol = []
    titleCol = []
    yearCol = []
    print("Sorting...")
    for movieI in movie.index:
        debug.alert("index", movieI, movie.index.stop)
        average = [rating["rating"][ratingI] for ratingI in rating.loc[rating["movieId"] == movieI+1].index]
        if average:
            debug.alert("rating", None, None)
            ratingCol.insert(i, (str(stat.median(average))))
        else:
            debug.alert("noRating", None, None)
            ratingCol.insert(i, np.nan)
        tagCol.insert(i, ([(tag["tag"][tagI]) for tagI in tag.loc[tag["movieId"] == movieI+1].index]))
        tagCol[i] = [str(x).lower() for x in tagCol[i]]
        tagCol[i] = [str(x).replace(" ","") for x in tagCol[i]]
        tagCol[i] = list(dict.fromkeys(tagCol[i]))
        tagCol[i] = "_".join(tagCol[i])
        if tagCol[i]:
            debug.alert("tag", None, None)
        else:
            tagCol[i] = np.nan
            debug.alert("noTag", None, None)
        titleCol.append(movie["title"][i].split(" (")[0])
        yearCol.append(re.sub("[()]", "", movie["title"][0].split(" ")[-1]))
        i += 1
        

    complete = pd.DataFrame(
        {
            "title": titleCol,
            "year": yearCol,
            "genres": movie["genres"],
            "ratings": ratingCol,
            "tags": tagCol
        }
    )
    complete = complete.dropna()
    print("\033[33m" + "Data sorting completed.")
    print("\033[37m", end="")
    complete.to_csv("data/complete.csv", index=True)
    #return(complete)
    

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "-debug":
        z = True
    elif len(sys.argv) < 2 or sys.argv[1] != '-debug':
        z = False
    main(z)