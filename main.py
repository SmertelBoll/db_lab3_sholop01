import psycopg2
import matplotlib.pyplot as plt


username = 'sholop01_lab2'
password = '21132113'
database = 'sholop01_lab2_DB'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW Artist_Points AS
SELECT TRIM(artist_name), artist_points 
FROM artist
ORDER BY artist_points DESC
'''
query_2 = '''
CREATE VIEW Count_Artist_country AS
SELECT TRIM(artist_country), COUNT(artist_country) 
FROM artist
GROUP BY artist_country
ORDER BY COUNT(artist_country) DESC
'''
query_3 = '''
CREATE VIEW Artist_country_Points AS
SELECT TRIM(artist_country), SUM(artist_points)
FROM artist
GROUP BY artist_country
ORDER BY SUM(artist_points) DESC
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur1 = conn.cursor()
    cur1.execute('DROP VIEW IF EXISTS Artist_Points')
    cur1.execute(query_1)
    cur1.execute('SELECT * FROM Artist_Points')
    name = []
    points = []

    for row in cur1:
        name.append(row[0])
        points.append(row[1])

    figure, (bar_ax, pie_ax, bar_bx) = plt.subplots(1, 3, figsize=(12, 8))

    x_range = range(len(name))
    bar = bar_ax.bar(x_range, points, width=0.5)
    bar_ax.set_title('Кількість балів зароблених співаком', size=15)
    # bar_ax.set_xticks(x_range)
    # bar_ax.set_xticklabels(name, fontdict={'rotation': 90, 'size': 0})
    bar_ax.set(ylabel='Бали')


    cur2 = conn.cursor()
    cur2.execute('DROP VIEW IF EXISTS Count_Artist_country')
    cur2.execute(query_2)
    cur2.execute('SELECT * FROM Count_Artist_country')
    country = []
    points = []

    for row in cur2:
        country.append(row[0])
        points.append(row[1])

    pie_ax.pie(points, labels=country, autopct='%1.1f%%', textprops={'fontsize': 8}, rotatelabels=True,)
    pie_ax.set_title('Кількість представників однієї країни')


    cur3 = conn.cursor()
    cur3.execute('DROP VIEW IF EXISTS Artist_country_Points')
    cur3.execute(query_3)
    cur3.execute('SELECT * FROM Artist_country_Points')
    country = []
    all_points = []

    for row in cur3:
        country.append(row[0])
        all_points.append(row[1])

    plt.plot(country, all_points)
    plt.plot(all_points, marker='o')
    plt.title('Сумарна кількість балів по країнам', size=15)
    plt.ylabel('Бали', size=15)
    plt.xticks(rotation=90, size=5)

figure.tight_layout()
plt.show()