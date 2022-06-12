import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import json

NUM_USER = 50
data_dir = "API/BUMI_users_data.csv"
metadata_file = 'Business Recommender/BUMI Business Recommender/synthetic_metadata.json'

cred = credentials.Certificate("API/bumi-api-4e903-firebase-adminsdk-75pgu-b7278330a6.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
users={}

def extract_from_csv():
    data = {}
    df = pd.read_csv(data_dir, index_col=None)
    records = df.to_dict(orient='records')
    print(type(records))
    for i in records:
        user_id = i["user_id"]
        punya_usaha = i["punya_usaha"]
        bidang_keahlian = i["bidang_keahlian"]
        hobi = i["hobi"]
        modal_usaha = i["modal_usaha"]
        nama_usaha = i["nama_usaha"]

        data["user_id"] = user_id
        data["punya_usaha"] = punya_usaha
        data["bidang_keahlian"] = bidang_keahlian
        data["hobi"] = hobi
        data["modal_usaha"] = modal_usaha
        data["nama_usaha"] = nama_usaha
        print(data)
        route =[
            "users",
            user_id
        ]
        pushData(db,route,data)

# Firestore
def getData(db, route):
	docs = db.collection(route[0]).get()
	data = []
	for doc in docs:
		# print(doc.to_dict())
		data.append(doc.to_dict())
	return data

def pushData(db,route,data):
    db.collection(route[0]).document(route[1]).set(data)
    print("push berhasil")

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
	users_from_firebase = (json.loads(json.dumps(list_users_from_firebase)))
	# print(users_from_firebase)
	# users_from_firebase = []
	# for i in list_users_from_firebase.items():
		# users_from_firebase.append(i[1])
	# # print(len(users_from_firebase))
	# # users_from_firebase.remove(None)
	# # print(users_from_firebase[0]["punya_usaha"])

	df = pd.DataFrame(users_from_firebase, columns=["user_id","punya_usaha","bidang_keahlian","hobi","modal_usaha","nama_usaha"])
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
    print(row)
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

if __name__ == "__main__":
    # extract_from_csv()
    df,new_df,users = ETL()
    print(users)
    # deserved_users = get_users_who_deserved_list(users)
    # getData()