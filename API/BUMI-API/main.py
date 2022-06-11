from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse, Response
from models import *
import tensorflow as tf
import pandas as pd
from helper import genreConcat, getDetails

import pyrebase
import pandas as pd
import json
from collections import OrderedDict

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings("ignore")

"""
//request user video recommendation:
{
  "user_request": [
    "string"
  ],
  "ids": [
    1,2,3,4,5,6,7,8,9,10
  ],
  "genres": [
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
  ]
}
output: "videoId YT, Judul, Deskripsi, Thumbnail"

//request user business recommendation:
{
  "user_id": int
}
output: list nama bisnis rekomendasi
"""
VIDEO_DATA_LOCATION = "umkm283.csv"
tflite_model_path = "model.tflite"
user_meta_data = {
    "user_id":"",
    "punya_usaha":"",
    "bidang_keahlian":"",
    "hobi":"",
    "modal_usaha":"",
    "nama_usaha":""
}

#############################################################################################
# FAST API INISIALIZATION
#############################################################################################
app = FastAPI()


"""
  Video Recommendation
"""
# Create TFLite interpreter.
interpreter = tf.lite.Interpreter(tflite_model_path)
interpreter.allocate_tensors()
model = Model(
    input_details = interpreter.get_input_details(),
    output_details = interpreter.get_output_details()
)
names = [
  'serving_default_context_movie_id:0',
  'serving_default_context_movie_genre:0',
  'serving_default_context_movie_rating:0',
]
indices = {i['name']: i['index'] for i in model.input_details}

#############################################################################################
# FIREBASE INISIALIZATION
#############################################################################################
config = {
    "apiKey": "AIzaSyCqHTbIfTWotR8LahossPvwwrbnIGPL6ws",
    "authDomain": "bumi-api-4e903.firebaseapp.com",
    "databaseURL": "https://bumi-api-4e903-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "bumi-api-4e903",
    "storageBucket": "bumi-api-4e903.appspot.com",
    "messagingSenderId": "909117640519",
    "appId": "1:909117640519:web:443206b8ad773e167d0662"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


#############################################################################################
# BUSINESS RECOMMENDATION
#############################################################################################
users={}
def getData(db,route):
    for r in route:
        db.child(r)
    data = db.get()
    # print(data.val())
    return data.val()

def ETL():
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
	df = pd.DataFrame()
	new_df = pd.DataFrame()
	users_from_firebase = []
	route =[
		"users"
	]   
	list_users_from_firebase = getData(db,route)
	list_users_from_firebase = (json.loads(json.dumps(list_users_from_firebase)))
	# print(list_users_from_firebase)
	users_from_firebase = []
	for i in list_users_from_firebase.items():
		users_from_firebase.append(i[1])
	# print(len(users_from_firebase))
	# users_from_firebase.remove(None)
	# print(users_from_firebase[0]["punya_usaha"])
	df = pd.DataFrame(users_from_firebase)
	# print((df.keys()))
	df["bidang_keahlian"]= df["bidang_keahlian"].apply(lambda x: x.replace("[","").replace("]","").replace("'",""))
	df["hobi"] = df["hobi"].apply(lambda x: x.replace("[","").replace("]","").replace("'",""))
	users = extract_user_datas(df)

	#Transform
	df.user_id= df.user_id.astype(str)

	#Load
	#load main datas to new dataframe will be used
	df["features"] = df["bidang_keahlian"] + "," + df["hobi"]  + "," + df["modal_usaha"]
	new_df = df[["user_id","features"]]
	new_df.features = new_df.features.apply(lambda x: x.replace(","," "))
	new_df.features = new_df.features.apply(lambda x: x.lower())
	# print(new_df.to_string())

	# # new_df

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
            "user_id":r[5],
            "punya_usaha":r[4],
            "bidang_keahlian":r[0],
            "hobi":r[1],
            "modal_usaha":r[2],
            "nama_usaha":r[3]
        }

        users[r[5]] = user_meta_data
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
	# print(users)
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
	jenis_usaha = {
		"under_50":"Usaha Mikro",
		"between_50_and_100":"Usaha Kecil",
		"above_100":"Usaha Menengah"
	}
	returnData = {}
	rekomendasi_teratas = []
	list_user = (list(users.keys()))

	#Convert Modal ke Jenis Usaha
	returnData["jenis_usaha"] = jenis_usaha[users[user_id]["modal_usaha"]]
	# print("JS", returnData)

	# print(new_df.to_string())
	if user_id not in list_user:
		print("User id tidak ditemukan")
		return 0

	if user_id not in deserved_users:
		print("Ganti nomor user yg belum punya usaha!")
		return 0
	else:
		index = new_df[new_df["user_id"] == str(user_id)].index[0]
		similarityMatrix = getSimilarityMatrix()
		# print(index+1)
		# print((similarityMatrix))
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

		for i in userRank:
			# print(i[0])
			## User ID
			if users[list_user[i[0]]]["punya_usaha"] == True and user_id != str(list_user[i[0]]) :
				rekomendasi_teratas.append(i)
				count+=1

			if count >= num_recommendation:
				break

		# print(rekomendasi_teratas) 
		# print(users[user_id])
		bidang_usaha = []
		rekomendasi = []

		for item in rekomendasi_teratas:
			# print(item[0])
			rekomendasi.extend((users[list_user[item[0]]]["nama_usaha"].replace("[","").replace("]","").replace("'","").split(",")))
			bidang_usaha.extend((users[list_user[item[0]]]["bidang_keahlian"].replace("[","").replace("]","").replace("'","").split(",")))
		returnData["rekomendasi"] = (list(set(rekomendasi)))
		returnData["bidang_usaha"] = (list(set(bidang_usaha)))
		return returnData


