import psycopg2
from xml.etree import ElementTree
import pandas as pd
from tqdm import tqdm

# Database 연결
host = 'stampy.db.elephantsql.com'
user = 'cdoksewy'
password = 'kIxGLNfCDOKwL_AbTNN3ocg-XjpQel_u'
database = 'cdoksewy'

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()


# flights 테이블 생성
cursor.execute("DROP TABLE IF EXISTS flights;")
cursor.execute("""CREATE TABLE flights(
                    Id SERIAL PRIMARY KEY,
                    departure_date DATE,
                    departure_day VARCHAR(12),
                    departure_time TIMESTAMP,
                    class VARCHAR(12),
                    arrival_date DATE,
                    arrival_day VARCHAR(12),
                    arrival_time TIMESTAMP,
                    flight_time INTEGER,
                    flight_type INTEGER,
                    price INTEGER,
                    airlines VARCHAR(130),
                    port_d VARCHAR(12),
                    port_a VARCHAR(12)
                )""")

flights = pd.read_csv('C:/Users/Juyeon/Documents/Project/Team_project_1/junseo/data_storing/flights.csv')
flights = flights.drop('Unnamed: 0', axis=1)
flights = flights.values.tolist()

for values in tqdm(flights):
    cursor.execute("""INSERT INTO flights (departure_date, departure_day, departure_time, class,
                   arrival_date, arrival_day, arrival_time, flight_time, flight_type, price, airlines, port_d, port_a)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    (values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12], values[13]))


# accommodation 테이블 생성
cursor.execute("DROP TABLE IF EXISTS accommodation;")
cursor.execute("""CREATE TABLE accommodation(
                    Id SERIAL PRIMARY KEY,
                    Name VARCHAR(110),
                    location VARCHAR(20),
                    distance_km FLOAT,
                    location_score INTEGER,
                    check_in_day DATE,
                    check_in_week VARCHAR(12),
                    score FLOAT,
                    price INTEGER
                )""")

accommodation = pd.read_csv("C:/Users/Juyeon/Documents/Project/Team_project_1/junseo/data_storing/accommodation.csv")
accommodation = accommodation.drop('Unnamed: 0', axis=1)
accommodation = accommodation.values.tolist()

for values in tqdm(accommodation):
    cursor.execute("""INSERT INTO accommodation (Name, location, distance_km, location_score,
                   check_in_day, check_in_week, score, price)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
    (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]))

connection.commit()

cursor.close()
connection.close()