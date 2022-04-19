import streamlit as st
import preprocessor
import modify
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title('Top Statistics')
        if selected_user == 'Overall':
            tol_users = modify.total_users(df)
            st.header("Total Users in Groups: " + str(tol_users))

        tol_messages, words, media_msg, tol_links = modify.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(tol_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(media_msg)

        with col4:
            st.header("Total Links Shared")
            st.title(tol_links)

        # Monthly_TimeLine
        st.title("Monthly Timeline")
        timeline = modify.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='#6dc2ae')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily_Timeline
        st.title("Daily Timeline")
        daily_timelines = modify.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timelines['Date_num'], daily_timelines['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = modify.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#c97c65')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy month")
            busy_month = modify.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#98bf62')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = modify.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Active Users')
            x, new_df = modify.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#575FE8')
                plt.xticks(rotation='vertical')
                plt.xlabel('Users')
                plt.ylabel('No. of messages')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        if selected_user == 'Overall':
            st.title('Top-10 media contributor of Group')
            x, new_df = modify.most_media_contributor(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='#79a832')
                plt.xticks(rotation='vertical')
                plt.xlabel('Users')
                plt.ylabel('No. of media')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title('WordCloud')
        df_wc = modify.create_word(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most Common Words

        mcw_df = modify.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(mcw_df[0], mcw_df[1], color='#C9EAB8')
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        wpm = modify.words_per_message(selected_user, df)
        st.title('Average Words per Message')
        st.header(wpm)

        emoji_df = modify.all_emoji(selected_user, df)
        st.title("Emoji's Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
