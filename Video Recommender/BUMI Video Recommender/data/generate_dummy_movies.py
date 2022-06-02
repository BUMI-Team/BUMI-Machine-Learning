import csv
import json
import pandas as pd
# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

dir = "Video Recommender/BUMI Video Recommender/data"

# create stemmer
def stemmer(sentence):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    return stemmer.stem(sentence)

def lowerSentence(sentence):
    return sentence.lower()

def removePunctuation(sentence):
    sentence = re.sub(r"\d+", "", sentence)
    sentence = sentence.translate(str.maketrans("","", string.punctuation))
    sentence = sentence.strip()
    return sentence

def tokenize(sentence):
    sentence = stemmer(sentence)
    # print(sentence)
    sentence = lowerSentence(sentence)
    sentence = removePunctuation(sentence)
    # print(sentence)
    token = sentence.split()
    return token

def removeStopWords(tokens):
    stop_factory = StopWordRemoverFactory()
    more_stopword = []
    data = stop_factory.get_stop_words()+more_stopword
    # stopword = stop_factory.create_stop_word_remover()
    tokens_clear = []
    for token in tokens:
        if token not in data:
            tokens_clear.append(token)
        else:
            continue
    return tokens_clear


def generateGenresfromTitle(titles):
    print(len(titles))
    tokens = []
    for i in range(len(titles)):
        print("extract token, title ke-",str(i))
        # print(titles[i])
        tokens.extend(tokenize(titles[i]))
    print(tokens)
    tokens = removeStopWords(tokens)
    print(tokens)
    kemunculan = nltk.FreqDist(tokens)
    # print()
    frekuensi_token = kemunculan.most_common()
    df = pd.DataFrame(frekuensi_token)
    output = dir+"/frekuensi_token.csv"
    df.to_csv(output, index = False)


            

    
    pass 

def ETL():
    df = pd.read_csv("Video Recommender/BUMI Video Recommender/data/umkm.csv")
    # print(df["videoId"])
    # print(df["metaData"][0])

    video_id = df["videoId"]
    titles = df["title"]
    metaData = df["metaData"]
    generateGenresfromTitle(titles)
    # print(titles)

    pass

def generateGenres():
    df = pd.read_csv("Video Recommender/BUMI Video Recommender/data/umkm.csv")
    titles = df["title"]

    df2 = pd.read_csv("Video Recommender/BUMI Video Recommender/data/frekuensi_token.csv")
    tokens = df2["0"][:10]
    for title in titles:
        genre = []
        title_token = tokenize(title)
        for item in title_token:
            if item in tokens:
                genre.append(item)

    
    pass

def main():
    # ETL()
    generateGenres()
    pass

if __name__ == "__main__":
    main()