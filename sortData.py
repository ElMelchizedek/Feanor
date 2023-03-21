import os
import numpy as np
import pandas as pd
import statistics as stat

movie = pd.read_csv("data/movie.csv")
rating = pd.read_csv("data/rating.csv")
tag = pd.read_csv("data/tag.csv")
complete = pd.DataFrame()

def main():
    complete["movieId"] = movie["movieId"]
    complete["title"] = movie["title"]
    complete["genres"] = movie["genres"]
    print("Set up easy columns for final data sheet.")

    i = 0
    ratingCol = []
    average = [0]
    print("sorting ratings.")
    for movieI in movie.index:
        #ratingCol.append(stat.median(average))
        print("INDEX " + str(movieI) + " OF " + str(movie.index.stop) + ": " + "finding average rating for " + movie["title"][movieI])
        average.clear()
        for ratingI in rating.loc[rating['movieId'] == movieI].index:
            #print("b")
            #print(rating["rating"][ratingI])
            average.append(rating['rating'][ratingI])
            #print(average)
        if not average:
            pass
        else:
            ratingCol.append(stat.median(average))
    
    complete["ratings"] = ratingCol
    print(complete.head())

if __name__ == "__main__":
    print("Starting.")
    main()