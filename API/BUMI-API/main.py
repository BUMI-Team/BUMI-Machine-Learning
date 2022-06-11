from uuid import uuid4
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import *
import tensorflow as tf
import pandas as pd
import json
"""
request user video recommendation:
{
  "user_request": [
    "string"
  ],
  "ids": [
    1,2,3,4,5,6,7,8,9,10
  ],
  "genres": [
    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
  ],
  "ratings": [
    1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0
  ]
}
output: "videoId YT, Judul, Deskripsi, Thumbnail"

request user business recommendation:
{
  "user_id": int
}
output: list nama bisnis rekomendasi


"""
VIDEO_DATA_LOCATION = "umkm283.csv"

app = FastAPI()
tflite_model_path = "model.tflite"
# Create TFLite interpreter.
interpreter = tf.lite.Interpreter(tflite_model_path)
interpreter.allocate_tensors()
model = Model(
    input_details = interpreter.get_input_details(),
    output_details = interpreter.get_output_details()
)
# Find indices.
names = [
  'serving_default_context_movie_id:0',
  'serving_default_context_movie_genre:0',
  'serving_default_context_movie_rating:0',
]
indices = {i['name']: i['index'] for i in model.input_details}

@app.get("/")
def root():
    return RedirectResponse("http://127.0.0.1:8000/docs")

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


@app.post("/api/v1/inference")
def inference(data:Datas):
	returnData = []
	print(data)
	ids = tf.constant(data.ids)
	print(ids)
	interpreter.set_tensor(indices[names[0]], ids)
	genres = tf.constant(data.genres)
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

	df = pd.read_csv(VIDEO_DATA_LOCATION)

	print(df.to_string()) 

	return 'List rekomendasi: {}'.format(top_prediction_scores)

@app.post("/api/v1/bRecommendation")
def bRecommendation(data: dataBRecommender):
	print(dataBRecommender)
	pass





# @app.delete("/api/v1/users/{user_id}")
# async def delete_user(user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             db.remove(user_id)
#             return

# @app.put("/api/v1/users/{user_id}")
# async def update_user(user_update: UserUpdateRequest, user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             if user_update.first_name is not None:
#                 user.first_name = user_update.first_name
#             if user_update.last_name is not None:
#                 user.last_name = user_update.last_name
#             if user_update.middle_name is not None:
#                 user.middle_name = user_update.middle_name
#             if user_update.roles is not None:
#                 user.roles = user_update.roles
#             return