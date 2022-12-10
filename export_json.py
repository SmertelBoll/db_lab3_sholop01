import json
import psycopg2

username = 'sholop01_lab2'
password = '21132113'
database = 'sholop01_lab2_DB'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

data = {}
with conn:
    cur = conn.cursor()

    for table in ('place', 'eurovision', 'artist', 'song'):
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]

        for row in cur:
            rows.append(dict(zip(fields, row)))

        data[table] = rows

with open('all_data.json', 'w') as outf:
    json.dump(data, outf, default=str)
