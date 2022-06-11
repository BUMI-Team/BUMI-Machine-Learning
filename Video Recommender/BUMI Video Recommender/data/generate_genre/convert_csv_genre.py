import pandas as pd
import json
import random
import re

NUM_VIDEO = 283

def generateDummy(videoId, genres, title):
    datas = []
    # genres_chosen = []
    for i in range(NUM_VIDEO):
        # all_genres=list(map(str, genres))
        # genres_chosen = 
        # print(genres)
        # print("|".join(genres_chosen))
        data = {
            "videoId": i+1,
            "title": title[i],
            "genres": "|".join(map(str,genres[i]))
        }
        datas.append(data)
    print(datas[0])
    return pd.DataFrame(datas)

def buildGenres(kuliner, homecare, healthcare, tutorial, ecommerce, marketing, review):
    g = []
    genre =[]
    for i in range(NUM_VIDEO):
        if (kuliner[i]==1):
            genre.append("Kuliner")
        if (homecare[i]==1):
            genre.append("Homecare")
        if (healthcare[i]==1):
            genre.append("Healthcare")
        if (tutorial[i]==1):
            genre.append("Tutorial")
        if (ecommerce[i]==1):
            genre.append("Ecommerce")
        if (marketing[i]==1):
            genre.append("Marketing")
        if (review[i]==1):
            genre.append("Review")
        g.append(genre)
        genre = []
    print(g)
    # for i in range(1,10):
    #     g.append("genre " + str(i))
    return g

def ETL():
    genres = [[]]
    df = pd.read_csv("umkm283.csv",encoding='unicode_escape')
    videoId = df["Video ID"]
    title = df["Title"]
    kuliner = df["kuliner"]
    # print(kuliner)
    homecare = df["homecare"]
    healthcare = df["healthcare"]
    tutorial = df["tutorial"]
    ecommerce = df["ecommerce"]
    marketing = df["marketing"]
    review = df["review"]
    genres = buildGenres(kuliner, homecare, healthcare, tutorial, ecommerce, marketing, review)
    # print(genres)
    df2 = generateDummy(videoId, genres, title)
    print(df2)

    output = "videos"+str(NUM_VIDEO)+".csv"
    df2.to_csv(output, index = False, header = False)
    print("videos csv generated!")
    pass

def main():
    ETL()
    pass

if __name__ == "__main__":
    main()