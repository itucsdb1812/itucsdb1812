from flask import Flask, render_template
# from database import Database
from database import musicdb

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

@app.route("/music",methods=["POST","GET"])
def musics():
    getmusics = musicdb.listAllMusic()
    return render_template("musics.html", getmusics=getmusics)


if __name__ == "__main__":
    app.debug = True
    app.run()
