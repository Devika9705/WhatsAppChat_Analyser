

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

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



