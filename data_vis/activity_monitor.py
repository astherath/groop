import tqdm
import pymongo
import pandas as pd
import matplotlib.pyplot as plt


URL = 'mongodb://localhost:27017'
client = pymongo.MongoClient(URL)
db = client.gc_data
col = db.messages



def add_all_names(names):
    dates = ['2019-01','2019-02','2019-03','2019-04']
    df_dict = {'Dates': dates, 'Names': names}
    df = pd.DataFrame(df_dict)

    #  for name in names:
        #  df.loc[name] =

    return df


if __name__ == '__main__':
    names = ['Rafa', 'Quinn', 'Matias', 'Martin', 'Liam', 'Luke', 'Cynder', 'Babak', 'Collin', 'Davo', 'Evan', 'Hannan', 'Israel', 'Jimmy', 'John', 'Felipe']

    df = add_all_names(names)

    print(df)

