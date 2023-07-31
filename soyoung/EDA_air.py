import pandas as pd
import numpy as np
import re
import datetime as datetime

# df = pd.read_csv('KRtoLA copy.csv')
# df1 = pd.read_csv('LAtoKR.csv')

# 컬럼 이름 통일
df = df[['departuredate', 'departureday', 'departuretime', 'class', 'arrivaldate', 'arrivalday', 'arrivaltime', 'flighttime', 'flighttype', 'price', 'airlines', 'portd', 'porta']]
df

# 날짜 형식 변경
df['departuredate'] = df['departuredate'].str.strip()
df['arrivaldate'] = df['arrivaldate'].str.strip()
df[['departuredate', 'arrivaldate']]

df['departuredate'] = pd.to_datetime(df['departuredate'], format='%m월 %d일')
df['departuredate'].apply(lambda x: x.strftime('%m-%d'))
df['arrivaldate'] = pd.to_datetime(df['arrivaldate'], format='%m월 %d일')
df['arrivaldate'].apply(lambda x: x.strftime('%m-%d'))
df['departuredate'] = df['departuredate'].apply(lambda x: x[-5:])
df['arrivaldate'] = df['arrivaldate'].apply(lambda x: x[-5:])

# 날짜 형식 통일
df['departureday']

# df.to_csv("KRtoLA.csv", index=False)
import re
df['arrivalday'] = df['arrivalday'].str.extract(r'\((.*?)\)')
df['arrivalday']

# 시간 형식 통일
df['departuretime']
def format_departuretime(time_str):
    time_period, time = time_str.split()
    hour, minute = time.split(':')
    hour = hour.zfill(2)
    return f"{time_period} {hour}:{minute}"
df['departuretime'] = df['departuretime'].apply(format_departuretime)
df['arrivaltime'] = df['arrivaltime'].apply(format_departuretime)
df[['departuretime', 'arrivaltime']]

# 경유/직항 형식 변경
df['flighttype'] = df['flighttype'].replace({'직항': 0, '경유 1회': 1, '경유 2회': 2, '경유 3회': 3, '경유 4회': 4, '경유 5회': 5})
df['flighttype']

# 가격 형식 변경
df['price'] = df['price'].str.split('₩').str[-1]

# 항공사 형식 통일
df['airlines']

# df.to_csv("KRtoLA.csv", index=False)
# # pd.read_csv('KRtoLA.csv')