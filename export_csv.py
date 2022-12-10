import psycopg2
import csv

username = 'sholop01_lab2'
password = '21132113'
database = 'sholop01_lab2_DB'

OUTPUT_FILE_T = 'BD_lab3_{}.csv'

TABLES = [
    'place',
    'eurovision',
    'artist',
    'song'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for table_name in TABLES:
        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]
        with open(OUTPUT_FILE_T.format(table_name), 'w', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])