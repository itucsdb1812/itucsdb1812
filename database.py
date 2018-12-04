
from tables import Music
import psycopg2 as dbapi2
import os
import sys

class Database:
    def __init__(self):
        self.music = self.Music()

    class Music:
        def __init__(self):
            self.url = os.getenv("DATABASE_URL")

        def addMusic(self, music):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO MUSIC (MUSICNAME, ARTIST, MUSICTYPE, RELEASEDATE, ALBUMNAME, MUSICLANGUAGE, MUSICCOUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (music.musicname, music.artist, music.musictype, music.releasedate, music.albumname, music.musiclanguage, music.musiccountry))
                cursor.close()



        def listAllMusic(self):
            connection = None
            Musics = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM MUSIC;")
                for music in cursor:
                    getMusic = Music(music[1], music[2], music[3], music[4], music[5], music[6], music[7])
                    Musics.append((music[0], getMusic))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

            return Musics

db=Database()
musicdb=db.music
