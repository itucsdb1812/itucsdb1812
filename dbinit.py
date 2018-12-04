import os
import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
            "CREATE TABLE USERS (ID SERIAL PRIMARY KEY,EMAIL VARCHAR(100), USERNAME VARCHAR(100) NOT NULL, PASSWORD VARCHAR(100) NOT NULL)",
            "CREATE TABLE USERPLAYLIST (PLAYLIST_ID SERIAL PRIMARY KEY, PLAYLISTNAME VARCHAR(100) NOT NULL, USERID INTEGER REFERENCES USERS (ID))",
            "CREATE TABLE MUSIC (MUSIC_ID SERIAL PRIMARY KEY, MUSICNAME VARCHAR(100) NOT NULL, ARTIST VARCHAR(100), MUSICTYPE VARCHAR(100), RELEASEDATE VARCHAR(100), ALBUMNAME VARCHAR(100), MUSICLANGUAGE VARCHAR(100), MUSICCOUNTRY VARCHAR(100) )",
            "CREATE TABLE PLAYLISTMUSIC (ID SERIAL PRIMARY KEY, USERPLAYLISTID INTEGER REFERENCES USERPLAYLIST (PLAYLIST_ID), MUSICID INTEGER REFERENCES MUSIC (MUSIC_ID))",
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

