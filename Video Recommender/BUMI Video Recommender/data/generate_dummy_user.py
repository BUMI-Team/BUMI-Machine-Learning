import random
import time
import pandas as pd
import datetime

dir = "Video Recommender/BUMI Video Recommender/data"

#Deklarasi Ketentuan Dummy Data
NUM_USER = 20
NUM_MOVIE = 1000
MIN_USER_RATING = 3                 #Berarti minimal user watch dan nge-rate sebanyak 3 video
MAX_USER_RATING = 10                #Anggapan user paling banyak melakukan rate & watch sebanyak 10x
# MAX_USER_RATING = NUM_MOVIE       #Anggapan terdapat user yang menonton semua video



def get_user_rating_attempt():
    userid_attempt =[]
    for user_id in range(1,NUM_USER+1):
        jumlah_user_rating = random.randint(MIN_USER_RATING,MAX_USER_RATING)
        # print(user_id," melakukan rate sebanyak :",jumlah_user_rating)
        userid_attempt.append(jumlah_user_rating)
    # print("sasa",len(userid_attempt))
    return userid_attempt

def generate_user_rating_timestamp(ts):
    times = ts
    time = ""
    while True:
        start_date = datetime.date(2022, 1, 1)
        end_date = datetime.date(2022, 12, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        time = datetime.datetime.strptime(str(random_date), "%Y-%m-%d").timestamp()
        if time in times:
            continue
        else:
            break
    times.append(str(int(time)))
    # print(random_date)
    # print(times)
    return times

def generate_dummy():
    random.seed(10)
    dummy = {
        "num_user": NUM_USER,
        "num_movie": NUM_MOVIE,
        "rating_attempt_of_user_id:": []
    }

    data = {
        "user_id": [],
        "video_id": [],
        "time_stamp": []
    }
    time_stamp_list = []

    # print(time.time())
    print(dummy["num_user"])
    dummy["rating_attempt_of_user_id"] =  get_user_rating_attempt()
    print("jumlah dummy seharusnya: ",sum(dummy["rating_attempt_of_user_id"]))
    print(dummy["rating_attempt_of_user_id"])
    for i in range(1,NUM_USER+1):
        # print(i)
        chosen = []
        while (dummy["rating_attempt_of_user_id"][i-1]) > 0:
            # print(dummy["rating_attempt_of_user_id"][i])      
            if len(chosen) == 0:
                dummy["rating_attempt_of_user_id"][i-1] -= 1
                video_id_chosen = random.randint(1,NUM_MOVIE)
                chosen.append(video_id_chosen)

                # dummy_rating = random.randint(1,5)
                data["user_id"].append(i)
                data["video_id"].append(video_id_chosen)
                # data["rating"].append(dummy_rating)
                time_stamp_list = generate_user_rating_timestamp(time_stamp_list)
                data["time_stamp"].append(time_stamp_list[-1])
            else:
                video_id_chosen = random.randint(1,NUM_MOVIE)
                if video_id_chosen not in chosen:
                    dummy["rating_attempt_of_user_id"][i-1] -= 1

                    # dummy_rating = float(random.randint(1,5))
                    data["user_id"].append(i)
                    data["video_id"].append(video_id_chosen)
                    # data["rating"].append(dummy_rating)
                    time_stamp_list = generate_user_rating_timestamp(time_stamp_list)
                    data["time_stamp"].append(time_stamp_list[-1])

    print("jumlah data dummmy setelah generated: ",len(data["user_id"]))

    # print(data)
    df = pd.DataFrame(data)
    # for i in df["time_stamp"][:10]:
    #     print(i)

    print(df[:100])
    print()
    output = dir+"/user_history"+str(len(data["user_id"]))+".csv"
    print(output)
    df.to_csv(output, index = False, header =False)
    print("user history csv generated!")
    pass

def main():
    generate_dummy()
    pass


if __name__ == "__main__":
    main()
