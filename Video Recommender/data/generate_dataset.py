from email.policy import strict
import json
import pandas as pd
import numpy as np

metadata_file = "Video Recommender\data\synthetic_metadata.json"

def get_dataframe_metadata(name_file):
    with open(name_file) as f:
        data = json.load(f)
    # print(data["movies_column"])
    # print(data["ratings_column"])
    # print(data["num_user_dummy"])
    return data

def ETL():
    metadata    = get_dataframe_metadata(metadata_file)
    num_user_dummy          = metadata["num_user_dummy"]
    # print(num_user_dummy)
    num_dummy = metadata["num_user_dummy"]
    movies_column = metadata["movies_column"]
    ratings_column = metadata["ratings_column"]

 


def main():
    ETL()
    # pass

if __name__ == "__main__":
    main()