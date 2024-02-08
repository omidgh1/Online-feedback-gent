import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi

user_name = "onlinefeedback_gent"
password = "Qu10mxMGOsFx4lHb"

def mongo_client(user_name,password):
    uri = f"mongodb+srv://{user_name}:{password}@cluster0.sry1dls.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['Feedback']
    collection = db['Gent']
    return collection

def db_update(collection,data):
    collection.insert_one(data)

def db_data(collection):
    dataset = pd.DataFrame(list(collection.find({})))
    return dataset


#data = {'section': 'Citadelpark', 'how_often': 'Daily', 'activity': 'Boating', 'score': '5 (Excellent)', 'idea': 'the lake is very beautiful',
#            'time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
#db_update(data)

