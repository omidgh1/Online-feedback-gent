import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from collections import Counter

def nlp_analysis(df):
    # Tokenization and Stopwords Removal
    stop_words = set(stopwords.words('english'))
    df['tokenized_text'] = df['idea'].apply(lambda x: word_tokenize(x.lower()))
    df['tokenized_text'] = df['tokenized_text'].apply(lambda x: [word for word in x if word.isalnum() and word not in stop_words])

    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['idea'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df['sentiment_label'] = df['sentiment_score'].apply(lambda score: 'positive' if score > 0 else ('negative' if score < 0 else 'neutral'))

    # Word Cloud
    word_counts = Counter(word for tokens in df['tokenized_text'] for word in tokens)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    return df, wordcloud
