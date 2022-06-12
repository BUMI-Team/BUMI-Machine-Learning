import pyrebase
import pandas as pd
import json


NUM_USER = 10
data_dir = "API/BUMI_users_data.csv"
metadata_file = 'Business Recommender/BUMI Business Recommender/synthetic_metadata.json'

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


def initMetaData():
    metadata = get_dataframe_metadata(metadata_file)
    print(metadata)
    route=[
        "metadata"
    ]
    pushData(db,route,metadata)
    updateData(db,route,{"num_user_dummy":NUM_USER})
    pass

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

        # print(modal_usaha)
    # pass

def get_dataframe_metadata(name_file):
    with open(name_file) as f:
        data = json.load(f, strict=False)
    return data

def pushData(db,route,data):
    # db.push(data)
    for r in route:
        db.child(r)
    db.set(data)
    print("push berhasil")

def getData(db,route):
    for r in route:
        db.child(r)
    data = db.get()
    # print(data.val())
    return data.val()

def updateData(db,route,dataUpdate):
    for r in route:
        db.child(r).update(dataUpdate)
    print("Data terupdate")

def deleteData(db,route):
    for r in route:
        db.child(r)
    db.remove()
    print("Data terhapus")

def runFireBase():

    #Push Data
    route =[
        "users",
        "firstPerson"
    ]
    # pushData(db, root, data)
    # getData(db)
    # updateData(db)
    # deleteData(db)

def main():
    # route = ["users"]
    # deleteData(db,route)
    initMetaData()
    extract_from_csv()
    # runFireBase()

    # users = []
    # route =[
    #     "users"
    # ]   
    # users = getData(db,route)
    # users.remove(None)
    # print(users[0]["punya_usaha"])

    # df = pd.DataFrame(users)
    # print(df)




    
    pass

if __name__ == "__main__":
    main()
    # print("hallo")
