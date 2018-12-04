from flask import Flask, render_template
# from database import Database
from database import musicdb

app = Flask(__name__)


@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/music",methods=["POST","GET"])
def musics():
    connection = dbapi2.connect(self.url)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM music")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics
    cursor.close()
    return render_template("musics.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
