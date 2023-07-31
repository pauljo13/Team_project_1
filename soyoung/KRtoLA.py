from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import copy
import re
import pandas as pd

options = Options()
# options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhoqEgoyMDIzLTA5LTAxagwIAhIIL20vMGhzcWZyDggDEgovbS8wMzBxYjN0QAFIAXABggELCP___________wGYAQI&tfu=EgYIARABGAA&hl=ko')

time.sleep(1)

tckt = []
data = []
week = ['월', '화', '수', '목', '금', '토', '일']
d, j = 1, 4

for _ in range(30):
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

data1 = copy.deepcopy(data)

one_t = []
data_li = []

for i in data1:
    one_t.append(i[0][:-4])  # 출발날짜
    one_t.append(i[0][-2:-1])  # 출발요일
    one_t.append(i[1])  # 좌석등급
    one_t.append(i[5])  # 출발시간
    one_t.append(i[7][-8:])  # 도착시간
    for j in i:
        if j.startswith('경유') and len(j) == 5:
            one_t.append(j)  # 경유 횟수
        elif j.startswith('직항'):
            one_t.append(j)  # 직항
        elif j.startswith('₩'):
            one_t.append(j)  # 가격
        elif j[:2].isdigit() and (j.endswith('분') or j.endswith('시간')):
            one_t.append(j)  # 소요 시간

    # 항공사
    if i[10].startswith('9월') or i[10].startswith('10월'):
        one_t.append(i[11])
    else:
        one_t.append(i[10])

    # 도착날짜
    if i[9].startswith('+'):
        one_t.append(i[10][:6])
    else:
        one_t.append(i[9][:6])

    # 도착요일
    if i[9].startswith('+'):
        one_t.append(i[10][5:10])
    else:
        one_t.append(i[9][5:10])

    for j in i:
        if re.match("^[a-zA-Z]+.*", j) and len(j) == 3:
            one_t.append(j)  # 출발.도착 공항

    data_li.append(one_t)
    one_t = []

columns = ['departuredate','departureday','class','departuretime','arrivaltime', 'flighttime', 'flighttype','price', 'airlines', 'arrivaldate','arrivalday','portd','porta','via1','via2','via3','via4']
df = pd.DataFrame(data_li, columns=columns)
print(df)

# df.to_csv("KRtoLA.csv", index=False)
# pd.read_csv('KRtoLA.csv')