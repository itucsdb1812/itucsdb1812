import os
import sys
import psycopg2 as dbapi2


INIT_STATEMENTS = [
            "CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(30) NOT NULL, password VARCHAR(20) NOT NULL)",
            "CREATE TABLE userplaylist (playlist_id SERIAL PRIMARY KEY, playlistname VARCHAR(30) NOT NULL, userid INTEGER REFERENCES users (id))",        
            "CREATE TABLE music (music_id SERIAL PRIMARY KEY, musicname VARCHAR(30) NOT NULL, artist VARCHAR(30), musictype VARCHAR(20), releasedate VARCHAR(10), albumname VARCHAR(100), musiclanguage VARCHAR(30), musiccountry VARCHAR(20) )",
            "CREATE TABLE playlistmusic (id SERIAL PRIMARY KEY, userplaylistid INTEGER REFERENCES userplaylist (playlist_id), musicid INTEGER REFERENCES music (music_id) )",
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
