#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
import statistics as stat
import re
import itertools
import math
import progressbar
import time

os.system("")

def main():
    print("Loading data files...")
    completeRaw = pd.concat(map(pd.read_csv, ["data/movies.csv", "data/ratings.csv", "data/genome-tags.csv", "data/genome-scores.csv"])).drop(columns=["userId", "timestamp"])

    idArr = []
    ratingDict = {}
    tagArr = []
    tagKeyDict = {}
    titleArr = []
    yearArr = []
    genresArr = []


    print("Sorting...")
    with progressbar.ProgressBar(max_value=len(completeRaw), redirect_stdout=True) as bar:
        for (i, row) in zip(range(len(completeRaw)), completeRaw.itertuples()):
            if isinstance(row.title, str):
                idArr.append(int(row.movieId))
                titleArr.append(row.title.split(" (")[0])
                yearArr.append(re.sub("[()]", "", row.title.split(" ")[-1]))
            if not pd.isna(row.rating):
                if not int(row.movieId) in ratingDict:
                    ratingDict[int(row.movieId)] = [int(row.rating)]
                else:
                    ratingDict[int(row.movieId)].append(int(row.rating))
                    ratingDict[int(row.movieId)] = [round(stat.median(ratingDict[int(row.movieId)]) * 2) / 2]
            if not pd.isna(row.tag) and not pd.isna(row.tagId):
                tagKeyDict[row.tagId] = str(row.tag)
            if not pd.isna(row.relevance):
                tagArr.append([int(row.movieId), str(tagKeyDict.get(row.tagId)), float(row.relevance)])
            if not pd.isna(row.genres):
                genresArr.append(str(row.genres))
            bar.update(i)
    

    print("Assembling...")
    spam = pd.DataFrame(
        {
            "movieId": idArr,
            "title": titleArr,
            "year": yearArr,
            "genres": genresArr
        }
    )

    ham = pd.DataFrame(list(ratingDict.items()), columns=["movieId", "rating"])
    eggs = pd.DataFrame(tagArr, columns=["movieId", "tag", "relevance"])
    sortedTags = pd.DataFrame(columns=["movieId", "tags"])
    with progressbar.ProgressBar(max_value=len(spam.index), redirect_stdout=True) as bar:
        for i in range(len(spam.index)):
            rawTags = eggs[(eggs["movieId"] == i)].sort_values(by="relevance", ascending=False).head(20)
            tagCol = [rawTags.iloc[x, rawTags.columns.get_loc("tag")] for x in range(len(rawTags.index))]
            tagCol = [str(x).lower() for x in tagCol]
            tagCol = [str(x).replace(" ","_") for x in tagCol]
            tagCol = list(dict.fromkeys(tagCol))
            tagCol = ",".join(tagCol)
            newTagEntry = pd.Series({'movieId': i, 'tags': tagCol})
            sortedTags = pd.concat([sortedTags, newTagEntry.to_frame().T], ignore_index=True)
            bar.update(i)

    complete = pd.DataFrame(columns=["movieId", "title", "year", "genres", "rating", "tags"])
    complete = pd.merge(spam, ham, on="movieId")
    complete = pd.merge(complete, sortedTags, on="movieId")
    complete = complete.dropna()


    print("Exporting...")
    complete.to_csv("data/complete.csv", index=True)
    

if __name__ == "__main__":
    main()