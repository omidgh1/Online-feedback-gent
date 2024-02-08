import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def percentage_radio(df,var,chosen):
    try:
        return round((int(df[var].value_counts()[chosen])/int(df[var].value_counts().sum()))*100,2)
    except:
        return round((int(1)/int(df[var].value_counts().sum()))*100,2)

def analysis_radio(df,var,section,chosen):
    h_often_percent = percentage_radio(df, var, chosen)
    text = f"{chosen} has been chosen by {str(h_often_percent)}% of people about the {section} like you."
    return text

def count_plot(df,var,section):
    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x=var, palette='pastel', hue=var)
    plt.title(f'Frequency of Visiting {section}', fontsize=16)
    plt.xlabel(var, fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    st.pyplot()

# Plot 2: Bar Plot of 'score'
def bar_plot_score(df,section):
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='score', y=df.index, palette='pastel', hue='score')
    plt.title(f'Scores for {section}', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Index', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    st.pyplot()

# Plot 3: Pie Chart of 'activity'
def pie_chart_act(df,var,section):
    plt.figure(figsize=(8, 6))
    activity_counts = df[var].explode().value_counts()
    plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'), textprops={'fontsize': 12})
    plt.title(f'Activity Distribution in {section}', fontsize=16)
    st.pyplot()

def time_plot(df,section):
    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])
    for i in df.index:
        df.loc[i, 'new_score'] = int(df.loc[i, 'score'].split(' ')[0])
    grouped_data = df.groupby(df['time'].dt.date)['new_score'].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=grouped_data, marker='o', linewidth=2.5)
    plt.title(f'Time Series of Average Scores for {section}', fontsize=18, fontweight='bold', color='black')
    plt.xlabel('Date', fontsize=14, fontweight='bold', color='black')
    plt.ylabel('Average Score', fontsize=14, fontweight='bold', color='black')
    plt.xticks(fontsize=12, color='black')
    plt.yticks(fontsize=12, color='black')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.gca().patch.set_facecolor('#f0f0f0')  # Set background color
    plt.gca().patch.set_alpha(0.7)  # Set background transparency
    plt.tight_layout()
    st.pyplot()

def create_plots(df,var,section):
    col1, col2 = st.columns(2)

# Plot 1: Count Plot of 'how_often'
    with col1:
        count_plot(df, var, section)

# Plot 2: Bar Plot of 'score'
    with col2:
        bar_plot_score(df, section)

    # Plot 3: Pie Chart of 'activity'
    with col1:
        pie_chart_act(df, var, section)

    # Plot 4: Time Series Plot
    with col2:
        time_plot(df, section)

def nlp_plots(wordcloud,df):
    col1, col2 = st.columns(2)
    with col1:
        col1.header('the Most written words')
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()
    with col2:
        sentiment_counts = df['sentiment_label'].value_counts()
        col2.header('Sentiment Analysis')
        plt.figure(figsize=(8, 5))
        sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment Label')
        plt.ylabel('Frequency')
        plt.xticks(rotation=0)
        st.pyplot()
