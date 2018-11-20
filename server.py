from flask import Flask, render_template
from database import Database
from tables import Music

app = Flask(__name__)

db=Database()

musicdb=db.music

musicdb.addMusic(Music("Annem","Zeki Müren","Türk Sanat Müziği","1975","Anne Sevgisi","Türkçe","Türkiye"))



@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html",getmusics=getmusics)


if __name__ == "__main__":
    app.run()
