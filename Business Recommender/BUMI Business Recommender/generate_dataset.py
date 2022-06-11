from json.tool import main
from operator import index
import random
import pandas
import csv
from IPython.display import display
import json

metadata_file       = 'Business Recommender/BUMI Business Recommender/synthetic_metadata.json'
output_file         = "Business Recommender/BUMI Business Recommender/user_input.csv"


def get_dataframe_metadata(name_file):
    with open(name_file) as f:
        data = json.load(f, strict=False)
    return data

def generate_dummy(proporsi):
    """
    Generate dummy data from metadata file atribute
    """
    metadata                = get_dataframe_metadata(metadata_file)
    
    num_user_dummy          = metadata["num_user_dummy"]
    df_column               = metadata["tags"]["column_name"]
    list_status             = metadata["tags"]["punya_usaha"]
    list_bidang_keahlian    = metadata["tags"]["bidang_keahlian"]
    list_hobi               = metadata["tags"]["hobi"]
    list_modal_usaha        = metadata["tags"]["modal_usaha"]
    
    df = pandas.DataFrame(columns=df_column)
    count = 0
    
    for i in range(1,num_user_dummy+1):
        user_id = i
        if count < proporsi/100*num_user_dummy:
            punya_usaha= list_status[0]
            nama_usaha = "nama_usaha-"+str(user_id)
        else:
            punya_usaha= list_status[1]
            nama_usaha = "UNK"
        

        #Pilihan diacak kembali sesuai dengan ketentuan jumlah pilihan
        
        jumlah_milih_maks_3 = random.randint(1,3)
        jumlah_milih_maks_5 = random.randint(1,5)
        
        bidang_keahlian = random.sample(list_bidang_keahlian, jumlah_milih_maks_3)
        hobi            = random.sample(list_hobi, jumlah_milih_maks_5)
        modal_usaha     = random.choice(list_modal_usaha)

        df.loc[i] = [user_id,punya_usaha,bidang_keahlian,hobi,modal_usaha,nama_usaha]
        count += 1
    df.to_csv(output_file, index = False)
    
    print(len(df))
    print(df)


def main():
    generate_dummy(proporsi = 40) #persentase yg udah punya usaha


if __name__ == "__main__":
    main()