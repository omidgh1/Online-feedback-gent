import streamlit as st
import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils.Mongo import db_update, db_data
from utils.analysis import analysis_radio

st.set_option('client.showErrorDetails', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
@st.cache(allow_output_mutation=True)
def get_mongo_client():
    user_name = "onlinefeedback_gent"
    password = "Qu10mxMGOsFx4lHb"
    uri = f"mongodb+srv://{user_name}:{password}@cluster0.sry1dls.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    return client

client = get_mongo_client()

collection = client['Feedback']['Gent']
data = db_data(collection)

park = data[data['section']=='Citadelpark'][['section','how_often','activity','score','idea','time']]

st.header("Submit Form Data")
st.title("Minnewater Park")
st.image('Minnewater Park.jpg')
how_often = st.radio('How often do you visit Minnewater Park?',
                     options=['Daily', 'Weekly','Monthly', 'Rarely','Never visited'])
score = st.radio('On a scale of 1 to 5, how would you rate the cleanliness of Minnewater Park?',
                     options=['1 (Poor)', '2 (Fair)', '3 (Average)', '4 (Good)', '5 (Excellent)'])
activity = st.radio('What activities do you typically engage in while at Minnewater Park? (Check all that apply)',
                     options=['Walking/Jogging', 'Picnicking', 'Boating', 'Birdwatching', 'Photography',
                              'Attending events/festivals'])
idea = st.text_input('Write your suggestion to improve the quality', max_chars=100)

if st.button("Submit"):
    data = {'section': 'Minnewater Park', 'how_often': how_often, 'activity': activity, 'score': score, 'idea': idea,
            'time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
    db_update(collection,data)
    st.success("Form submitted successfully!")
    how_often_result = analysis_radio(park, 'how_often', 'Minnewater Park', how_often)
    activity_result = analysis_radio(park, 'activity', 'Minnewater Park', activity)
    st.markdown(how_often_result)
    st.markdown(activity_result)


