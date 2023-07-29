import streamlit as st
import requests
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from category_encoders import OrdinalEncoder
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor
import pickle
import random
# import shap
# from pdpbox.pdp import pdp_isolate, pdp_plot
import datetime
from datetime import datetime, timedelta
import sqlite3
# Metabase 설정




# ============================== 수정한 코드 부분 시작 =============================== #
class SessionState:
    def __init__(self, **kwargs):
        self.hotel_result = pd.DataFrame()
        self.hotel = ""
        self.selected_hotel_price = 0
        self.__dict__.update(kwargs)

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('sqlite_db.db')  # 데이터베이스 파일 경로를 입력
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# check in 날짜 반환
def check_in(d_time, travel_class, flight_type):
    check_in_hour = {
        '이코노미': [-4.78, 7.29, 9.92, 10.80, 35.60],
        '비즈니스': [-4.66, 6.94, 9.62, 13.00, 35.65],
        '프리미엄 이코노미': [-4.70, 7.05, 10.04, 10.86, 35.00],
        '퍼스트': [-4.83, 3.99, 8.59, 13.37, 35.00]
    }

    def calculate_check_in_time(dt, t_class, f_type):
        hour_offset = check_in_hour[t_class][f_type]
        dt += timedelta(hours=hour_offset)
        if dt.hour >= 24:
            dt += timedelta(days=1)
            dt = dt.replace(hour=dt.hour % 24)
        return dt

    return calculate_check_in_time(d_time, travel_class, flight_type)

# check in 날짜로 부터 ckech out 날짜 계산
def travel_duration(check_in, h_date):
    check_in_datetime = datetime.combine(check_in, datetime.min.time())
    h_date_datetime = datetime.combine(h_date, datetime.min.time())
    travel_duration = h_date_datetime - check_in_datetime
    return travel_duration.days

# ============================== 수정한 코드 부분 끝 =============================== #





def main():
# ============================== 수정한 코드 부분 시작 =============================== #
    if "state" not in st.session_state:
        st.session_state.state = SessionState()

    state = st.session_state.state
