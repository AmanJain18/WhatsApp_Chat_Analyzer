from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import emoji
import numpy as np

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    tol_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return  tol_messages, len(words), media_msg, len(links)


def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Contribution %'})
    return x, df


def total_users(df):
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    return len(user_list)


def most_media_contributor(df):
    mm = df[df['message'] == '<Media omitted>\n']
    mm1 = mm['user'].value_counts().head(10)
    df = round((mm['user'].value_counts().head(10) / mm.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Media Contribution %'})
    return mm1, df


def create_word(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_sw(message):
        rm = []
        for word in message.lower().split():
            if word not in stop_words:
                rm.append(word)
        return " ".join(rm)

    wc = WordCloud(
        background_color='white',
        height=400,
        width=400,
        min_word_length=8,
        stopwords=STOPWORDS
    )

    temp['message'] = temp['message'].apply(remove_sw)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    mcw = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                mcw.append(word)

    mcw_return = pd.DataFrame(Counter(mcw).most_common(25))

    return mcw_return


def all_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def words_per_message(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wpm = (np.sum(df['Word\'s']))/df.shape[0]
    w_p_m = ("%.3f" % round(wpm, 2))

    return w_p_m


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timelines = df.groupby('Date_num').count()['message'].reset_index()

    return daily_timelines


def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['Days'].value_counts()


def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='Days', columns='Time - Period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
