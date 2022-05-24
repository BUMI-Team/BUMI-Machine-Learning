import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds

def ETL(csv_name):    
    df = pd.read_csv(csv_name)
    feature = df[["videoId","viewCount","likeCount","commentCount"]]

    print(normalizer(numeric_features.iloc[:3]))
    print(numeric_features.head())
    
def main():
    datas = ETL("Machine Learning/umkm.csv")
    # print((datas.keys()))
    pass

if __name__ == '__main__':
    main()
    