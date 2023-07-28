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


# ## 비행시간 출력 함수
# def Flight_Time(Departure_or_entry,Class,Flight_type):
#     # 비행 시간표
#     departure = pd.DataFrame({'비즈니스': [11.335042016806725, 22.935111930471425, 25.619097639981486, 28.99587301587302, 51.64812499999999], 
#              '이코노미': [11.215637583892619, 23.28843523073319, 25.919412673879446, 26.798203497615262, 51.6],
#              '프리미엄 이코노미': [11.302, 23.054464520367937, 26.041043719989894, 26.864802784222736, 51], 
#              '퍼스트': [11.169999999999995, 19.993137996219282, 24.588079999999998, 29.370550660792954, 51]}).round(2)
#     entry = pd.DataFrame({'비즈니스': [13.326504065040652, 25.909293025470127, 28.1739769065521, 36.17582456140351, 54.69217391304348], 
#          '이코노미': [13.261862068965517, 25.64626043841336, 28.733799201369084, 29.991457399103137, 56], 
#          '프리미엄 이코노미': [13.166, 25.593388288800455, 28.34211437170805, 33.18008445945946, 81.385], 
#          '퍼스트': [13.33435483870968, 24.71732824427481, 28.076642066420664, 31.87838331160365, 88.10833333333333]}).round(2)
#     # 비행 시간 출력
#     if Departure_or_entry == '출국':
#         return departure[Class][Flight_type]
#     elif Departure_or_entry == '귀국':
#         return entry[Class][Flight_type]

# ## 날짜 데이터 처리
# def Date_data(Date):
#     dt = datetime(Date)
#     day = dt.day
#     # 월:0,화:1,수:2,목:3,금:4,토:5,일:6 /->전환/ '토':2, '금':1, '화':5, '수':6, '일':3, '월':4, '목':7
#     week_list = {'0':'월','1':'화','2':'수','3':'목','4':'금','5':'토','6':'일'}
#     week_code = {'토':2, '금':1, '화':5, '수':6, '일':3, '월':4, '목':7}
#     wc = week_list[str(dt.weekday())]
#     week = week_code[wc]
#     hour = dt.hour
#     return day, week, hour

