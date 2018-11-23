import os
import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
            "CREATE TABLE USERS (ID SERIAL PRIMARY KEY, USERNAME VARCHAR(30) NOT NULL, PASSWORD VARCHAR(20) NOT NULL)",
            "CREATE TABLE USERPLAYLIST (PLAYLIST_ID SERIAL PRIMARY KEY, PLAYLISTNAME VARCHAR(30) NOT NULL, USERID INTEGER REFERENCES USERS (ID))",        
            "CREATE TABLE MUSIC (MUSIC_ID SERIAL PRIMARY KEY, MUSICNAME VARCHAR(30) NOT NULL, ARTIST VARCHAR(30), MUSICTYPE VARCHAR(20), RELEASEDATE VARCHAR(10), ALBUMNAME VARCHAR(100), MUSICLANGUAGE VARCHAR(30), MUSICCOUNTRY VARCHAR(20) )",
            "CREATE TABLE PLAYLISTMUSIC (ID SERIAL PRIMARY KEY, USERPLAYLISTID INTEGER REFERENCES USERPLAYLIST (PLAYLIST_ID), MUSICID INTEGER REFERENCES MUSIC (MUSIC_ID) )",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py",

file=sys.stderr)
        sys.exit(1)
    initialize(url)

