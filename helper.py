from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob

extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    num_messages = df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())
    num_media_messages = df[df['message'] == '<Media omitted>/n'].shape[0]
    links = []
    for message in df['message']:
        links.extend((extract.find_urls(message)))

    return num_messages,len(words),num_media_messages,len(links)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    wc = WordCloud(width=500,height =500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    f = open('stop_hinglish_words.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline
def daily_timeline(selected_user, df):
    # Filter by user if not overall
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Group by date and count messages
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heapmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    activity = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity

# Define emoji to mood category mapping
mood_map = {
    "❤️": "Love",
    "💖": "Love",
    "😘": "Kissing",
    "🤬": "Angry",
    "😢": "Sad",
    "🙁": "Disappointed",
    "😄": "Happy",
    "🎉": "Celebrate",
    "🤗": "Support",
    "🫂": "Hug",
}

def extract_mood_counts(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    mood_counter = Counter()

    for message in df['message']:
        for char in message:
            if emoji.is_emoji(char) and char in mood_map:
                mood_counter[mood_map[char]] += 1

    return mood_counter

def sentiment_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    sentiments = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    for message in df['message']:
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiments['Positive'] += 1
        elif polarity == 0:
            sentiments['Neutral'] += 1
        else:
            sentiments['Negative'] += 1

    return sentiments


import requests


def get_conversation_advice(name, messages):
    prompt = f"""
    Below are WhatsApp messages from {name}. Analyze their mood, tone, and talk style.
    Then suggest how to communicate better with this person.

    Messages:
    {messages[:2000]}
    """

    headers = {
        "Authorization": "Bearer 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",  # Put your OpenRouter key here
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    try:
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        print("❌ Error:", e)
        print("❌ Response JSON:", response.text)
        return "⚠️ Sorry, AI advice could not be generated. Please check your API key or try again later."
