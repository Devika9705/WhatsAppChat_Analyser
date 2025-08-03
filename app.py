import streamlit as st
import matplotlib.pyplot as plt
import helper
import seaborn as sns
import preprocess
from helper import most_common_words, daily_timeline
import pandas as pd


# Hide Streamlit footer and menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Adding custom footer
st.markdown("""
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; color: gray;">
        <hr>
        <p>Developed by Devika Shukla</p>
    </div>
""", unsafe_allow_html=True)


st.set_page_config(page_title="WhatsApp Chat Analyzer")
st.sidebar.title("WhatsApp_Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox('Show analysis wrt',user_list)
if st.sidebar.button("Show Statistics"):
       num_messages,words,num_media_messages,num_links = helper.fetch_stats(selected_user,df)
       st.title("Statistics")
       col1,col2,col3,col4 = st.columns(4)

       with col1:
            st.header("Total Messages")
            st.title(num_messages)
       with col2:
           st.header("Total Words")
           st.title(words)
       with col3:
           st.header("Media Shared")
           st.title(num_media_messages)
       with col4:
           st.header("Links Shared")
           st.title(num_links)

    #monthly timeline
       st.title("Monthly timeline")
       timeline = helper.monthly_timeline(selected_user,df)
       fig,ax = plt.subplots()
       ax.plot(timeline['time'],timeline['message'],color = 'green')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
    #daily timeline
       st.title("Daily Timeline")
       timeline = helper.daily_timeline(selected_user,df)
       fig,ax = plt.subplots()
       ax.plot(timeline['only_date'],timeline['message'],color = 'blue')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
if st.sidebar.button("Activity"):
# activity map
       st.title("Activity")
       col1,col2 = st.columns(2)
       with col1:
           st.header("Most busy day")
           busy_day = helper.week_activity_map(selected_user,df)
           fig,ax=plt.subplots()
           ax.bar(busy_day.index,busy_day.values,color = 'pink')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)
       with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color = 'yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
       st.title('Weekly Activity Chart')
       user_heatmap = helper.activity_heapmap(selected_user,df)
       fig,ax=plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)


if st.sidebar.button("Busy User Analysis"):
           st.title('Most Busy Users')
           x,new_df= helper.most_busy_users(df)
           fig,ax = plt.subplots()

           col1,col2 = st.columns(2)
           with col1:
               ax.bar(x.index, x.values,color='red')
               plt.xticks(rotation = 'vertical')
               st.pyplot(fig)
           with col2:
                 st.dataframe(new_df)
if st.sidebar.button("WordCloud"):
    #WordCloud
    st.title('WordCloud')
    df_wc = helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    most_common_df = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.title("Most Common Words")
    st.pyplot(fig)
if st.sidebar.button("Emoji Analysis"):
    st.title('Emoji Analysis')

    emoji_df = helper.emoji_helper(selected_user, df)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)

    with col2:
        if not emoji_df.empty:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        else:
            st.write("No emojis found.")

if st.sidebar.button("Show Mood Analysis"):
    st.markdown("## 🧠 Mood / Sentiment Analysis")

    sentiment_result = helper.sentiment_analysis(selected_user, df)
    mood_counts = helper.extract_mood_counts(selected_user, df)

    st.markdown("### 🧡 Mood-Based Emoji Metrics")
    st.caption("This section reflects actual emoji usage from chat messages, grouped by mood.")

    # ---------- Emoji Cards Layout ----------
    mood_emojis = {
        "Love": "❤️",
        "Kissing": "😘",
        "Hug": "🫂",
        "Support": "🤗",
        "Happy": "😄",
        "Celebrate": "🎉",
        "Angry": "🤬",
        "Sad": "😢",
        "Disappointed": "🙁",
    }

    moods = list(mood_emojis.keys())
    cols = st.columns(3)
    for idx, mood in enumerate(moods):
        emoji_icon = mood_emojis[mood]
        with cols[idx % 3]:
            st.metric(label=f"{emoji_icon} {mood}", value=mood_counts.get(mood, 0))

    st.markdown("---")

    # ---------- Mood Distribution Pie Chart ----------
    st.markdown("### 🥧 Mood Distribution")

    pie_labels = [f"{mood_emojis[mood]} {mood}" for mood in mood_counts.keys()]
    pie_values = [mood_counts[mood] for mood in mood_counts.keys()]
    pie_colors = sns.color_palette("pastel")[0:len(pie_labels)]

    fig1, ax1 = plt.subplots()
    ax1.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=pie_colors, textprops={'fontsize': 9})
    ax1.axis('equal')
    st.pyplot(fig1)

    # ----------  Horizontal Bar Chart ----------
    st.markdown("### 📊 Mood Usage Comparison")

    sorted_mood_df = pd.DataFrame({
        "Mood": [f"{mood_emojis[mood]} {mood}" for mood in mood_counts.keys()],
        "Count": [mood_counts[mood] for mood in mood_counts.keys()]
    }).sort_values(by="Count", ascending=True)

    fig2, ax2 = plt.subplots()
    sns.barplot(x="Count", y="Mood", data=sorted_mood_df, palette="Set2", ax=ax2)
    ax2.set_xlabel("Emoji Usage Count")
    ax2.set_ylabel("Mood")
    st.pyplot(fig2)
