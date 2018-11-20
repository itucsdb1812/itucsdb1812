from flask import Flask, render_template
from database import Database
from tables import Music

app = Flask(__name__)

db=Database()

musicdb=db.music

musicdb.addMusic(Music("Annem","Zeki Müren","Türk Sanat Müziği","1975","Anne Sevgisi","Türkçe","Türkiye"))
musicdb.addMusic(Music("asd","asdasd Müren","asdasd Sanat Müziği","2000","asdasd Sevgisi","asdasd","asdasd"))
musicdb.addMusic(Music("qweqwe","Zeki qweqwe","Türk qweqwe Müziği","2005","qweqwe Sevgisi","qweqwe","qweqwe"))
musicdb.addMusic(Music("Rolling in the Deep","Adele","Rock","2011","21","English","U.K."))
musicdb.addMusic(Music("Maeva in Wonderland","Ibrahim Maalouf","Jazz","2011","Diagnostic","Instrumental","France"))
musicdb.addMusic(Music("Iron","Woodkid","Alternative","2013","Iron","English","France"))
musicdb.addMusic(Music("Beat It","Michael Jackson","Pop","2012","Bad 25th Anniversary","English","U.S.A."))



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html",getmusics=getmusics)


if __name__ == "__main__":
    app.run()
