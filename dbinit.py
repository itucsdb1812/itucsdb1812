import os
import sys
import psycopg2 as dbapi2



INIT_STATEMENTS = [
            
     """CREATE TABLE IF NOT EXISTS USERS (
        ID         SERIAL PRIMARY KEY,
        EMAIL          VARCHAR(100),
        USERNAME       VARCHAR(100),
        PASSWORD       VARCHAR(100)       
    )""",

    """
    CREATE TABLE IF NOT EXISTS USERPLAYLIST (
        PLAYLIST_ID    SERIAL PRIMARY KEY,
        PLAYLISTNAME   VARCHAR(50),
        USERID         INTEGER REFERENCES USERS (ID)
    )  """,

    """         
    CREATE TABLE IF NOT EXISTS MUSIC (
        MUSIC_ID         SERIAL PRIMARY KEY,
        MUSICNAME        VARCHAR(50),
        ARTIST           VARCHAR(50),
        MUSICTYPE        VARCHAR(50),
        RELEASEDATE      VARCHAR(50),
        ALBUMNAME        VARCHAR(50),
        MUSICLANGUAGE    VARCHAR(50),
        MUSICCOUNTRY     VARCHAR(50)
    )  """,

        """         
    CREATE TABLE IF NOT EXISTS PLAYLISTMUSIC (
        ID               SERIAL PRIMARY KEY,
        USERPLAYLISTID   INTEGER REFERENCES USERPLAYLIST (PLAYLIST_ID),
        MUSICID          INTEGER REFERENCES MUSIC (MUSIC_ID)
    )  """,     
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
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
