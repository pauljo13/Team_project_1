import pandas as pd
import numpy as np

# 체크인 날짜 형식이 조금 달라 파일 7,8과 9를 따로 준비한다.

def prepare_7_8(file_csv):

    file_csv = file_csv.drop(['check_out_day','check_out_week'], axis=1)
    file_csv['distance(km)'] = ''
    columns = ['Name', 'location', 'distance(km)', 'location_score', 'check_in_day', 'check_in_week', 'score', 'price']
    file_csv = file_csv[columns]

    # 체크인 날짜
    check_in_day = []
    for i in range(len(file_csv['check_in_day'])):
        if len(file_csv['check_in_day'][i][6:]) == 5:
            year = int(file_csv['check_in_day'][i][:4])
            month = int(file_csv['check_in_day'][i][6])
            day = int(file_csv['check_in_day'][i][9])
        else:
            year = int(file_csv['check_in_day'][i][:4])
            month = int(file_csv['check_in_day'][i][6])
            day = int(file_csv['check_in_day'][i][9:11])

        check_in_day.append(f"{year:04}-{month:02}-{day:02}")

    file_csv['check_in_day'] = check_in_day

    # 체크인 요일
    check_in_week = []
    for i in range(len(file_csv['check_in_week'])):
        check_in_week.append(file_csv.iloc[i]['check_in_week'][0])

    file_csv['check_in_week'] = check_in_week
    
    return file_csv


def prepare_9(file_csv):
    file_csv.rename(columns = {'호텔 이름':'Name', '위치':'location', '가격':'price', '평점':'score'}, inplace=True)
    file_csv = file_csv.drop(['check_out_day','check_out_week'], axis=1)
    file_csv['location_score'] = 9
    file_csv['distance(km)'] = ''
    columns = ['Name', 'location', 'distance(km)', 'location_score', 'check_in_day', 'check_in_week', 'score', 'price']
    file_csv = file_csv[columns]

    # 체크인 날짜
    check_in_day = []
    for i in range(len(file_csv['check_in_day'])):
        if len(file_csv['check_in_day'][i][6:]) == 5:
            year = int(file_csv['check_in_day'][i][:4])
            month = int(file_csv['check_in_day'][i][7])
            day = int(file_csv['check_in_day'][i][-2])
        else:
            year = int(file_csv['check_in_day'][i][:4])
            month = int(file_csv['check_in_day'][i][7])
            day = int(file_csv['check_in_day'][i][10:12])

        check_in_day.append(f"{year:04}-{month:02}-{day:02}")

    file_csv['check_in_day'] = check_in_day

    # 체크인 요일
    check_in_week = []
    for i in range(len(file_csv['check_in_week'])):
        check_in_week.append(file_csv.iloc[i]['check_in_week'][0])

    file_csv['check_in_week'] = check_in_week

    return file_csv


def clean(file_csv, file_name):

    # location 항목에서 거리 데이터 분리
    location = []
    distance = []

    for i in range(len(file_csv['location'])):
        loc = file_csv['location'][i].split('-')
        if len(loc) < 2:
            location.append(loc[0])
            distance.append('')
        else:
            location.append(loc[0])
            distance.append(loc[1])

    file_csv['location'] = location
    file_csv['distance(km)'] = distance

    # distance(km)항목 정리
    distance_km = []
    for i in range(len(file_csv['distance(km)'])):
        if file_csv['distance(km)'][i].startswith(' 도심까지'):
            if file_csv['distance(km)'][i][-2].isdigit():
                distance_km.append(round(int(file_csv['distance(km)'][i][6:-1])*0.001,2))
            else:
                distance_km.append(float(file_csv['distance(km)'][i][6:-2]))
        elif file_csv['distance(km)'][i].startswith(' 도심에'):
            distance_km.append(0)
        else:
            distance_km.append(np.nan)

    file_csv['distance(km)'] = distance_km

    # location 항목 정리(로스앤젤레스(CA) 텍스트 제거)
    new_loc = []
    for i in range(len(file_csv['location'])):
        new_loc.append(file_csv['location'][i].split(',')[0])

    file_csv['location'] = new_loc

    # 중복 제거
    file_csv = file_csv.drop_duplicates().reset_index(drop=True)

        # nan값 location별 평균 값으로 채워주기
    empty_idx = file_csv[file_csv['distance(km)'].isnull()].index.values.tolist()
    empty_loc = set(file_csv[file_csv['distance(km)'].isnull()]['location'])
    full = file_csv.drop(empty_idx)

        # 평균 값 구하기
    loc_avg = {}
    for i in empty_loc:
        avg = round(full[full['location'] == i]['distance(km)'].sum() / len(full[full['location'] == i]),1)
        loc_avg[i] = avg

        # 구한 평균 넣어주기
    distance_km = []
    for i in range(len(file_csv)):
        if file_csv['distance(km)'][i] >= 0:
            distance_km.append(file_csv['distance(km)'][i])
        else:
            distance_km.append(loc_avg[file_csv.iloc[i]['location']])

    file_csv['distance(km)'] = distance_km

    # 항목별 타입 변경
    file_csv['check_in_day'] = pd.to_datetime(file_csv['check_in_day'])
    file_csv['score'] = file_csv['score'].astype(float)
    file_csv['price'] = file_csv['price'].replace(',', '', regex=True)
    file_csv['price'] = file_csv['price'].astype(int)
    file_csv['distance(km)'] = file_csv['distance(km)'].astype(float)

    # 파일 저장
    file_csv.to_csv(file_name, index=False)



df_7 = pd.read_csv("agoda_hotels_7.csv")
df_8 = pd.read_csv("agoda_hotels_8.csv")
df_9 = pd.read_csv("agoda_hotels_9.csv", encoding='cp949')

prepared_7 = prepare_7_8(df_7)
prepared_8 = prepare_7_8(df_8)
prepared_9 = prepare_9(df_9)

clean(prepared_7, 'hotels_7.csv')
clean(prepared_8, 'hotels_8.csv')
clean(prepared_9, 'hotels_9.csv')