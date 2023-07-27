import streamlit as st
import requests

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
        st.write("이곳은 여행 경비 예측 모델을 사용해 볼 수 있는 페이지입니다. 모델을 기다립니다..")
        st.caption('\n\nTeam I5 ')

if __name__ == "__main__":
    main()