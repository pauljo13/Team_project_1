import streamlit as st
import requests
import numpy as np 
import pandas as pd 
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import *
# from category_encoders import OrdinalEncoder
# from sklearn.pipeline import make_pipeline
# from sklearn.metrics import r2_score, mean_absolute_error
# from xgboost import XGBRegressor
import pickle
import random
# import shap
# from pdpbox.pdp import pdp_isolate, pdp_plot
import datetime
from datetime import datetime, timedelta
import sqlite3
# Metabase 설정
METABASE_URL = "https://teami5.metabaseapp.com/public/dashboard/20c55ded-717f-4edd-ad63-89af2654c8da"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('db/sqlite_db.db')  # 데이터베이스 파일 경로를 입력
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

    
def Flight_Time(Departure_or_entry,Class,Flight_type):
    # 비행 시간표
    departure = pd.DataFrame({'비즈니스': [11.335042016806725, 22.935111930471425, 25.619097639981486, 28.99587301587302, 51.64812499999999], 
             '이코노미': [11.215637583892619, 23.28843523073319, 25.919412673879446, 26.798203497615262, 51.6],
             '프리미엄 이코노미': [11.302, 23.054464520367937, 26.041043719989894, 26.864802784222736, 51], 
             '퍼스트': [11.169999999999995, 19.993137996219282, 24.588079999999998, 29.370550660792954, 51]}).round(2)
    entry = pd.DataFrame({'비즈니스': [13.326504065040652, 25.909293025470127, 28.1739769065521, 36.17582456140351, 54.69217391304348], 
         '이코노미': [13.261862068965517, 25.64626043841336, 28.733799201369084, 29.991457399103137, 56], 
         '프리미엄 이코노미': [13.166, 25.593388288800455, 28.34211437170805, 33.18008445945946, 81.385], 
         '퍼스트': [13.33435483870968, 24.71732824427481, 28.076642066420664, 31.87838331160365, 88.10833333333333]}).round(2)
    # 비행 시간 출력
    if Departure_or_entry == '출국':
        return departure[Class][Flight_type]
    elif Departure_or_entry == '귀국':
        return entry[Class][Flight_type]

def Date_data(Date):
    dt = datetime(Date)
    day = dt.day
    # 월:0,화:1,수:2,목:3,금:4,토:5,일:6 /->전환/ '토':2, '금':1, '화':5, '수':6, '일':3, '월':4, '목':7
    week_list = {'0':'월','1':'화','2':'수','3':'목','4':'금','5':'토','6':'일'}
    week_code = {'토':2, '금':1, '화':5, '수':6, '일':3, '월':4, '목':7}
    wc = week_list[str(dt.weekday())]
    week = week_code[wc]
    hour = dt.hour
    return day, week, hour

def Make_DataFrame(Departure_or_entry,Date):
    day, week, hour = Date_data(Date)
    Flight_time_hour = Flight_Time(Departure_or_entry,Class,Flight_type)
    return pd.DataFrame({'class': Class, 
                         'port_a': Port_a, 
                         'interior_airlines': Interior_airlines, 
                         'flight_type': Flight_type,
                         'flight_time_hour': Flight_time_hour, 
                         'port_d': Port_d,
                         'departure_hour': hour, 
                         'departure_date_day': day, 
                         'departure_day': week})

