import selenium
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from datetime import datetime
#=============================== 함수 ===============================
#여행 날짜 선정 (month:1~5 / week:1~7)
def check_in_out(driver,month,week):
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

def driver_refresh():
    driver.implicitly_wait(5)
    good = driver.find_element(By.XPATH,'//*[@id="SideBarLocationFilters"]/div[12]/div[2]/ul/li[3]/span/span[1]/span')
    good.click()
    driver.implicitly_wait(2)

# 스크롤 함수
def scroll():
    for i in range(0,27493,700):
        driver.execute_script(f"window.scrollTo(0,{i});")
        time.sleep(1)

# 데이터 추출 함수
def data_extraction(hotel_elements):
    hotel_data = []
    print('정보 추출중...')
    for hotel_element in hotel_elements:
        # 호텔 이름, 가격, 평점 등과 같은 정보를 추출합니다.
        # 적절한 요소와 속성을 식별하여 데이터를 추출해야 합니다.
        try:
            hotel_name_element = hotel_element.find_element(By.CLASS_NAME,'sc-jrAGrp.sc-kEjbxe.eDlaBj.dscgss')
            hotel_name = hotel_name_element.text
        except:
            pass
        
        try:
            hotel_price_element = hotel_element.find_element(By.CLASS_NAME,'PropertyCardPrice__Value')
            hotel_price = hotel_price_element.text
        except:
            pass
        
        try:
            hotel_location_element = hotel_element.find_element(By.CLASS_NAME,'sc-hBEYos.cMRRiJ')
            hotel_location = hotel_location_element.text
        except:
            pass

        try:
            hotel_rating_element = hotel_element.find_element(By.CLASS_NAME,'Typographystyled__TypographyStyled-sc-j18mtu-0.Hkrzy.kite-js-Typography')
            hotel_rating = hotel_rating_element.text
        except:
            pass
        
        hotel_data.append({
            '호텔 이름': hotel_name,
            '위치': hotel_location,
            'check_in_day' : check_in_day,
            'check_in_week' : check_in_week,
            'check_out_day' : check_out_day,
            'check_out_week' : check_out_week,
            '가격': hotel_price,
            '평점': hotel_rating
        })
    print('정보 추출 완료')
    return hotel_data

# 날짜 데이터
def convert_date_format(input_date_str):
    # '년 월 일' 형식의 문자열을 datetime 객체로 파싱
    dt = datetime.strptime(input_date_str, '%Y년 %m월 %d일')
    # 원하는 형식으로 포맷팅
    return dt.strftime('%m_%d')
#=============================== 함수 ===============================

# 데이터를 수집할 데이터 범위 설정
day_list = []
for i in range(1,6):
    for j in range(1,8):
        day_list.append((i,j))
day_list = day_list[4:34]
count = 0
for i in day_list:
    # 브라우저 꺼짐 방지 옵션
    print(f'{count}번째 수행 시작')
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    url = 'https://www.agoda.com/ko-kr/?cid=1891463&tag=3efe13a1-1d9d-38ef-93e8-dfb7f2c53ec0&gclid=Cj0KCQjwk96lBhDHARIsAEKO4xZYURYV-sVuksr5zPfNuPl9ceepMKW5naEQVcoM70MqgBjqY3rF_FQaAks1EALw_wcB'
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(10)
    print('드라이브 실행 중...')
    #광고 닫기
    try:
        close_button = driver.find_element(By.CLASS_NAME, "ab-close-button")
        close_button.click()
    except:
        pass

    #여행 지역 검색
    time.sleep(2)
    search_area = driver.find_element(By.CLASS_NAME, "IconBox__wrapper")
    search_area.click()
    search_area2 = driver.find_element(By.CLASS_NAME, "SearchBoxTextEditor.SearchBoxTextEditor--autocomplete")
    search_area2.click()
    search_area2.send_keys('로스앤젤레스 (CA)')
    driver.find_element(By.CLASS_NAME, "Suggestion.Suggestion__categoryName").click()
    time.sleep(2)
    print('지역 선택')

    check_in_out(driver,i[0],i[1])

    #인원 수 설정
    people_num = driver.find_element(By.CLASS_NAME,'sc-bdfBwQ.sc-gsTCUz.cNevaa')
    people_num.click()
    time.sleep(2)
    print('인원 수 설정')

    #검색
    for i in range(2):
        search = driver.find_element(By.CLASS_NAME, 'Buttonstyled__ButtonStyled-sc-5gjk6l-0.iCZpGI.Box-sc-kv6pi1-0.fDMIuA')
        search.click()

    driver.switch_to.window(driver.window_handles[-1])
    print('검색결과')
    driver_refresh()

    check_in_day = driver.find_element(By.XPATH, '//*[@id="check-in-box"]/div/div/div/div[1]').text
    check_in_week = driver.find_element(By.XPATH, '//*[@id="check-in-box"]/div/div/div/div[2]').text

    check_out_day = driver.find_element(By.XPATH, '//*[@id="check-out-box"]/div/div/div/div[1]').text
    check_out_week = driver.find_element(By.XPATH, '//*[@id="check-out-box"]/div/div/div/div[2]').text

    # 전체 hotel 정보들
    scroll()
    hotel_elements = driver.find_elements(By.XPATH, '//*[@class="PropertyCard PropertyCardItem"]')
    # DataFrame 생성
    hotel_data = data_extraction(hotel_elements)
    df_hotels = pd.DataFrame(hotel_data)

    page_numder = driver.find_element(By.CLASS_NAME, 'pagination2__text').text.split()
    print('크롤링 시작...')
    while True:
        time.sleep(2)
        driver.implicitly_wait(2)
        driver.switch_to.window(driver.window_handles[-1])
        next_page = driver.find_element(By.XPATH , '//*[@id="paginationNext"]')
        next_page.click()
        scroll()
        page_numder = driver.find_element(By.CLASS_NAME, 'pagination2__text').text.split()

        hotel_elements = driver.find_elements(By.XPATH, '//*[@class="PropertyCard PropertyCardItem"]')
        hotel_data = data_extraction(hotel_elements)
        df_hotels2 = pd.DataFrame(hotel_data)
        df_hotels = pd.concat([df_hotels,df_hotels2])

        if page_numder[0] >= page_numder[2]:
            break
        page_numder[0] == page_numder[2]

    # DataFrame 출력
    file_name = f'agoda_hotels_{convert_date_format(check_in_day)}.csv'
    df_hotels.to_csv(file_name, index=False)

    # 크롤링이 끝난 후에는 드라이버를 닫아주세요
    driver.quit()
    count += 1
    print('성공적으로 파일이 만들어졌습니다.')