# ## 데이터 프레임형태로 만드는 함수
# def Make_DataFrame(Departure_or_entry,Date):
#     day, week, hour = Date_data(Date)
#     Flight_time_hour = Flight_Time(Departure_or_entry,Class,Flight_type)
#     return pd.DataFrame({'class': Class, 
#                          'port_a': Port_a, 
#                          'interior_airlines': Interior_airlines, 
#                          'flight_type': Flight_type,
#                          'flight_time_hour': Flight_time_hour, 
#                          'port_d': Port_d,
#                          'departure_hour': hour, 
#                          'departure_date_day': day, 
#                          'departure_day': week})

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
        st.write("이곳은 대시보드 페이지입니다. 대시보드 연결을 기다립니다..")
        st.caption('\n\nTeam I5 ')

        # # Metabase 설정
        # METABASE_URL = "https://your-metabase-url.com"
        # METABASE_USERNAME = "your-metabase-username"
        # METABASE_PASSWORD = "your-metabase-password"
        # DASHBOARD_ID = 1

        # # Metabase API 로그인
        # def metabase_login():
        #     url = f"{METABASE_URL}/api/session"
        #     data = {
        #         "username": METABASE_USERNAME,
        #         "password": METABASE_PASSWORD
        #     }
        #     response = requests.post(url, json=data)
        #     return response.json()["id"]

        # # 대시보드 데이터 가져오기
        # def get_dashboard_data():
        #     session_id = metabase_login()
        #     url = f"{METABASE_URL}/api/dashboard/{DASHBOARD_ID}/query"
        #     headers = {
        #         "X-Metabase-Session": session_id
        #     }
        #     response = requests.get(url, headers=headers)
        #     return response.json()

        # dashboard_data = get_dashboard_data()

        # # Streamlit에서 대시보드 데이터 시각화 또는 표시
        # # 예: 테이블 또는 차트로 데이터를 시각화하거나 필요한 방식으로 표시
        # st.write("대시보드 데이터:")
        # st.write(dashboard_data)
        
    elif selected_page == "Travel Cost Prediction":
        
        st.write("원하시는 일정의 항공권에 대한 가격을 예측하고 싶다면 몇 가지 데이터를 입력해 주세요.")
        st.write("출국 항공권 가격 예측")
        # 입력 데이터 (입력값 : 치환값)
        direction_list = ["한국->미국","미국->한국"]
        direction_dict = {"한국->미국":"출국","미국->한국":"입국"}
        airlines_list = ['국내 항공사','국외 항공사']
        airlines_dict = {'국내 항공사':1,'국외 항공사':0}
        class_list = ["이코노미", "비지니스", "프리미엄 이코노미", "퍼스트"]
        class_dict = {"이코노미":1, "비지니스":2, "프리미엄 이코노미":3, "퍼스트":4}
        airport_list = ["인천국제공항(ICN)","김포공항(GMP)","로스엔젤레스국제공항(LAX)","할리우드버뱅크공항(BUR)"]
        airport_dict = {"인천국제공항(ICN)":1,"김포공항(GMP)":2,"로스엔젤레스국제공항(LAX)":3,"할리우드버뱅크공항(BUR)":4}
        flight_type_list = ['직항','경유 1회', '경유 2회','경유 3회','경유 4회']
        flight_type_dict = {'직항':0,'경유 1회':1, '경유 2회':2,'경유 3회':3,'경유 4회':4}
        # ## 출국 데이터 입력
        # Departure_or_entry = '출국' #비행기 방향(KA->LA 출국)
        # Class = input() #클래스 선택( 이코노미 : 1 / 비즈니스 : 2 / 프리미엄 이코노미 : 3 / 퍼스트 : 4 )
        # Port_d = input() #탑승 공항( K->L : ICN = 1 / GMP = 2 | L->K LAX = 1 / BUR = 2 )
        # Date = input() #날짜(-> departure_day 요일/departure_date_day 일/ departure_hour 시간/ departure_minute 분 으로 데이터가 나누어짐)
        # Port_a = input() #하차 공항( K->L : LAX = 1 / BUR = 2 | L->K GMP = 1 / ICN = 2 )
        # Interior_airlines = input() #국내 항공 선택(국내항공 선택 : 1 / 국내항공 선택 안함 : 0)
        # Flight_type = input() #직항 경유 선택 여부(직항 : 0 / 경유 회수 : 1, 2, 3, 4)
        # departure_df = Make_DataFrame(Departure_or_entry,Date)
        direction = st.selectbox("항공권 방향을 고르세요", direction_list)
        departure_date = st.date_input("출발 날짜를 고르세요. (23년도 9월만 예측 가능)")
        if departure_date.year != 23 and departure_date.month != 9:
            st.write("<span class='warning-text'>23년도 9월만 서비스 가능합니다. 날짜를 확인해주세요.</span>",unsafe_allow_html=True)
        departure_time = st.time_input("출발 시각을 고르거나 입력하세요")
        dclass = st.selectbox("좌석 클래스를 고르세요", class_list)
        departure_airport = st.selectbox("출발 공항을 고르세요", airport_list)
        arrival_airport = st.selectbox("도착 공항을 고르세요",airport_list)
        flight_type = st.selectbox("항공권 경유 횟수를 고르세요",flight_type_list)

        # departure_df = Make_DataFrame(Departure_or_entry,Date)


        # ## 귀국 데이터 입력
        # Departure_or_entry = '귀국' #비행기 방향(LA->KA 입국)
        # Class = input() #클래스 선택( 이코노미 : 1 / 비즈니스 : 2 / 프리미엄 이코노미 : 3 / 퍼스트 : 4 )
        # Port_d = input() #탑승 공항( K->L : ICN = 1 / GMP = 2 | L->K LAX = 1 / BUR = 2 )
        # Date = input() #날짜(-> departure_day 요일/departure_date_day 일/ departure_hour 시간/ departure_minute 분 으로 데이터가 나누어짐)
        # Port_a = input() #하차 공항( K->L : LAX = 1 / BUR = 2 | L->K GMP = 1 / ICN = 2 )
        # Interior_airlines = input() #국내 항공 선택(국내항공 선택 : 1 / 국내항공 선택 안함 : 0)
        # Flight_type = input() #직항 경유 선택 여부(직항 : 0 / 경유 회수 : 1, 2, 3, 4)
        # entry_df = Make_DataFrame(Departure_or_entry,Date)

        
        # # 출국(KA -> LA)
        # with open('departure.pkl','rb') as pickle_file:
        #     model_departure = pickle.load(pickle_file)
        # departure_pred = model_departure.predict(departure_df)[0]

        # # 귀국(LA -> KA)
        # with open('entry.pkl','rb') as pickle_file:
        #     model_entry = pickle.load(pickle_file)
        # entry_pred = model_departure.predict(entry_df)[0]

        # # 티켓 완복 가격
        # Price = round(departure_pred + entry_pred,0)
        # print('출국 티켓값 : ',int(departure_pred))
        # print('입국 티켓값 : ',int(entry_pred))
        # print('총 티켓값 : ', int(Price))


        st.caption('\n\nTeam I5 ')

if __name__ == "__main__":
    main()