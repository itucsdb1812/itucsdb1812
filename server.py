from flask import Flask, render_template, url_for, redirect, request, session
import psycopg2 as dbapi2


app = Flask(__name__)
app.secret_key = "super secret key"

kekoenes = """user='aqclrrxqvuskdd' password='c6b8d1b121bfae6deb78546f2e0423cb2628f56c5cafee6c3fbfc00959622f10'
         host='ec2-54-246-117-62.eu-west-1.compute.amazonaws.com' port=5432 dbname='d80l7qfpjcdsh0'"""

# INDEX
@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

# MUSIC HTML
@app.route("/music",methods=["POST","GET"])
def musics():
    connection = dbapi2.connect(kekoenes)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM music")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics
    cursor.close()
    return render_template("musics.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
