import os
from sys import displayhook
import numpy as np
import pandas as pd
import statistics as stat

movie = None
rating = None
tag = None

os.system("")
class style():
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

class debug():
    def __init__(self):
        self.toggle = False
    
    def enable(self):
        print(style.MAGENTA + "DEBUG ENABLED")
        self.toggle = True

    def alert(self, option, x, y):
        if self.toggle == True:
            if option == "index":
                print(style.WHITE + "INDEX " + str(x) + " OF " + str(y) + ": " + movie["title"][x])
            elif option == "ratingsList":
                print(style.YELLOW + "Length of ratings list: " + str(len(x)))
            elif option == "noRating":
                print(style.RED + "NO RATING FOUND")
            elif option == "rating":
                print(style.GREEN + "RATING FOUND")
            elif option == "duplicate":
                print(style.CYAN + "REMOVED DUPLICATE TAG")
            elif option == "noTag":
                print(style.RED + "NO TAGS FOUND")
            elif option == "tag":
                print(style.GREEN + "TAGS FOUND")

def main():
    #complete = pd.DataFrame
    Debug = debug()
    #Debug.enable()
    #complete["movieId"] = movie["movieId"]
    #complete["title"] = movie["title"]
    #complete["genres"] = movie["genres"]
    print("Set up easy columns for final data sheet.")

    i = 0
    ratingCol = []
    tagCol = []
    print("sorting ratings.")
    for movieI in movie.index:
        if i == 3:
            break
        else:
            #ratingCol.append(stat.median(average))
            #Debug.alert("index", movieI, movie.index.stop)
            print(style.WHITE + "INDEX " + str(movieI) + " OF " + str(movie.index.stop) + ": " + movie["title"][movieI])
            #if i % 100 == 0:
            #    print(style.WHITE + "INDEX " + str(movieI) + " OF " + str(movie.index.stop) + ".")
            #Debug.alert("ratingsList", ratingCol, None)
            #print("Length of ratings list: " + str(len(ratingCol)))
            #average = [0.0]
            average = [rating["rating"][ratingI] for ratingI in rating.loc[rating["movieId"] == movieI+1].index]
            if average:
                Debug.alert("rating", None, None)
                ratingCol.insert(i, (str(stat.median(average))))
            else:
                Debug.alert("noRating", None, None)
                ratingCol.insert(i, 0.0)
            tagCol.insert(i, ([(tag["tag"][tagI]) for tagI in tag.loc[tag["movieId"] == movieI+1].index]))
            tagCol[i] = [str(x).lower() for x in tagCol[i]]
            tagCol[i] = [str(x).replace(" ","") for x in tagCol[i]]
            tagCol[i] = list(dict.fromkeys(tagCol[i]))
            tagCol[i] = "_".join(tagCol[i])
            if tagCol[i]:
                Debug.alert("tag", None, None)
            else:
                tagCol[i] = ""
                Debug.alert("noTag", None, None)
            #tagCol[i] += str(newTag.replace(" ","") + "_")
            #for ratingI in rating.loc[rating["movieId"] == movieI].index:
            #    average.append(rating["rating"][ratingI])
            #if not average:
                #Debug.alert("noRating", None, None)
                #print(style.RED + "NO RATING FOUND")
            #    ratingCol.append(0.0)
                #pass
            #else:
            #    Debug.alert("rating", None, None)
                #print(style.GREEN + "RATING FOUND")
            #    ratingCol.append(stat.median(average))
            #tagCol = [str(tag["tag"][tagI]) for tagI in tag.loc[tag["movieId"]].index if not str(tag["tag"][tagI]) in tagCol[i]]
            #for tagI in tag.loc[tag["movieId"] == movieI].index:
            #    newTag = str(tag["tag"][tagI])
            #    if newTag in tagCol[i]:
            #        Debug.alert("duplicate", None, None)
            #        #print(style.CYAN + "REMOVED DUPLICATE TAG")
            #    else:
            #        tagCol[i] += newTag.replace(" ","")
            #        tagCol[i] += "_"
            #if tagCol[i] == "_":
            #    Debug.alert("noTag", None, None)
            #    #print(style.RED + "NO TAGS FOUND")
            #else:
            #    Debug.alert("tag", None, None)
                #print(style.GREEN + "TAGS FOUND")
            i += 1

    ratingCol = pd.DataFrame(ratingCol, columns = ["rating"])
    tagCol = pd.DataFrame(tagCol, columns = ["tags"])
    complete = pd.DataFrame
    complete.join(complete, ratingCol)
    #complete = complete.join(list[movie["movieId"], movie["title"], movie["genres"], ratingCol, tagCol])
    print(complete)
    #complete["rating"] = ratingCol
    #complete["tag"] = tagCol
    #print(complete.tostring())
    #complete = [x for x in complete if (complete.loc["rating"][x] == 0.0).any() and (complete.loc["tags"][x] == "").any()]
    #complete.to_csv("complete.csv", index=False)
    #complete.to_json("complete.json")
    

if __name__ == "__main__":
    print("Starting.")
    movie = pd.read_csv("data/movie.csv")
    rating = pd.read_csv("data/rating.csv")
    tag = pd.read_csv("data/tag.csv")
    complete = pd.DataFrame()
    main()