import streamlit as st
import pandas as pd
from datetime import date
import datetime
import sqlite3


def create_connection(sqlite_db):
    global conn
    conn = None
    try:
        conn=sqlite3.connect(sqlite_db)
        return conn
    except sqlite3.Error as e:
        st.error(e)
    return conn

#쿼리실행함수
def get_unique_values(conn,check_in_day,location,score):
    try:
        cursor=conn.cursor()
        query =f"""
        SELECT ('Name,price')
        From accommodation'
        WHERE check_in_day = '{check_in_day}'
        AND location = '{location}'
        AND score >= '{score}'
        ORDER BY price ASC
        LIMIT 5;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [row[0] for row in result]
    except sqlite3.Error as e:
        st.error(e)

def main():
    if st.button("조건입력"):
        conn = create_connection('C:\Users\user\Desktop\AI_bootcamp\Sectionmine\streamlit_website')
        if conn is not None:
            st.success("조건을 검색해주세요")
        else:
            st.error("오류가 떴습니다")

    if conn is not None:
        location = get_unique_values(conn, "location_column")
        if location:
            selected_location = st.selectbox("장소 선택", location)
            st.write("선택한 장소:", selected_location)
        else:
            st.warning("데이터베이스에 장소 데이터가 없습니다.")
    
    date = st.date_input("날짜 입력")
    rating = st.slider("평점 입력", min_value=5, max_value=10, value=5)
    
    if st.button("검색"):
        if conn is not None:
            # 호텔 검색 쿼리 실행
            result = search_hotels(conn,check_in_day, location, score)
            if len(result) > 0:
                # 검색 결과 출력
                st.subheader("검색 결과:")
                for i, (Name, price) in enumerate(result, 1):
                    st.write(f"{i}. {Name} - {price}원")
            else:
                st.warning("조건에 해당하는 호텔이 없습니다.")

if __name__ == "__main__":
    main()