def main():
    # 사이드바 스타일을 적용하기 위한 CSS 스타일
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-item {
            font-size: 20px;
            color: #007bff;
            padding: 10px;
            margin: 5px 0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .sidebar .sidebar-item:hover {
            background-color: #007bff;
            color: white;
        }
        .special-word {
                color: blue;
                font-weight: bold;
            }
        .warning-text {
                color: red;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    page_style = """
    <style>
        /* 타이틀을 상단 중앙에 정렬하는 스타일 */
        .title {
            text-align: center;
            margin-top: 20px;
            color: black;
            font-size: 40px;
        }
        /* 페이지 배경 이미지를 지정하는 스타일 */
        body {
            background-image: '/img/undraw_background.png';
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }
        .iframe-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 800px;
        }
        .iframe {
            width: 1300px;
            height: 800px;
            border: none;
        }
    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)

    # 타이틀 표시
    st.markdown("<h1 class='title'>Travel Cost Hunter</h1>", unsafe_allow_html=True)


    # 사이드바에서 페이지 선택
    
    selected_page = st.sidebar.selectbox("Menu", ["Home", "Travel Cost Prediction", "DashBoard"])

    depart_cost=0
    return_cost=0
    accom_cost=0

    # 각 페이지의 내용을 표시
    if selected_page == "Home":

        """


        Travel Cost Hunter에 오신 것을 환영합니다 !

        Travel Cost Hunter는 사용자가 가고자 하는 여행지와 관련된 여행 경비를 쉽고 간단하게 알아볼 수 있는 서비스를 제공합니다.

        현재 Travel Cost Hunter 서비스 범위는 2023년 9월 한국에서 미국으로의 여행 경비로, 해당 항공권과 숙박권 데이터를 기준으로 서비스를 제공합니다.


        """
        st.write("여행 경비를 간단하게 예측하고 싶다면 사이드 메뉴를 통해 <span class='special-word'>Travel Cost Prediction</span> 페이지로 이동하세요!", unsafe_allow_html=True)
        st.write("항공권, 숙박권 등에 대한 여행 경비 데이터들을 직접 확인하고 싶다면 사이드 메뉴를 통해 <span class='special-word'>DashBoard</span> 페이지로 이동하세요!", unsafe_allow_html=True)
        st.caption('\n\nTeam I5 ')


    elif selected_page == "DashBoard":
        
        # dashboard_data = get_dashboard_data()
        st.write(f'<div class="iframe-container"><iframe class="iframe" src="{METABASE_URL}"></iframe></div>', unsafe_allow_html=True)
        st.write(page_style, unsafe_allow_html=True)
        st.caption('\n\nTeam I5 ')

    elif selected_page == "Travel Cost Prediction":

        st.write("Travel Cost Hunter는 출국 항공권,귀국 항공권 그리고 숙박권을 바탕으로 총 여행 경비를 예측합니다. 출국 항공권,귀국 항공권 그리고 숙박권에 대한 몇 가지 데이터를 입력해주시면 예측해드리겠습니다!")
         # 입력 데이터 (입력값 : 치환값)

        # 출국 날짜
        departure_date = st.date_input("출발 날짜를 고르세요.")
        departure_time = st.time_input("출발 시각을 고르거나 입력하세요")

        departure = str(departure_date)+" "+str(departure_time)
        departure = pd.to_datetime(departure)
        st.write(departure)

        # 국내 항공사 선택
        airlines_list = ['국내 항공사','국외 항공사']
        airlines_dict = {'국내 항공사':1,'국외 항공사':0}
        dIa = st.selectbox("국내 항공사를 꼭 사용하겠습니까?", airlines_list)
        departure_Interior_airlines = airlines_dict[dIa]

        # class 설정
        class_list = ["이코노미", "비지니스", "프리미엄 이코노미", "퍼스트"]
        class_dict = {"이코노미": 1, "비지니스": 2, "프리미엄 이코노미": 3, "퍼스트": 4}
        dclass = st.selectbox("좌석 클래스를 고르세요", class_list)
        departure_CLASS = class_dict[dclass]
        
        # 탑승 공항 선택
        port_d_list = ["인천국제공항(ICN)","김포공항(GMP)"]
        port_a_list = ["로스엔젤레스국제공항(LAX)","할리우드버뱅크공항(BUR)"]
        airport_dict = {"인천국제공항(ICN)":1,"김포공항(GMP)":2,"로스엔젤레스국제공항(LAX)":3,"할리우드버뱅크공항(BUR)":4}
        departure_airport = st.selectbox("출발 공항을 고르세요", port_d_list)
        departure_Port_d = airport_dict[departure_airport]
        arrival_airport = st.selectbox("도착 공항을 고르세요",port_a_list)
        departure_Port_a = airport_dict[arrival_airport]
        
        # 경유 여부
        flight_type_list = ['직항','경유 1회', '경유 2회','경유 3회','경유 4회']
        flight_type_dict = {'직항':0,'경유 1회':1, '경유 2회':2,'경유 3회':3,'경유 4회':4}
        flight_type = st.selectbox("항공권 경유 횟수를 고르세요",flight_type_list)
        departure_Flight_type = flight_type_dict[flight_type]
        
        # 자동 설정
        departure = pd.DataFrame({'이코노미': [11.215637583892619, 23.28843523073319, 25.919412673879446, 26.798203497615262, 51.6],
                    '비즈니스': [11.335042016806725, 22.935111930471425, 25.619097639981486, 28.99587301587302, 51.64812499999999],
                    '프리미엄 이코노미': [11.302, 23.054464520367937, 26.041043719989894, 26.864802784222736, 51], 
                    '퍼스트': [11.169999999999995, 19.993137996219282, 24.588079999999998, 29.370550660792954, 51]})
        departure_Flight_time_hour = round(departure[dclass][departure_Flight_type],2)

        #week_encoding = {'월':0,'화':1,'수':2,'목':3,'금':4,'토':5,'일':6}
        st.header('귀국일')
        # 귀국 날짜
        homecoming_date = st.date_input("귀국 날짜를 고르세요.")
        if departure_date == homecoming_date:
            st.write("<span class='warning-text'>출국일과 귀국일이 동일합니다.</span>",unsafe_allow_html=True)
        if departure_date > homecoming_date:
            st.write("<span class='warning-text'>오류:출국일 보다 과거의 시간입니다.</span>",unsafe_allow_html=True)
        homecoming_time = st.time_input("출발 시각을 고르거나 입력하세요", key="unique_key_for_homecoming_time")
        
        # homecoming = str(homecoming_date)+" "+str(homecoming_time)
        # homecoming = pd.to_datetime(homecoming)
        # st.write(homecoming)

        # 국내 항공사
        dIa2 = st.selectbox("국내 항공사를 꼭 사용하겠습니까?", airlines_list, key="unique_key_for_dIa2")
        homecoming_Interior_airlines = airlines_dict[dIa2]

        # 클래스 설정
        dclass2 = st.selectbox("좌석 클래스를 고르세요", class_list, key="unique_key_for_dclass2")
        homecoming_CLASS = class_dict[dclass2]

        # 경유 여부
        flight_type2 = st.selectbox("항공권 경유 횟수를 고르세요",flight_type_list, key="unique_key_for_flight_type2")
        homecoming_Flight_type = flight_type_dict[flight_type2]

        # 자동 설정
        # 탑승 공항 -> 기존에 선택한 공항의 반대로 자동으로 선택
        homecoming_Port_d = airport_dict[arrival_airport]
        homecoming_Port_a = airport_dict[departure_airport]

        entry = pd.DataFrame({'비즈니스': [13.326504065040652, 25.909293025470127, 28.1739769065521, 36.17582456140351, 54.69217391304348], 
         '이코노미': [13.261862068965517, 25.64626043841336, 28.733799201369084, 29.991457399103137, 56], 
         '프리미엄 이코노미': [13.166, 25.593388288800455, 28.34211437170805, 33.18008445945946, 81.385], 
         '퍼스트': [13.33435483870968, 24.71732824427481, 28.076642066420664, 31.87838331160365, 88.10833333333333]})
        homecoming_Flight_time_hour = round(entry[dclass2][homecoming_Flight_type],2)

        # test = homecoming_date + homecoming_time
        # st.write(f'{test}')
        st.write(f'{type(str(homecoming_date))}')
        st.write(f'{str(homecoming_date)+" "+str(homecoming_time)}')

        if st.button("선택 완료"):
            df_homecoming = pd.DataFrame({'departure_date': homecoming_date.day,
                            'departure_week':homecoming_date.weekday(),
                            'departure_time': homecoming_time.hour, 
                            'class': homecoming_CLASS,
                            'flight_type': homecoming_Flight_type,
                            'flight_time_hour': homecoming_Flight_time_hour, 
                            'port_d':homecoming_Port_d, 
                            'port_a':homecoming_Port_a, 
                            'interior_airlines': homecoming_Interior_airlines}, index=[0])
            
            df_departure = pd.DataFrame({'departure_date': departure_date.day,
                            'departure_week':departure_date.weekday(),
                            'departure_time': departure_time.hour, 
                            'class': departure_CLASS,
                            'flight_type': departure_Flight_type,
                            'flight_time_hour': departure_Flight_time_hour, 
                            'port_d':departure_Port_d, 
                            'port_a':departure_Port_a, 
                            'interior_airlines': departure_Interior_airlines}, index=[0])
            
            with open('last_model.pkl','rb') as pickle_file:
                model_departure = pickle.load(pickle_file)
            departure_pred = model_departure.predict(df_departure)[0]
            homecoming_pred = model_departure.predict(df_homecoming)[0]
            departure_result = format(int(departure_pred), ',d')
            homecoming_result = format(int(homecoming_pred), ',d')
            result = format(int(departure_pred+homecoming_pred), ',d')
            st.table(df_departure)
            st.table(df_homecoming)
            st.write(f'{departure_result}원')
            st.write(f'{homecoming_result}원')
            st.write(f'{result}원')
        

        st.write("\n숙소 가격 검색")

        col1,col2,col3,col4 = st.columns(4)
        # 입력값
        def get_user_input(conn):
            locations_query= "SELECT DISTINCT location FROM accommodation;"
            locations = pd.read_sql_query(locations_query,conn)['location'].tolist()
            
            with col1:
                check_in_day = st.date_input('체크인 날짜를 선택하세요.')
            with col2:
                location = st.selectbox('숙소 지역을 선택하세요.',locations)
            with col3:
                score = st.slider('최소 평점을 선택하세요.', 5.0, 10.0)
            if check_in_day.year != 23 and check_in_day.month != 9:
                st.write("<span class='warning-text'>23년도 9월만 서비스 가능합니다. 날짜를 확인해주세요.</span>",unsafe_allow_html=True)
            return check_in_day, location, score

        # 쿼리를 실행하는 함수
        def run_query(conn, check_in_day, location, score):
            query = f'''
                SELECT Name, price
                FROM accommodation
                WHERE check_in_day = '{check_in_day}' AND location = '{location}' AND score >= {score}
                ORDER BY price ASC
                LIMIT 5;
            '''
            result = pd.read_sql_query(query, conn)
            with col4:
                return result

        # 쿼리를 실행하는 함수
        def run_query(conn, check_in_day, location, score):
            query = f'''
                SELECT Name, price
                FROM Accommodation
                WHERE check_in_day = '{check_in_day}' AND location = '{location}' AND score >= {score}
                ORDER BY price ASC
                LIMIT 5;
            '''
            result = pd.read_sql_query(query, conn)
            with col4:
                return result

        conn = create_connection()
        if conn is None:
            st.error('데이터베이스 연결에 실패했습니다.')
            return
        
        check_in_day, location, score = get_user_input(conn)
        
        if st.button('검색'):
            if not check_in_day or not location:
                st.warning('날짜와 지역을 입력해주세요.')
            else:
                result = run_query(conn, check_in_day, location,score)
                st.table(result)

        st.caption('\n\nTeam I5 ')

                

if __name__ == "__main__":
    main()