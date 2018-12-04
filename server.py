from flask import Flask, render_template, url_for, redirect, request, session
# from database import Database
from database import musicdb
from tables import Music
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import psycopg2 as dbapi2


app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/",methods=["POST","GET"])
def index():
    return render_template("index.html")

# MUSIC HTML
@app.route("/music",methods=["POST","GET"])
def musics():
    connection = dbapi2.connect(self.url)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM music")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics
    cursor.close()
    return render_template("musics.html")


@app.route("/addmusic",methods=["POST","GET"])
def addmusictolist():
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