# ============================== 수정한 코드 부분 끝 =============================== #
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
        .centered-btn {
        display: flex;
        justify-content: center;
        }
        .lefted-btn {
        display: flex;
        justify-content: left;
        }
        .righted-btn {
        display: flex;
        justify-content: right;
        }
    </style>
    """
    st.markdown(page_style, unsafe_allow_html=True)

    # 타이틀 표시
    st.markdown("<h1 class='title'>Travel Cost Hunter</h1>", unsafe_allow_html=True)

    # 사이드바에서 페이지 선택
    selected_page = st.sidebar.selectbox("Menu", ["Home", "Travel Cost Prediction", "DashBoard"])

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
        predict_process_page = st.session_state.get("predict_process_page", "시작페이지")
        if predict_process_page == "시작페이지":
            st.write("Travel Cost Hunter는 출국 항공권,귀국 항공권 그리고 숙박권을 바탕으로 총 여행 경비를 예측합니다. 출국 항공권,귀국 항공권 그리고 숙박권에 대한 몇 가지 데이터를 입력해주시면 예측해드리겠습니다!")
            st.caption('\n\nTeam I5 ')
            col1, col2, col3 = st.columns([0.31, 0.33, 0.1])
            with col2:
                if st.button("시작하기"):
                    # 입력 받은 데이터를 세션 상태에 저장하고 페이지 전환
                    st.session_state.predict_process_page = "출국항공권"
                    st.experimental_rerun()

        elif predict_process_page == "출국항공권":
            
            # 입력 데이터 (입력값 : 치환값)
            st.header('출국 항공권')
            # 출국 날짜
            departure_date = st.date_input("출발 날짜를 고르세요.")
            departure_time = st.time_input("출발 시각을 고르거나 입력하세요")

        
            d_date = datetime.combine(departure_date, departure_time)
            st.session_state['d_date'] = d_date
        
            departure = str(departure_date)+" "+str(departure_time)
            departure = pd.to_datetime(departure)

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
            
            st.caption('\n\nTeam I5 ')
            col1, col2, col3 = st.columns([0.28, 0.2, 0.18])
            with col1:
                if st.button("처음으로", key="Travel Cost Prediction return to startpage1"):
                    st.session_state.predict_process_page = "시작페이지"
                    st.experimental_rerun()
            with col2:
                pass
            with col3:
                if st.button("귀국 항공권 선택하기", key="Travel Cost Prediction from depart ticket to return ticket"):
                    # 자동 설정
                    departure = pd.DataFrame({'이코노미': [11.215637583892619, 23.28843523073319, 25.919412673879446, 26.798203497615262, 51.6],
                                '비즈니스': [11.335042016806725, 22.935111930471425, 25.619097639981486, 28.99587301587302, 51.64812499999999],
                                '프리미엄 이코노미': [11.302, 23.054464520367937, 26.041043719989894, 26.864802784222736, 51], 
                                '퍼스트': [11.169999999999995, 19.993137996219282, 24.588079999999998, 29.370550660792954, 51]})
                    departure_Flight_time_hour = round(departure[dclass][departure_Flight_type],2)

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
                    departure_result = format(int(departure_pred), ',d')
                    # 입력 받은 데이터를 세션 상태에 저장하고 페이지 전환
                    
                    st.session_state['df_departure'] = df_departure
                    st.session_state['departure_result'] = departure_result
                    st.session_state['departure_pred'] = departure_pred
                    st.session_state['departure_date'] = departure_date
                    st.session_state['arrival_airport'] = arrival_airport
                    st.session_state['departure_airport'] = departure_airport
                    st.session_state['dclass'] = dclass
                    st.session_state['departure_Flight_type'] = departure_Flight_type
                    st.session_state.predict_process_page = "귀국항공권"
                    st.experimental_rerun()
            

        elif predict_process_page == "귀국항공권":
            
            st.header('귀국 항공권')
            airlines_list = ['국내 항공사','국외 항공사']
            airlines_dict = {'국내 항공사':1,'국외 항공사':0}
            class_list = ["이코노미", "비지니스", "프리미엄 이코노미", "퍼스트"]
            class_dict = {"이코노미": 1, "비지니스": 2, "프리미엄 이코노미": 3, "퍼스트": 4}
            port_d_list = ["인천국제공항(ICN)","김포공항(GMP)"]
            port_a_list = ["로스엔젤레스국제공항(LAX)","할리우드버뱅크공항(BUR)"]
            airport_dict = {"인천국제공항(ICN)":1,"김포공항(GMP)":2,"로스엔젤레스국제공항(LAX)":3,"할리우드버뱅크공항(BUR)":4}
            flight_type_list = ['직항','경유 1회', '경유 2회','경유 3회','경유 4회']
            flight_type_dict = {'직항':0,'경유 1회':1, '경유 2회':2,'경유 3회':3,'경유 4회':4}

            # 귀국 날짜
            departure_date = st.session_state['departure_date']
            st.subheader(f"출국일 : {departure_date}")
            homecoming_date = st.date_input("귀국 날짜를 고르세요.")
            if departure_date == homecoming_date:
                st.write("<span class='warning-text'>출국일과 귀국일이 동일합니다.</span>",unsafe_allow_html=True)
            if departure_date > homecoming_date:
                st.write("<span class='warning-text'>오류:출국일 보다 과거의 시간입니다.</span>",unsafe_allow_html=True)
            homecoming_time = st.time_input("출발 시각을 고르거나 입력하세요", key="unique_key_for_homecoming_time")
# ============================== 수정한 코드 부분 시작 =============================== #
            h_date = datetime.combine(homecoming_date, homecoming_time)
            st.session_state['h_date'] = h_date

# ============================== 수정한 코드 부분 끝 =============================== #

            # 국내 항공사
            dIa2 = st.selectbox("국내 항공사를 꼭 사용하겠습니까?", airlines_list, key="unique_key_for_dIa2")
            homecoming_Interior_airlines = airlines_dict[dIa2]

            # 클래스 설정
            dclass2 = st.selectbox("좌석 클래스를 고르세요", class_list, key="unique_key_for_dclass2")
            homecoming_CLASS = class_dict[dclass2]

            # 경유 여부
            flight_type2 = st.selectbox("항공권 경유 횟수를 고르세요",flight_type_list, key="unique_key_for_flight_type2")
            homecoming_Flight_type = flight_type_dict[flight_type2]

            st.caption('\n\nTeam I5 ')
            col1, col2, col3 = st.columns([0.28, 0.2, 0.14])

            with col1:
                if st.button("출국 항공권 선택으로 돌아가기", key="Travel Cost Prediction from return ticket to depart ticket"):
                    st.session_state.predict_process_page = "출국항공권"
                    st.experimental_rerun()
            with col3:
                if st.button("숙박권 선택으로", key="Travel Cost Prediction from return ticket to accomoation ticket"):
                    # 자동 설정
                    # 탑승 공항 -> 기존에 선택한 공항의 반대로 자동으로 선택
                    arrival_airport = st.session_state['arrival_airport']
                    departure_airport = st.session_state['departure_airport']
                    homecoming_Port_d = airport_dict[arrival_airport]
                    homecoming_Port_a = airport_dict[departure_airport]

                    entry = pd.DataFrame({'비즈니스': [13.326504065040652, 25.909293025470127, 28.1739769065521, 36.17582456140351, 54.69217391304348], 
                    '이코노미': [13.261862068965517, 25.64626043841336, 28.733799201369084, 29.991457399103137, 56], 
                    '프리미엄 이코노미': [13.166, 25.593388288800455, 28.34211437170805, 33.18008445945946, 81.385], 
                    '퍼스트': [13.33435483870968, 24.71732824427481, 28.076642066420664, 31.87838331160365, 88.10833333333333]})
                    homecoming_Flight_time_hour = round(entry[dclass2][homecoming_Flight_type],2)

                    df_homecoming = pd.DataFrame({'departure_date': homecoming_date.day,
                                    'departure_week':homecoming_date.weekday(),
                                    'departure_time': homecoming_time.hour, 
                                    'class': homecoming_CLASS,
                                    'flight_type': homecoming_Flight_type,
                                    'flight_time_hour': homecoming_Flight_time_hour, 
                                    'port_d':homecoming_Port_d, 
                                    'port_a':homecoming_Port_a, 
                                    'interior_airlines': homecoming_Interior_airlines}, index=[0])
                    
                    with open('last_model.pkl','rb') as pickle_file:
                        model_departure = pickle.load(pickle_file)
                    homecoming_pred = model_departure.predict(df_homecoming)[0]     
                    homecoming_result = format(int(homecoming_pred), ',d')

                    st.session_state['homecoming_pred'] = homecoming_pred
                    st.session_state['df_homecoming'] = df_homecoming
                    st.session_state['homecoming_result'] = homecoming_result
                    st.session_state.predict_process_page = "숙박권"
                    st.experimental_rerun()
                
        elif predict_process_page == "숙박권":



# ============================== 수정한 코드 부분 시작=============================== #
            st.subheader("\n숙소 가격 검색")
            d_date = st.session_state['d_date']
            dclass = st.session_state['dclass']
            departure_Flight_type = st.session_state['departure_Flight_type']

            col1,col2,col3,col4 = st.columns(4)
            # 입력값
            def get_user_input(conn):
                where = str(check_in(d_date,dclass,departure_Flight_type).date())
                locations_query= f"SELECT DISTINCT location FROM accommodation WHERE check_in_day = '{where}';"
                locations = pd.read_sql_query(locations_query,conn)['location'].tolist()
                
                with col1:
                    check_in_day = check_in(d_date,dclass,departure_Flight_type).date()
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
            st.session_state['check_in_day'] = check_in_day 
            if st.button("검색하기", key="Travel Cost Prediction accommoation search"):
                if not check_in_day or not location:
                    st.warning('날짜와 지역을 입력해주세요.')
                else:
                    state.hotel_result = run_query(conn, check_in_day, location, score)
                    if state.hotel_result.empty:
                        st.warning("검색 결과가 없습니다.")
                    else:
                        st.table(state.hotel_result)
            

            result_encode = {}
            result_copy = state.hotel_result.copy()
            if result_copy.empty:
                st.warning("검색 결과가 없거나 하나의 결과만 있어 호텔을 선택할 수 없습니다.")
            else:
                result_columns = list(result_copy.columns)
                for i in range(len(state.hotel_result)):
                    name = result_copy[result_columns[0]][i]
                    price = result_copy[result_columns[1]][i]
                    result_encode[f'이름: {name}        가격: {price}'] = price

            state.hotel = st.selectbox("호텔을 고르세요", list(result_encode.keys()), key="unique_key_for_hotel")
            state.selected_hotel_price = result_encode.get(state.hotel, 0)
            st.write(f'{state.selected_hotel_price}')
# ============================== 수정한 코드 부분  끝=============================== #




            st.caption('\n\nTeam I5 ')
            col1, col2, col3 = st.columns([0.28, 0.2, 0.18])
            with col1:
                if st.button("귀국 항공권 선택으로 돌아가기", key="Travel Cost Prediction from accommodation to return ticket"):
                    st.session_state.predict_process_page = "귀국항공권"
                    st.experimental_rerun()
            with col3:
                if st.button("최종 비용 예측하기", key="Travel Cost Prediction predict button"):
                    st.session_state.predict_process_page = "최종결과"
                    st.experimental_rerun()

        elif predict_process_page == "최종결과":
            departure_pred = st.session_state['departure_pred']
            homecoming_pred = st.session_state['homecoming_pred']
            df_departure = st.session_state['df_departure']
            df_homecoming = st.session_state['df_homecoming']
            departure_result = st.session_state['departure_result']
            homecoming_result = st.session_state['homecoming_result']

# ============================== 수정한 코드 부분  시작 =============================== #
            check_in_day = st.session_state['check_in_day']
            h_date = st.session_state['h_date']
            air_result = format(int(departure_pred+homecoming_pred), ',d')
            hotel_price_result = format(int(state.selected_hotel_price), ',d')
            Travel_duration_day = travel_duration(check_in_day, h_date)
            total_hotel_price = int(hotel_price_result.replace(',', '')) * (Travel_duration_day - 1)
            total_travel_price = int(hotel_price_result.replace(',', '')) * (Travel_duration_day - 1) + int(departure_pred+homecoming_pred)

            st.write(f"선택한 호텔 1박 가격: {hotel_price_result}원")
            st.write(f"선택한 호텔 총 가격: {total_hotel_price:,d}원")
            st.write(f'출국 비행기 티켓가격 : {departure_result}원')
            st.write(f'귀국 비행기 티켓가격 : {homecoming_result}원')
            st.write(f' 총 비행기 티켓가격 : {air_result}원')
            st.write(f'여행 총 가격: {total_travel_price:,d}원')
# ============================== 수정한 코드 부분  끝=============================== #


            st.caption('\n\nTeam I5 ')
            col1, col2, col3 = st.columns([0.28, 0.2, 0.20])
            with col1:
                if st.button("시작페이지로", key="Travel Cost Prediction from predict to start page"):
                    st.session_state.predict_process_page = "시작페이지"
                    st.experimental_rerun()
            with col2:
                if st.button("숙박권 선택으로 돌아가기", key="Travel Cost Prediction from predict to accommodation ticket"):
                    st.session_state.predict_process_page = "숙박권"
                    st.experimental_rerun()


if __name__ == "__main__":
    main()