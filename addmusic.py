import psycopg2 as dbapi2

url = """user='aqclrrxqvuskdd' password='c6b8d1b121bfae6deb78546f2e0423cb2628f56c5cafee6c3fbfc00959622f10'
         host='ec2-54-246-117-62.eu-west-1.compute.amazonaws.com' port=5432 dbname='d80l7qfpjcdsh0'"""

def addMusic(musicname, artist, musictype, releasedate, albumname, musiclanguage, musiccountry):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO music(MUSICNAME, ARTIST, MUSICTYPE, RELEASEDATE, ALBUMNAME, MUSICLANGUAGE, MUSICCOUNTRY) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (musicname, artist, musictype, releasedate, albumname, musiclanguage,
             musiccountry))
        cursor.close()

addMusic("Annem","Zeki Müren","Türk Sanat Müziği","1975","Anne Sevgisi","Türkçe","Türkiye")
addMusic("Smooth Criminal","Michael Jackson","Pop","2012","Bad 25th Anniversary","English","U.S.A.")
addMusic("Rolling in the Deep","Adele","Rock","2011","21","English","U.K.")
addMusic("Maeva in Wonderland","Ibrahim Maalouf","Jazz","2011","Diagnostic","Instrumental","France")
addMusic("Iron","Woodkid","Alternative","2013","Iron","English","France")
addMusic("Beat It","Michael Jackson","Pop","2012","Bad 25th Anniversary","English","U.S.A.")
addMusic("Blue Skies","Frank Sinatra","Jazz","1941","The Essentian Frank Sinatra","English","U.S.A.")
addMusic("The Show Must Go On","Queen","Rock","2011","2011 Remastered","English","U.K.")
addMusic("Sway","Dean Martin","Jazz","1953","Brother Pour Thw Wine","English","U.S.A.")
addMusic("Happy","Pharrell Williams","Pop","2013","Despicable Me 2","English","U.S.A.")
addMusic("More","Bobby Darin","Jazz","1964","Bobby Darin Love Songs","English","U.S.A.")
addMusic("Coesur Volant","Zaz","Jazz","2011","Single","French","France")
addMusic("Power","Marcus Miller","Jazz","2001","M2","Instrumental","U.S.A.")
addMusic("Human","Rag'n'Bone Man","Soul","2017","Human (Deluxe)","English","U.S.A.")
addMusic("Hajret","Kusha Doğan","Blues","2005","Wered 2","Circassian","Turkey")
addMusic("Pump It","Black Eyed Peas","Pop","2005","Monkey Business","English","U.S.A.")
addMusic("The Thrill Is Gone","B.B. King","Jazz","1970","Deuces Wild","English","U.S.A.")
addMusic("Night And Day","Frank Sinatra","Jazz","1932","A Swingin' Affair!","English","U.S.A.")
addMusic("At Last","Etta James","Jazz","1960","The Essentian tta James","English","U.S.A.")
