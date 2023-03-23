import os
import sys
import pandas as pd
import statistics as stat

movie = None
rating = None
tag = None

os.system("")

class debug():
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

def main(Debug):
    i = 0
    ratingCol = []
    tagCol = []
    print("Sorting...")
    for movieI in movie.index:
        Debug.alert("index", movieI, movie.index.stop)
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
        i += 1

    complete = pd.DataFrame(
        {
            "title": movie["title"],
            "genres": movie["genres"],
            "ratings": ratingCol,
            "tags": tagCol
        }
    )
    print("\033[33m" + "Data sorting completed.")
    print("\033[37m", end="")
    complete.to_csv("complete.csv", index=False)
    

if __name__ == "__main__":
    Debug = debug()
    if len(sys.argv) >= 2 and sys.argv[1] == "-debug":
        Debug.enable()
    elif len(sys.argv) < 2 or sys.argv[1] != '-debug':
        pass
    print("Loading data files...")
    movie = pd.read_csv("data/movies.csv")
    rating = pd.read_csv("data/ratings.csv")
    tag = pd.read_csv("data/tags.csv")
    main(Debug)