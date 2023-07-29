from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import re
import pandas as pd


def get_data(url,day):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(1)

    tckt = []
    data = []
    week = ['월', '화', '수', '목', '금', '토', '일']
    d, j = 1, 4

    for _ in range(day):
        for i in range(1,5):

            # 좌석등급 바꾸기
            gbox_path = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div'
            gbox = driver.find_element(By.XPATH, gbox_path)
            gbox.click()
            g_path = f'//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[1]/div[3]/div/div/div/div[2]/ul/li[{i}]'
            g = driver.find_element(By.XPATH, g_path)
            g.click()

            time.sleep(1)

            # 현재 페이지 파싱
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 항공권 정보 긁어오기
            ticket_box = soup.select('ul.Rk10dc')
            tickets = ticket_box[0].select('li>div>div.yR1fYc>div>div:nth-of-type(2)')
            tickets.extend(ticket_box[1].select('li>div>div.yR1fYc>div>div:nth-of-type(2)'))

            # 좌석 등급
            grade = soup.select_one('span#i19').text
            # 날짜
            day = f'9월 {d}일 ({week[j]})'

            tckt = [day, grade]

            for one in tickets:
                for info in one.select('span, div'):
                    if info.text == '':
                        pass
                    elif info.text in tckt:
                        pass
                    else:
                        tckt.append(info.text)

                    if info.get('aria-label') is not None and info.get('aria-label').startswith('기착'):
                        tckt.append(info.get('aria-label'))
                data.append(tckt)
                tckt = [day, grade]

            time.sleep(1)


        # 날짜 바꾸기
        nd_path = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[3]'
        next_day = driver.find_element(By.XPATH, nd_path)
        next_day.click()
        
        d += 1
        j += 1

        if j > 6: j = 0

        time.sleep(1)

    driver.quit()

    return data


def clean_data(crawling_data):
    one_t = []
    data_li = []

    for i in crawling_data:
        one_t.append(i[0][:-4])  # 출발 날짜
        one_t.append(i[0][-2:-1])  # 출발 요일
        one_t.append(i[5])  # 출발 시간
        one_t.append(i[1])  # 좌석 등급

        arrival = i[10].split(' ')  # 도착 정보
        one_t.append(arrival[0] + ' ' + arrival[1])  # 도착 날짜
        one_t.append(arrival[2][1:-2])  # 도착 요일
        one_t.append(arrival[3] + ' ' + arrival[4])  # 도착 시간

        for j in i:
            if j.startswith('경유') and len(j)==5:
                one_t.append(j[-2])  # 경유 횟수
            elif j.startswith('직항'):
                one_t.append(0)  # 직항
            elif j.startswith('₩'):
                one_t.append(j[1:])  # 가격
            elif j[:2].isdigit() and (j.endswith('분') or j.endswith('시간')):
                one_t.append(j)  # 소요 시간

        # 항공사
        if i[11].startswith('함께'):
            one_t.append(i[15])
        else:
            one_t.append(i[11])

        for j in i:
            if (re.match("^[a-zA-Z]+.*", j) and len(j) == 3):
                if j in ['GMP','ICN','LAX','HUR']:
                    one_t.append(j)# 출발.도착 공항
                else:
                    pass
            # elif (re.match("^[a-zA-Z]+.*", j) and j.endswith('환승')):
            #     one_t.append(f'환승 도착 {j[:3]}')# 환승 도착 공항
            #     one_t.append(f'환승 출발 {j[6:9]}')# 환승 출발 공항

        # for j in i:
        #     if j.startswith('기착'):
        #         j = j.split('. ')
        #         for k in j:
        #             if k.startswith('기착'):
        #                 numbers = re.findall(r'[0-9]{1,2}',k[12:])
        #                 if len(numbers) == 1:
        #                     one_t.append(f"{numbers[0]}:00")  # 기착 시간(시간)
        #                 elif len(numbers) == 2:
        #                     one_t.append(f"{numbers[0]}:{numbers[1]}")  # 기착 시간(시간+분)

        data_li.append(one_t)
        one_t = []

    return data_li

def save_csv(clean_data_result):
    columns = ['departure_date','departure_day','departure_time','class','arrival_date','arrival_day','arrival_time','flight_time','flight_type','price','airlines','port_d','port_a']
    df = pd.DataFrame(clean_data_result, columns=columns)

        # 출발 날짜 형식 09-01 형태로 바꿔주기
    for i in range(len(df['departure_date'])):
        if len(df['departure_date'][i]) == 5:
            month = int(df['departure_date'][i][0])
            day = int(df['departure_date'][i][3])
        else:
            month = int(df['departure_date'][i][0])
            day = int(df['departure_date'][i][3:5])

        df['departure_date'][i] = f"{month:02}-{day:02}"

    # 도착 날짜 형식 09-01 형태로 바꿔주기
    for i in range(len(df['arrival_date'])):
        if len(df['arrival_date'][i]) == 5:   # 9월 3일
            month = int(df['arrival_date'][i][0])
            day = int(df['arrival_date'][i][3])
        elif len(df['arrival_date'][i]) == 6 and df['arrival_date'][i][1].isdigit():  # 10월 1일
            month = int(df['arrival_date'][i][:2])
            day = int(df['arrival_date'][i][4])
        else:  # 9월 30일
            month = int(df['arrival_date'][i][0])
            day = int(df['arrival_date'][i][3:5])

        df['arrival_date'][i] = f"{month:02}-{day:02}"

    # 소요 시간 형식 00:00 형태로 바꿔주기
    for i in range(len(df['flight_time'])):
        if len(df['flight_time'][i]) == 4:
            hour = int(df['flight_time'][i][0:2])
        elif len(df['flight_time'][i]) == 7:
            hour = int(df['flight_time'][i][0:2])
            minutes = int(df['flight_time'][i][5])
        else:
            hour = int(df['flight_time'][i][0:2])
            minutes = int(df['flight_time'][i][5:7])

        df['flight_time'][i] = f"{hour:02}:{minutes:02}"

    df.to_csv("LAtoKR.csv", index=False)




# 페이지 설정, 원하는 일수 설정
lakr_url = 'https://www.google.com/travel/flights/search?tfs=CBwQAhoqEgoyMDIzLTA5LTAxag4IAxIKL20vMDMwcWIzdHIMCAMSCC9tLzBoc3FmQAFIAXABggELCP___________wGYAQI&tfu=EgYIARABGAA'

# 데이터 가져오기
crawling_data = get_data(lakr_url,30)
# 데이터 리스트 형태로 정리
clean_data_result = clean_data(crawling_data)
# csv로 데이터 저장
save_csv(clean_data_result)