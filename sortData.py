#!/usr/bin/python
import pandas as pd
import statistics as stat
import re
import itertools
import progressbar

def main():
    # Combines the various .csv files provided by the MovieLens dataset into one "Frankenstein" Pandas DataFrame for manipulation.
    print("Loading data files...")
    try:
        completeRaw = pd.concat(map(pd.read_csv, ["data/movies.csv", "data/ratings.csv", "data/genome-tags.csv", "data/genome-scores.csv"])).drop(columns=["userId", "timestamp"])

        idArr = []
        ratingDict = {}
        tagArr = []
        tagKeyDict = {}
        titleArr = []
        yearArr = []
        genresArr = []
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found. Please check that the file path is correct and try again.")
    except pd.errors.EmptyDataError as e:
        print("Error: One of the input data files is empty. Please check the data files and try again.")
    except pd.errors.ParserError as e:
        print("Error: Unable to parse one of the input data files. Please check the data files and try again.")
    except pd.errors.MergeError as e:
        print("Error: Unable to merge the input data files. Please check the data files and try again.")
    except Exception as e:
        print("Error:", e)

    # Iterates through the completeRaw dataframe to format what can be done without complicating the code, while also primarily splitting the data up into smaller sets for further
    # manipualtion. Notably, it removes the parantheses from the "title" column and breaks off the year from the column, and also gains the statistical median of the rating for each 
    # film.
    print("Sorting...")
    try:
        with progressbar.ProgressBar(max_value=len(completeRaw), redirect_stdout=True) as bar:
            for (i, row) in zip(range(len(completeRaw)), completeRaw.itertuples()):
                try:
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
                except Exception as e:
                    print(f"Error processing row {i}: {e}")
    except pd.errors.EmptyDataError:
        print("Error: One or more of the input data files are empty")
    except pd.errors.ParserError:
        print("Error: One or more of the input data files could not be parsed")
    except pd.errors.DtypeWarning:
        print("Warning: One or more columns in the input data files could not be parsed correctly")
    except Exception as e:
        print(f"Error: {e}")

    # Here the code commits itself to the most tedious of data manipulation, that being the reformatting of the "tag" columns into something useful, which is carried out mostly by simple 
    # string manipulation. Then all the extant DataFrames are combined into a clean, "fixed" DataFrame.
    print("Assembling...")
    try:
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

    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}. There is no data to assemble.")
    except pd.errors.MergeError as e:
        print(f"Error: {e}. An error occurred while merging dataframes. Check that the columns used for merging exist and are the same data type in all dataframes.")
    except pd.errors.ParserError as e:
        print(f"Error: {e}. An error occurred while parsing the data files. Check that the files are correctly formatted as CSVs.")
    except pd.errors.DtypeWarning as e:
        print(f"Error: {e}. An error occurred while merging dataframes. Check that the columns used for merging have the same data type in all dataframes.")
    except KeyError as e:
        print(f"Error: {e}. A KeyError occurred while assembling the data. Check that the data files have the necessary columns.")
    except ValueError as e:
        print(f"Error: {e}. A ValueError occurred while assembling the data. Check that the data files have the necessary values and that they are the correct data type.")
    except Exception as e:
        print(f"An unexpected error occurred while assembling the data: {e}.")

    # Finally, the DataFrame is exported as a .csv file for use in the web app proper.
    print("Exporting...")
    try:
        complete.to_csv("data/complete.csv", index=True)
    except IOError as e:
        print("Error exporting data:", e)

if __name__ == "__main__":
    main()