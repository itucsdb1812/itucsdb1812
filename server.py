from flask import Flask, render_template
# from database import Database
from database import musicdb

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html", getmusics=getmusics)

@app.route("/addmusic",methods=["POST","GET"])
def addmusictolist():
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
