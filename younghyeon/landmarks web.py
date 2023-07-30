import streamlit as st
import pandas as pd

def read_data():
    data=pd.read_csv('landmarks.csv')
    return data

def main():
    st.title('랜드마크 가격')
    data = read_data()
    selected_title = st.selectbox('Landmark Title 선택',data['title'])
    selected_price = data[data['title'] == selected_title]['price'].iloc[0]
    
    st.write(f"{selected_title}의 가격: {selected_price}원")

if __name__ == '__main__':
    main()