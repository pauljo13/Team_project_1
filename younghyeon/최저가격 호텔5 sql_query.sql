SELECT name, price
From accommodation
WHERE check_in_day = '2023-09-23'
 AND location = '로스엔젤레스 다운타운, 로스앤젤레스 (CA) '
 AND score >= '8.5'
ORDER BY price ASC
LIMIT 5;