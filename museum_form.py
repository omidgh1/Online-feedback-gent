import streamlit as st
import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils.Mongo import db_update, db_data
from utils.form_analysis import analysis_radio

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

museum = data[data['section']=='Gravensteen'][['section','how_hear','motivation','score','idea','time']]

st.header("Submit Form Data")
st.title("Gravensteen")
st.image('Gravensteen.jpg')
how_hear = st.radio('How did you hear about Gravensteen?',
                    options=['Online advertisement','Social media', 'Word of mouth', 'Local events'])
motivation = st.radio('What motivated you to visit',
                      options=['Interest in the specific exhibits', 'Recommendation from friends or family',
                               'Curiosity about the museum itself', 'Research or academic purposes'])
score = st.radio('How satisfied were you with the ticketing process',
                 options=['1 (Poor)', '2 (Fair)', '3 (Average)', '4 (Good)', '5 (Excellent)'])
idea = st.text_input('Write your suggestion to improve the quality', max_chars=100)

if st.button("Submit"):
    data = {'section': 'Gravensteen', 'how_hear': how_hear, 'motivation': motivation, 'score': score, 'idea': idea,
            'time': datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
    db_update(collection,data)
    st.success("Form submitted successfully!")
    how_hear_result = analysis_radio(museum, 'how_hear', 'Gravensteen', how_hear)
    motivation_result = analysis_radio(museum, 'motivation', 'Gravensteen', motivation)
    st.markdown(how_hear_result)
    st.markdown(motivation_result)

