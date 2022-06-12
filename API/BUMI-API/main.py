from uuid import uuid4
from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, JSONResponse, Response
from models import *
import tensorflow as tf
import pandas as pd
from helper import *

# import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import json

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
# VIDEO_DATA_LOCATION = "umkm283.csv"
tflite_model_path = "model.tflite"
data_users_csv = "BUMI_users_data_v2.csv"
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
# BUSINESS RECOMMENDATION
#############################################################################################
users={}
## RealtimeDatabase
# def getData(db,route):
#     for r in route:
#         db.child(r)
#     data = db.get()
#     # print(data.val())
#     return data.val()

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
	# df = pd.DataFrame()
	# new_df = pd.DataFrame()
	df = pd.read_csv(data_users_csv, names=["user_id","punya_usaha","bidang_keahlian","hobi","modal_usaha","nama_usaha"], header=0)

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
    # print(row)
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
	# print(list_user)
	print(users)
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

		print(rekomendasi_teratas) 
		# print(users[user_id])
		bidang_usaha = []
		rekomendasi = []

		for item in rekomendasi_teratas:
			# print((users[list_user[item[0]]]["bidang_keahlian"].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")))
			rekomendasi.extend((users[list_user[item[0]]]["nama_usaha"].replace("[","").replace("]","").replace("'","").split(",")))
			bidang_usaha.extend((users[list_user[item[0]]]["bidang_keahlian"].replace("[","").replace("]","").replace("'","").replace(" ","").split(",")))
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
@app.post("/api/v1/genreJSON")
def getvideo(data:Genre):
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
  resdata = genreFilter(genre)
  print(resdata)

  return Response(content=getDetails(resdata[:10]), media_type="application/json")

@app.post("/api/v1/genre")
def getvideo(genre: str = Form()):
  returnData ={
    "listVideos": []
  }

  switcher = {
    "Kuliner": 2,
    "Rumah Tangga": 3,
    "Kesehatan": 4,
    "Tutorial": 1,
    "Ecommerce": 5,
    "Marketing": 7,
    "Review": 6
  }
  intGenre = switcher.get(genre, 0)
  resdata = genreFilter(intGenre)
  # print(resdata)
  datas = getDetails(resdata[:10])
  print((datas[0].id))
  for d in datas:
    returnData["listVideos"].append({
      "id": d.id,
      "genre": d.genre,
      "thumbnail": d.thumbnail,
      "description": d.description,
      "title": d.title,
      "noID": d.noID,
    })
  print(type(returnData))
  return JSONResponse(content = returnData)
  # return Response(content=getDetails(resdata[:10]), media_type="application/json")

# """
#   API ROUTE
#   /api/v1/inference
# """
# @app.post("/api/v1/inferenceJSON")
# def inference(data:Datas):
#   print(data)
#   ids = tf.constant(data.ids)
#   genreData = genreConcat(data.ids)
#   print(ids)
#   interpreter.set_tensor(indices[names[0]], ids)
#   genres = tf.constant(genreData)
#   print(genres)
#   interpreter.set_tensor(indices[names[1]], genres)
#   # ratings = tf.constant(data.ratings)
#   # interpreter.set_tensor(indices[names[2]], ratings)

#   # Run inference.
#   interpreter.invoke()
#   # # Get outputs.
#   top_prediction_ids = interpreter.get_tensor(model.output_details[0]['index'])
#   top_prediction_scores = interpreter.get_tensor(model.output_details[1]['index'])
#   print('Predicted results:')
#   # print('Top ids: {}'.format(top_prediction_ids))
#   print('Top scores: {}'.format(top_prediction_scores))
#   return Response(content=getDetails(top_prediction_scores), media_type="application/json")

@app.post("/api/v1/inference")
def inference(ids: str = Form()):
  returnData ={
    "listVideos": []
  }
  print(ids)
  idArray = ids.split(",")
  idArray = [int(x) for x in idArray]
  print([genreSplice(getGenre(x)) for x in idArray])
  # for i in x:
  #   idArray.append(int(i))
  # print(type(idArray[0]))
  idTensor = tf.constant(idArray)
  genreData = genreConcat(idArray)
  print(ids)
  interpreter.set_tensor(indices[names[0]], idTensor)
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


  datas = getDetails(top_prediction_scores)
  # print((datas[0].id))
  for d in datas:
    returnData["listVideos"].append({
      "id": d.id,
      "genre": d.genre,
      "thumbnail": d.thumbnail,
      "description": d.description,
      "title": d.title,
      "noID": d.noID,
    })
  return JSONResponse(content = returnData)
  # return Response(content=getDetails(top_prediction_scores), media_type="application/json")

"""
  API ROUTE
  /api/v1/bRecommendation
"""
@app.post("/api/v1/bRecommendation")
def bRecommendation(user_id: str = Form()):
	global new_df,df, users
	returnData = {}
	# print(data.user_id)

	df,new_df,users = ETL()
	deserved_users = get_users_who_deserved_list(users)
	# print((deserved_users))
	# print("Pilih salah 1 dari user ini")
	# print(deserved_users)
	returnData = getRecommendation(user_id, deserved_users, 3)

	return JSONResponse(content=returnData)