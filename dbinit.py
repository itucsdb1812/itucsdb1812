import os
import sys
import psycopg2 as dbapi2

INIT_STATEMENTS = [

    """CREATE TABLE IF NOT EXISTS USERS (
       ID         SERIAL PRIMARY KEY,
       EMAIL          VARCHAR(100) UNIQUE,
       USERNAME       VARCHAR(100) UNIQUE,
       PASSWORD       VARCHAR(100)       
   )""",

    """
    CREATE TABLE IF NOT EXISTS USERPLAYLIST (
        PLAYLIST_ID    SERIAL PRIMARY KEY,
        PLAYLISTNAME   VARCHAR(50),
        USERID         INTEGER REFERENCES USERS (ID)
                       ON UPDATE CASCADE
                       ON DELETE CASCADE,
        IS_FAVORITE    VARCHAR(1),
        UNIQUE(PLAYLISTNAME, USERID)
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
        MUSICCOUNTRY     VARCHAR(50),
        UNIQUE (MUSICNAME, ARTIST, ALBUMNAME)
    )  """,

    """         
CREATE TABLE IF NOT EXISTS PLAYLISTMUSIC (
    ID               SERIAL PRIMARY KEY,
    USERPLAYLISTID   INTEGER REFERENCES USERPLAYLIST (PLAYLIST_ID)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
    MUSICID          INTEGER REFERENCES MUSIC (MUSIC_ID)
                     ON UPDATE CASCADE
                     ON DELETE CASCADE,
    UNIQUE(USERPLAYLISTID, MUSICID)                  
)  """,
]


def initialize(config):
    with dbapi2.connect(config) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


def addMusic(musicname, artist, musictype, releasedate, albumname, musiclanguage, musiccountry):
    with dbapi2.connect(config) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO music(MUSICNAME, ARTIST, MUSICTYPE, RELEASEDATE, ALBUMNAME, MUSICLANGUAGE, MUSICCOUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (musicname, artist, musictype, releasedate, albumname, musiclanguage,
             musiccountry))
        cursor.close()



if __name__ == "__main__":
    initialize(config)

    addMusic("Annem", "Zeki Müren", "Türk Sanat Müziği", "1975", "Anne Sevgisi", "Türkçe", "Türkiye")
    addMusic("Smooth Criminal", "Michael Jackson", "Pop", "2012", "Bad 25th Anniversary", "English", "U.S.A.")
    addMusic("Rolling in the Deep", "Adele", "Rock", "2011", "21", "English", "U.K.")
    addMusic("Maeva in Wonderland", "Ibrahim Maalouf", "Jazz", "2011", "Diagnostic", "Instrumental", "France")
    addMusic("Iron", "Woodkid", "Alternative", "2013", "Iron", "English", "France")
    addMusic("Beat It", "Michael Jackson", "Pop", "2012", "Bad 25th Anniversary", "English", "U.S.A.")
    addMusic("Blue Skies", "Frank Sinatra", "Jazz", "1941", "The Essentian Frank Sinatra", "English", "U.S.A.")
    addMusic("The Show Must Go On", "Queen", "Rock", "2011", "2011 Remastered", "English", "U.K.")
    addMusic("Sway", "Dean Martin", "Jazz", "1953", "Brother Pour Thw Wine", "English", "U.S.A.")
    addMusic("Happy", "Pharrell Williams", "Pop", "2013", "Despicable Me 2", "English", "U.S.A.")
    addMusic("More", "Bobby Darin", "Jazz", "1964", "Bobby Darin Love Songs", "English", "U.S.A.")
    addMusic("Coesur Volant", "Zaz", "Jazz", "2011", "Single", "French", "France")
    addMusic("Power", "Marcus Miller", "Jazz", "2001", "M2", "Instrumental", "U.S.A.")
    addMusic("Human", "Rag'n'Bone Man", "Soul", "2017", "Human (Deluxe)", "English", "U.S.A.")
    addMusic("Hajret", "Kusha Doğan", "Blues", "2005", "Wered 2", "Circassian", "Turkey")
    addMusic("Pump It", "Black Eyed Peas", "Pop", "2005", "Monkey Business", "English", "U.S.A.")
    addMusic("The Thrill Is Gone", "B.B. King", "Jazz", "1970", "Deuces Wild", "English", "U.S.A.")
    addMusic("Night And Day", "Frank Sinatra", "Jazz", "1932", "A Swingin' Affair!", "English", "U.S.A.")
    addMusic("At Last", "Etta James", "Jazz", "1960", "The Essentian tta James", "English", "U.S.A.")






