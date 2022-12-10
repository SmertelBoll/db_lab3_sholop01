import psycopg2
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np


username = 'sholop01_lab2'
password = '21132113'
database = 'sholop01_lab2_DB'
host = 'localhost'
port = '5432'


query_0 = """
DELETE FROM Song;
DELETE FROM Artist;
DELETE FROM Eurovision;
DELETE FROM Place;
"""

query_place = """
INSERT INTO Place(place_id, place_city, place_country) VALUES ('%s', '%s', '%s')
"""

query_eurovision = """
INSERT INTO Eurovision(eurovision_id, eurovision_name, place_id) 
VALUES ('%s', '%s', (SELECT place_id FROM Place WHERE place_city = '%s' AND place_country = '%s'))
"""

query_artist = """
INSERT INTO Artist(artist_id, artist_name, artist_country, artist_points, eurovision_id) 
VALUES ('%s', '%s', '%s', '%s', (SELECT eurovision_id FROM Eurovision WHERE eurovision_name = '%s'))
"""

query_song = """
INSERT INTO Song(song_id, song_name, artist_id)
VALUES ('%s', '%s', (SELECT artist_id FROM Artist WHERE artist_name = '%s'))
"""
#AND Eurovision.eurovision_name = '%s'

data = pd.read_csv(r'eurovision.csv')

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_0)

    cur1 = conn.cursor()
    df_city = pd.DataFrame(data, columns=['host_city'])
    df_country = pd.DataFrame(data, columns=['host_country'])

    unique_city = []
    unique_country = []

    list_city = df_city.values.tolist()
    list_country = df_country.values.tolist()
    for i in range(len(list_city)):
        if list_city[i][0] not in unique_city:
            unique_city.append(*list_city[i])
            unique_country.append(*list_country[i])

    for i in range(len(unique_city)):
        query = query_place % (i, unique_city[i], unique_country[i])
        cur1.execute(query)
    conn.commit()

    cur2 = conn.cursor()
    df = pd.DataFrame(data, columns=['event', 'host_city', 'host_country'])
    eu_name = df['event'].tolist()
    eu_city = df['host_city'].tolist()
    eu_country = df['host_country'].tolist()

    unique_eu_name = []
    unique_eu_city = []
    unique_eu_country = []

    for i in range(len(eu_name)):
        if eu_name[i] not in unique_eu_name:
            unique_eu_name.append(eu_name[i])
            unique_eu_city.append(eu_city[i])
            unique_eu_country.append((eu_country[i]))



    for i in range(len(unique_eu_name)):
        query = query_eurovision % (i, unique_eu_name[i], unique_eu_city[i], unique_eu_country[i])
        cur2.execute(query)

    conn.commit()

    cur3 = conn.cursor()
    df = pd.DataFrame(data, columns=['artist', 'artist_country', 'total_points', 'event'])
    ar_artist = df['artist'].tolist()
    ar_artist_country = df['artist_country'].tolist()
    ar_total_points = df['total_points'].tolist()
    ar_event = df['event'].tolist()

    unique_ar_artist = []
    unique_ar_artist_country = []
    unique_ar_total_points = []
    unique_ar_event = []

    for i in range(len(ar_artist)):
        if ar_artist[i] not in unique_ar_artist:
            unique_ar_artist.append(ar_artist[i])
            unique_ar_artist_country.append(ar_artist_country[i])
            unique_ar_total_points.append(ar_total_points[i])
            unique_ar_event.append(ar_event[i])

    for i in range(len(unique_ar_artist)):
        query = query_artist % (i,
                                unique_ar_artist[i].replace("\'", ''),
                                unique_ar_artist_country[i],
                                0 if np.isnan(unique_ar_total_points[i]) else int(unique_ar_total_points[i]),
                                unique_ar_event[i])
        cur3.execute(query)

    conn.commit()

    cur4 = conn.cursor()
    df = pd.DataFrame(data, columns=['song', 'artist', 'event'])
    sg_song = df['song']
    sg_artist = df['artist']
    sg_event = df['event']

    for i in range(len(sg_song)):
        song_name = str(sg_song[i]).replace("\'", '')
        artist_name = sg_artist[i].replace("\'", '')

        query = query_song % (i, song_name, artist_name)
        cur4.execute(query)

    conn.commit()
