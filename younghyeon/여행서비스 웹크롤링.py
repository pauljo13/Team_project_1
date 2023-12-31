import time
import selenium
import pandas as pd
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime

#셀레니움 버전이 업그레이드 되면서 기존 명령어가 적용되지 않을 때
#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options = webdriver.ChromeOptions()

#무한 스크롤
def scroll():
    before_h = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)

def check_in_out(driver,month,week): #여행 날짜 선정 (month:1~5 / week:1~7) !!!참고한것!!!
    check_in = driver.find_element(By.XPATH, f'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[2]/div[2]/div[3]/div[{month}]/div[{week}]/div/div')
    check_in.click()
    next_day = week + 1
    if next_day > 7:
        month += 1
        next_day = 1
    if month == 5 and week == 6:
        check_out = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[2]/div[2]/div[3]/div[1]/div[7]/div')
    else:
        check_out = driver.find_element(By.XPATH, f'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[2]/div[2]/div[3]/div[{month}]/div[{next_day}]/div/div')
    check_out.click()
    time.sleep(2)

def data_extraction(hotel_elements): #데이터 추출
    hotel_data=[]
    
    for hotel_element in hotel_elements:
        try: #예외처리
            global hotel_name
            hotel_name_element = hotel_element.find_element(By.CLASS_NAME,'sc-jrAGrp sc-kEjbxe eDlaBj dscgss')
            hotel_name = hotel_element.text
        except:
            pass
          
        try:
            global hotel_price
            hotel_price_element = hotel_element.find_element(By.CLASS_NAME,'PropertyCardPrice__Value')
            hotel_price = hotel_price_element.text
        except:
            pass

        try:
            global hotel_location
            hotel_location_element = hotel_element.find_element(By.CLASS_NAME,'sc-jrAGrp sc-kEjbxe eDlaBj fRhhIV sc-crrsfI iDhzRL')
            hotel_location = hotel_location_element.text
        except:
            pass

        try:
            global hotel_rating
            hotel_rating_element = hotel_element.find_element(By.CLASS_NAME,'sc-bdfBwQ sc-gsTCUz  hwyJDv')
            hotel_rating = hotel_rating_element.text
        except:
            pass

        hotel_data.append({'hotel_name,hotel_price,hotel_location,hotel_rating,check_in_day,check_out_day'})

def convert_date_format(input_date_str): #참고했음
    dt = datetime.strptime(input_date_str, '%Y년 %m월 %d일')
    return dt.strftime('%m_%d')
        
day_list = []
for i in range(1,6):
    for j in range(1,8):
        day_list.append((i,j))
day_list = day_list[4:34]
count = 0


#웹페이지 해당 주소로 이동
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.agoda.com/ko-kr/")
time.sleep(5)

#팝업창을 없애는 코드
popup_box = driver.find_element(By.XPATH,"/html/body/div[12]/div[2]/button")
popup_box.click()
time.sleep(5)

#로스엔젤레스로 검색한다
search_box = driver.find_element(By.XPATH,'//*[@id="textInput"]')
search_box.send_keys("로스엔젤레스")
search_box.send_keys(Keys.RETURN)
time.sleep(3)

autocomplete_tab = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/ul/li[1]')
autocomplete_tab.click()
time.sleep(3)

#날짜 설정
next_month_button = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[1]/span[2]')
next_month_button.click()
time.sleep(3)

start_date = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[2]/div[1]/div[3]/div[1]/div[5]/span')
start_date.click()
time.sleep(3)

end_date = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[6]/div/div/div[1]/div/div[2]/div[1]/div[3]/div[1]/div[6]/span')
end_date.click()
time.sleep(3)

#이용 인원 수 설정
human_num = driver.find_element(By.XPATH,'//*[@id="occupancy-selector"]/div/div/div[2]/div[2]/div[1]')
human_num.click()
time.sleep(3)

#검색
search_button = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[2]/button/div')
search_button.click()
time.sleep(3)

search_button = driver.find_element(By.XPATH,'//*[@id="SearchBoxContainer"]/div[2]/button/div')
search_button.click()
time.sleep(3)

hotel_loc_score = driver.find_element(By.XPATH,'//*[@id="SideBarLocationFilters"]/div[10]/div[2]/ul/li[1]/span/span[1]/span')
hotel_loc_score.click()
time.sleep(3)

check_in_day = driver.find_element(By.XPATH, '//*[@id="check-in-box"]/div/div/div/div[1]').text
check_out_day = driver.find_element(By.XPATH, '//*[@id="check-out-box"]/div/div/div/div[1]').text

hotel_elements = driver.find_elements(By.XPATH,'//*[@id="contentContainer"]/div[4]/ol/li[1]')
hotel_data = data_extraction(hotel_elements)
df_hotels = pd.DataFrame(hotel_data)



"""
CREATE Accommodation (
  ID INT
  시설 이름 CHAR(100)
  별점 INT
  시설 유형 CHAR(100)
  가격 (INT)
  위치 CHAR(100)
  체크인 날짜 DATETIME
  요일 CHAR(100)
);
 숙박 디폴트 옵션: 성인 1인, 1박 기준, 지역 한정. <아고다 기준, 9월>
"""
