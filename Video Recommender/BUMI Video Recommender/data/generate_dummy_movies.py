import pandas as pd
import json
import random
import re

dir = "Video Recommender/BUMI Video Recommender/data"
NUM_VIDEO = 200
MAX_GENRE = 7
MIN_GENRE = 2


def adaptTitle(df):
    titles = []
    df["metaData"] = df["metaData"].apply(lambda x: x.replace("\'","\""))
    for i in range(len(df)):
        tanggal = json.loads(df["metaData"][0])["snippet"]["publishedAt"]
        year = re.search(r"(\d{4})-(\d{2})", tanggal)[1] 
        titles.append(df["title"][i] +" ("+year+")")
    print(year)
    # pass
    return titles


def generateDummy(videoId, genres,new_titles):
    random.seed(10)

    datas = []
    for i in range(NUM_VIDEO):
        num_genre = random.randint(MIN_GENRE,MAX_GENRE)
        genres_chosen = sorted(random.sample(genres, num_genre))
        # print(genres_chosen)
        # print("|".join(genres_chosen))
        data = {
            "videoId": i,
            "title": new_titles[i],
            "genres": "|".join(genres_chosen)
        }
        datas.append(data)
    # print(datas[0])
    return pd.DataFrame(datas)

def buildGenres():
    g = []
    for i in range(10):
        g.append("genre " + str(i))
    return g

def ETL():
    genres = []
    df = pd.read_csv("Video Recommender/BUMI Video Recommender/data/umkm.csv")
    videoId = df["videoId"]
    genres = buildGenres()
    # print(genres)
    new_titles = adaptTitle(df)
    # print(titles[0])
    df2 = generateDummy(videoId, genres, new_titles)
    print(df2)


    output = dir+"/movies"+str(NUM_VIDEO)+".csv"
    df2.to_csv(output, index = False, header = False)
    print("movies csv generated!")
    pass

def main():
    ETL()
    
    # print(json.loads(a.replace("\'","\"")))
    pass

if __name__ == "__main__":
    main()