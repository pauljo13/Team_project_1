import streamlit as st
import pandas as pd
import sqlite3

# SQLite 데이터베이스에 연결
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('sqlite.db.db')  # 데이터베이스 파일 경로를 입력
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

col1,col2,col3,col4 = st.columns(4)
# 입력값
def get_user_input(conn):
    locations_query= "SELECT DISTINCT location FROM accommodation;"
    locations = pd.read_sql_query(locations_query,conn)['location'].tolist()
    
    with col1:
        check_in_day = st.date_input('날짜를 선택하세요.')
    with col2:
        location = st.selectbox('지역을 입력하세요.',locations)
    with col3:
        score = st.slider('평점을 선택하세요.', 5.0, 10.0)
    
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

# 메인 함수
def main():
    st.title('여행경비예측서비스')
    
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

if __name__ == '__main__':
    main()
