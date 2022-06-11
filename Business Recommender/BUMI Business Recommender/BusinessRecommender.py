# import os
# import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

# import nltk
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings("ignore")
"""
update matrix
rekomendasi

"""
csv_location = "Business Recommender/BUMI Business Recommender/user_input.csv"
users = {}
user_meta_data = {
    "user_id":"",
    "punya_usaha":"",
    "bidang_keahlian":"",
    "hobi":"",
    "modal_usaha":"",
    "nama_usaha":""
}




def ETL(csv_file):
    """
    input:
        csv file
    deskripsi:
        mengekstrak, transformasi data, 
        dan load data kedalam dataframe/variabel baru
    output:
        df,new_df,users
    """
    #Variabel Lokal
    users={}

    #Extract
    df = pd.read_csv(csv_file)
    df.bidang_keahlian = df.bidang_keahlian.apply(lambda x: x.replace("[","").replace("]","").replace("'",""))
    df.hobi = df.hobi.apply(lambda x: x.replace("[","").replace("]","").replace("'",""))
    users = extract_user_datas(df)
    # print(users)
    # print(df)
    # ##show statistics
    # df.info()
    # df.isnull().sum()
    # df.level
    # df.bidang_keahlian
    # df.hobi
    # df.modal_usaha

    #Transform
    df.user_id= df.user_id.astype(str)

    #Load
    #load main datas to new dataframe will be used
    df["features"] = df["bidang_keahlian"] + "," + df["hobi"]  + "," + df["modal_usaha"]
    new_df = df[["user_id","features"]]
    new_df.features = new_df.features.apply(lambda x: x.replace(","," "))
    new_df.features = new_df.features.apply(lambda x: x.lower())
    # print(new_df.to_string())

    # new_df

    return df,new_df,users

def extract_user_datas(df):
    """
    output: 
        list users
    """
    row = df.values.tolist()
    # print(row[0])
    for r in row:
        # print(r)
        user_meta_data = {
            "user_id":r[0],
            "punya_usaha":r[1],
            "bidang_keahlian":r[2],
            "hobi":r[3],
            "modal_usaha":r[4],
            "nama_usaha":r[5]
        }

        users[r[0]] = user_meta_data
    return users

def get_users_who_deserved_list(users):
    """
    input:
        list user
    deskripsi:
        Penentuan userId yang "layak" mendapatkan rekomendasi bisnis
    output: 
        list user id yang belum punya bisnis
    """
    deserved_users = []
    for key,user in users.items():
        # print(user["punya_usaha"])
        if user["punya_usaha"] == False:
            deserved_users.append(key)

    return deserved_users

        
def stem(txt):
    y = []
    porterStemmer = PorterStemmer()
    for t in txt.split():
        y.append(porterStemmer.stem(t))
    return " ".join(y)
    
def getSimilarityMatrix():
    cv = CountVectorizer(max_features = 5000)
    vectors = cv.fit_transform(new_df.features).toarray()
    
    new_df.features = new_df.features.apply(stem)
    similarityMatrix = cs(vectors)
    # print("Similarity Matrix:\n",similarityMatrix) 

    return similarityMatrix

def getRecommendation(user_id, deserved_users, num_recommendation):
    """
    input:
        user id yang belum memiliki bisnis
    deskripsi:
        Fungsi untuk mendapatkan rekomendasi bisnis
        output rekomendasi berdasarkan user2 yang sudah punya bisnis
    output:
        nama usaha rekomendasi
    """
    rekomendasi_teratas = []
    # print(new_df.to_string())
    if user_id not in deserved_users:
        print("Ganti nomor user yg belum punya usaha!")
    else:
        index = new_df[new_df["user_id"] == str(user_id)].index[0]
        similarityMatrix = getSimilarityMatrix()
        # print(type(similarityMatrix))
        distance = similarityMatrix[index]
        userRank = sorted(list(enumerate(distance)), reverse = True, key = lambda x:x[1])
        # print("Recommendation Ranking:\n",userRank)

        print("List Rekomendasi ", num_recommendation, " teratas:")
        count = 0

        """
        The Recommendation system only for he doesn't has any business
        or who has punya_usaha "belum_punya usaha". So, they will be recommended 
        the business from who have any business. The punya_usaha "true"
        will be skipped since they are not relevant to be recommended to the users
        """
        # print("UR\n",userRank)
        # print(users)
        for i in userRank:
            # print(i[0])
            ## User ID
            if users[i[0]+1]["punya_usaha"] == True and user_id != str(i[0]+1) :
                rekomendasi_teratas.append(i)
                count+=1

            if count >= num_recommendation:
                break
        # print(rekomendasi_teratas) 
        for item in rekomendasi_teratas:
            print(users[item[0]]["nama_usaha"])

def main():
    global new_df,df, users
    df,new_df,users = ETL(csv_location)
    deserved_users = get_users_who_deserved_list(users)
    # print((deserved_users))


    print("Pilih salah 1 dari user ini")
    print(deserved_users)
    getRecommendation(10000, deserved_users, 10)


if __name__ == "__main__":
    main()