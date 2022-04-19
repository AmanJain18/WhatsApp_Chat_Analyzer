import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'u_msg': messages, 'msg_dates': dates})
    df['msg_dates'] = pd.to_datetime(df['msg_dates'], format='%m/%d/%y, %I:%M %p - ').dt.strftime('%Y/%m/%d %H:%M')
    df.rename(columns={'msg_dates': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['u_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['u_msg'], inplace=True)
    df['Letter\'s'] = df['message'].apply(lambda s: len(s))
    df['Word\'s'] = df['message'].apply(lambda s: len(s.split(' ')))
    df['Date_num'] = pd.DatetimeIndex(df['date']).date
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['month'] = pd.DatetimeIndex(df['date']).month_name()
    df['month_num'] = pd.DatetimeIndex(df['date']).month
    df['day'] = pd.DatetimeIndex(df['date']).day
    df['Days'] = pd.DatetimeIndex(df['date']).day_name()
    df['hour'] = pd.DatetimeIndex(df['date']).hour
    df['minute'] = pd.DatetimeIndex(df['date']).minute

    period = []
    for hour in df[['Days', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Time - Period'] = period

    return df
