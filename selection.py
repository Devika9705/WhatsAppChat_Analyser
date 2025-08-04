# selection.py

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import helper
import plotly.express as px


def show_mood_analysis(df, selected_user):
    st.markdown("## 🧠 Mood / Sentiment Analysis", unsafe_allow_html=True)

    sentiment_result = helper.sentiment_analysis(selected_user, df)
    mood_counts = helper.extract_mood_counts(selected_user, df)

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
    with st.expander("💖 Mood Emoji Counters", expanded=True):
        cols = st.columns(3)
        for idx, mood in enumerate(moods):
            emoji_icon = mood_emojis[mood]
            with cols[idx % 3]:
                st.metric(label=f"{emoji_icon} {mood}", value=mood_counts.get(mood, 0))

    with st.expander("🌸 Mood Distribution", expanded=True):
        pie_labels = [f"{mood_emojis[mood]} {mood}" for mood in mood_counts.keys()]
        pie_values = [mood_counts[mood] for mood in mood_counts.keys()]
        fig = px.pie(
            names=pie_labels,
            values=pie_values,
            title="Mood Proportions",
            color_discrete_sequence=px.colors.sequential.Plasma_r
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 Mood Comparison", expanded=True):
        sorted_mood_df = pd.DataFrame({
            "Mood": [f"{mood_emojis[mood]} {mood}" for mood in mood_counts.keys()],
            "Count": [mood_counts[mood] for mood in mood_counts.keys()]
        }).sort_values(by="Count", ascending=True)

        fig2 = px.bar(
            sorted_mood_df,
            x="Count",
            y="Mood",
            orientation='h',
            color="Mood",
            title="Mood Frequency",
            color_discrete_sequence=px.colors.sequential.Agsunset
        )
        st.plotly_chart(fig2, use_container_width=True)


def show_ai_advice(df, selected_user):
    st.markdown("### 🤖 AI Mood Advice", unsafe_allow_html=True)
    if selected_user != "Overall" and st.button("Get AI Mood & Advice"):
        messages = df[df['user'] == selected_user]['message'].tolist()
        combined = "\n".join(messages[:200])
        with st.spinner("Analyzing with AI..."):
            result = helper.get_conversation_advice(selected_user, combined)
        st.success(f"AI Mood & Talk Advice for {selected_user}")
        st.write(result)


def show_stats(df, selected_user):
    st.markdown("## 📊 Chat Statistics", unsafe_allow_html=True)
    num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)

    with st.expander("📈 Overview", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Messages", num_messages)
        col2.metric("Words", words)
        col3.metric("Media Shared", num_media)
        col4.metric("Links Shared", num_links)

    with st.expander("📅 Monthly Timeline", expanded=True):
        timeline = helper.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Message Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📆 Daily Timeline", expanded=True):
        timeline = helper.daily_timeline(selected_user, df)
        fig = px.line(timeline, x='only_date', y='message', title='Daily Message Count', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Activity Map", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            busy_day = helper.week_activity_map(selected_user, df)
            fig = px.bar(x=busy_day.index, y=busy_day.values, labels={'x': 'Day', 'y': 'Messages'},
                         title='Most Active Days', color_discrete_sequence=['#FF69B4'])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            busy_month = helper.month_activity_map(selected_user, df)
            fig = px.bar(x=busy_month.index, y=busy_month.values, labels={'x': 'Month', 'y': 'Messages'},
                         title='Most Active Months', color_discrete_sequence=['#FFD700'])
            st.plotly_chart(fig, use_container_width=True)

        heatmap = helper.activity_heapmap(selected_user, df)
        st.write("### 🗓️ Weekly Heatmap")
        fig, ax = plt.subplots()
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)


def show_wordcloud(df, selected_user):
    st.markdown("## ☁️ Word Cloud", unsafe_allow_html=True)
    df_wc = helper.create_wordcloud(selected_user, df)
    with st.expander("Word Cloud", expanded=True):
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

    with st.expander("Most Common Words", expanded=True):
        most_common_df = helper.most_common_words(selected_user, df)
        fig2 = px.bar(most_common_df, x=1, y=0, orientation='h',
                     labels={"0": "Word", "1": "Count"},
                     title="Top Used Words",
                     color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig2, use_container_width=True)


def show_emoji_analysis(df, selected_user):
    st.markdown("## 😀 Emoji Analysis", unsafe_allow_html=True)
    emoji_df = helper.emoji_helper(selected_user, df)

    with st.expander("Emoji Usage Table", expanded=True):
        st.dataframe(emoji_df)

    if not emoji_df.empty:
        with st.expander("Emoji Pie Chart", expanded=True):
            fig = px.pie(emoji_df.head(), names=0, values=1, title="Top Emojis Used",
                         color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No emojis found in selected chat.")