import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from utils.Mongo import db_data
from utils.analysis import create_plots, nlp_plots
from utils.nlp_tech import nlp_analysis
import nltk

st.set_option('client.showErrorDetails', False)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")
@st.cache(allow_output_mutation=True)
def get_mongo_client():
    user_name = "onlinefeedback_gent"
    password = "Qu10mxMGOsFx4lHb"
    uri = f"mongodb+srv://{user_name}:{password}@cluster0.sry1dls.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    return client

client = get_mongo_client()

collection = client['Feedback']['Gent']
data = db_data(collection)
museum = data[data['section']=='Gravensteen'][['section','how_hear','motivation','score','idea','time']]
park = data[data['section']=='Citadelpark'][['section','how_often','activity','score','idea','time']]


st.header("Analysis Dashboard")
sector = st.radio('which place do you want to see its analysis?',options=['Minnewater Park', 'Groeninge Museum'])
st.title(sector)
if sector == 'Groeninge Museum':
    create_plots(df=museum,var='how_hear',section=sector)
    df_museum, wordcloud_museum = nlp_analysis(df=museum)
    st.title('Natural Language Processing')
    nlp_plots(wordcloud_museum, df_museum)
elif sector == 'Minnewater Park':
    create_plots(df=park,var='how_often',section=sector)
    df_park, wordcloud_park = nlp_analysis(df=park)
    st.title('Natural Language Processing')
    nlp_plots(wordcloud_park, df_park)

