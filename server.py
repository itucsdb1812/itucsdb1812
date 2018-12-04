from flask import Flask, render_template, url_for, redirect, request, session
import psycopg2 as dbapi2


app = Flask(__name__)
app.secret_key = "super secret key"

# INDEX
@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

# MUSIC HTML
@app.route("/music",methods=["POST","GET"])
def musics():
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM music")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics
    cursor.close()
    return render_template("musics.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
