SELECT *
FROM 데이터를 저장한 테이블명
WHERE check_in_day = '2023-09-01' 9월1일자 검색
  AND location_score >= 7 위치평점 7이상
  AND score >= 8.5; 평점 8.5이상

SELECT MIN(price) AS min_price  가격 최솟값
FROM 데이터를 저장한 테이블명
WHERE check_in_day >= '2023-09-01' 
  AND location_score >= 7 위치평점 7이상
  AND score >= 8.5; 평점 8.5이상