from flask import Flask, render_template
from database import Database
from tables import Music

app = Flask(__name__)

db=Database()

musicdb=db.music

musicdb.addMusic(Music("Annem","Zeki Müren","Türk Sanat Müziği","1975","Anne Sevgisi","Türkçe","Türkiye"))
musicdb.addMusic(Music("asd","asdasd Müren","asdasd Sanat Müziği","2000","asdasd Sevgisi","asdasd","asdasd"))
musicdb.addMusic(Music("qweqwe","Zeki qweqwe","Türk qweqwe Müziği","2005","qweqwe Sevgisi","qweqwe","qweqwe"))




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html",getmusics=getmusics)


if __name__ == "__main__":
    app.run()