#############################################################################################
# API PART
#############################################################################################
"""
  API ROUTE
  /home
"""
@app.get("/")
def root():
    return RedirectResponse("http://127.0.0.1:8000/docs")

"""
  API ROUTE
  /api/v1/modelinfo
"""
@app.get("/api/v1/modelinfo")
def model_info():
    # info = {
    #     "input": model.input_details,
    #     "output": model.output_details
    # }
    return str({ \
        "input": model.input_details, \
        "output": model.output_details \
    })


"""
  API ROUTE
  /api/v1/genre
"""
@app.post("/api/v1/genre")
def getvideo(data:Genre):
  ids = tf.constant([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  switcher = {
    "Kuliner": 2,
    "Homecare": 3,
    "Healthcare": 4,
    "Tutorial": 1,
    "Ecommerce": 5,
    "Marketing": 7,
    "Review": 6
  }
  genre = switcher.get(data.genre, 0)
  genres = []

  for i in range(20):
    genres.append(genre)

  genreTensor = tf.constant(genres)
  interpreter.set_tensor(indices[names[0]], ids)
  interpreter.set_tensor(indices[names[1]], genreTensor)

  # Run inference
  interpreter.invoke()

  top_prediction_scores = interpreter.get_tensor(model.output_details[1]['index'])

  return Response(content=getDetails(top_prediction_scores), media_type="application/json")

"""
  API ROUTE
  /api/v1/inference
"""
@app.post("/api/v1/inference")
def inference(data:Datas):
  print(data)
  ids = tf.constant(data.ids)
  genreData = genreConcat(data.ids)
  print(ids)
  interpreter.set_tensor(indices[names[0]], ids)
  genres = tf.constant(genreData)
  print(genres)
  interpreter.set_tensor(indices[names[1]], genres)
  # ratings = tf.constant(data.ratings)
  # interpreter.set_tensor(indices[names[2]], ratings)

  # Run inference.
  interpreter.invoke()
  # # Get outputs.
  top_prediction_ids = interpreter.get_tensor(model.output_details[0]['index'])
  top_prediction_scores = interpreter.get_tensor(model.output_details[1]['index'])
  print('Predicted results:')
  # print('Top ids: {}'.format(top_prediction_ids))
  print('Top scores: {}'.format(top_prediction_scores))
  return Response(content=getDetails(top_prediction_scores), media_type="application/json")

"""
  API ROUTE
  /api/v1/bRecommendation
"""
@app.post("/api/v1/bRecommendation")
def bRecommendation(data: dataBRecommender):
	global new_df,df, users
	returnData = {}
	# print(data.user_id)

	df,new_df,users = ETL()
	deserved_users = get_users_who_deserved_list(users)
	# print((deserved_users))
	# print("Pilih salah 1 dari user ini")
	# print(deserved_users)
	returnData = getRecommendation(data.user_id, deserved_users, 3)

	return JSONResponse(content=returnData)