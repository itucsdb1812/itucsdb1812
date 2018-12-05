from flask import Flask, render_template, url_for, redirect, request, session
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import psycopg2 as dbapi2


app = Flask(__name__)
app.secret_key = "super secret key"

url = """user='aqclrrxqvuskdd' password='c6b8d1b121bfae6deb78546f2e0423cb2628f56c5cafee6c3fbfc00959622f10'
         host='ec2-54-246-117-62.eu-west-1.compute.amazonaws.com' port=5432 dbname='d80l7qfpjcdsh0'"""

# INDEX
@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])

# MUSIC HTML
@app.route("/music",methods=["POST","GET"])
def musics():
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM music""")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics
    cursor.close()
    return render_template("musics.html")

# REGISTER -------------

class RegisterForm(Form):
    username = StringField('', [validators.Length(min=4, max=25)])
    email = StringField('', [validators.Length(min=4, max=50)])
    password = PasswordField('', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords dont match')
    ])
    confirm = PasswordField('')

@app.route("/register",methods=["POST","GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email=form.email.data
        username = form.username.data
        password = form.password.data
        #aynı username var mı yok mu denenecek şimdilik 2 aynı username açabiliyor.

        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO users(email,username,password) VALUES(%s, %s, %s)""",(email,username,password))

        connection.commit()
        cursor.close()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# REGISTER FINAL ----------

# LOGIN
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']

        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        exist = cursor.execute("""SELECT * FROM users WHERE username = %s""", [username])
        row_count = 0
        for row in cursor:
            row_count += 1
        exist = cursor.execute("""SELECT * FROM users WHERE username = %s""", [username])
        if row_count > 0:
            user = cursor.fetchone()
            password = user[3]
            userid = user[0]
            if password == password_form:
                session['logged_in'] = True
                session['username'] = username
                session['userid'] = userid
                return redirect(url_for("profile"))
            else:
                return render_template("login.html")
            cursor.close()
        else:
            return render_template("login.html")

    return render_template("login.html")

# LOGIN FINAL

# PROFILE

class userplaylist(Form):
    listname = StringField('Listname', [validators.Length(min=4, max=50)])

@app.route("/profile", methods=["POST","GET"])
def profile():
    userid = session['userid']
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM userplaylist WHERE userid = %s""", [userid])
    userlists = cursor.fetchall()
    session['userlists'] = userlists

    form = userplaylist(request.form)
    if request.method == 'POST' and form.validate():
        listname = form.listname.data
        connection = dbapi2.connect(url)
        cursor = connection.cursor()

        print(userid)
        cursor.execute("""INSERT INTO userplaylist(playlistname,userid) VALUES(%s, %s)""", (listname, userid))
        connection.commit()
        cursor.close()
        return redirect(url_for("profile"))


    return render_template("profile.html", form=form)


# PROFILE FINAL

# LOGOUT 
@app.route("/logout",methods=["POST","GET"])
def logout():
    session.clear()
    return redirect(url_for("index"))
# LOGOUT FINAL

# ADMIN PAGE
@app.route("/admin",methods=["POST","GET"])
def admin():
    if session['username'] == 'alican' or session['username'] == 'enes':
        return render_template("admin.html")
    return render_template("index.html")

# ADMIN PAGE FINAL

# MYLIST
@app.route("/mylist/<string:id>",methods=["POST","GET"])
def mylist(id):
    print(id)
    session['listid'] = id
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM playlistmusic WHERE userplaylistid = %s""", [id])
    musiclist = cursor.fetchall()

    music = []
    for row in musiclist:
        musicid = row[2]  # musicID
        cursor2 = connection.cursor()
        cursor2.execute("""SELECT * FROM music WHERE music_id = %s""", [musicid])
        music.append(cursor2.fetchone())
        cursor2.close()

    cursor3 = connection.cursor()
    cursor3.execute("""SELECT * FROM userplaylist WHERE playlist_id = %s""",[id])
    listname = cursor3.fetchone()
    session['listname'] = listname[1]
    session['musiclist'] = music
    cursor.close()

    cursor3.close()

    return render_template("mylist.html")

# MYLIST FINAL

# ADD MUSIC BY ADMIN

class MusicForm(Form):
    musicname = StringField('', [validators.Length(min=2, max=50)])
    artist = StringField('', [validators.Length(min=2, max=50)])
    musictype = StringField('', [validators.Length(min=2, max=50)])
    date = StringField('', [validators.Length(min=4, max=10)])
    albumname = StringField('', [validators.Length(min=2, max=50)])
    language = StringField('', [validators.Length(min=2, max=50)])
    country = StringField('', [validators.Length(min=2, max=50)])

@app.route("/addmusic",methods=["POST","GET"])
def addmusic():
    if session['username'] == 'alican' or session['username'] == 'enes':
        form2 = MusicForm(request.form)

        if request.method == 'POST' and form2.validate():
            musicname = form2.musicname.data
            artist = form2.artist.data
            musictype = form2.musictype.data
            date = form2.date.data
            albumname = form2.albumname.data
            language = form2.language.data
            country = form2.country.data

            connection = dbapi2.connect(url)
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO music(musicname,artist,musictype,releasedate,albumname,musiclanguage,musiccountry) VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                (musicname, artist, musictype, date, albumname, language, country))

            connection.commit()
            cursor.close()
            session['ADDED'] = True
            return redirect(url_for('addmusic'))

        return render_template("addmusic.html", form=form2)
    else:
        return render_template("index.html")
# ADD MUSIC BY ADMIN FINAL

# DELETE MUSIC BY ADMIN
@app.route("/deletemusic/<string:musicid>",methods=["POST","GET"])
def deletemusic(musicid):
    if session['username'] == 'alican' or session['username'] == 'enes':
        connection = dbapi2.connect(url)
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM music WHERE music_id = %s""", [musicid])
        connection.commit()
        cursor.close()
        return redirect(url_for("musics"))
    else:
        return render_template("index.html")
# DELETE MUSIC BY ADMIN FINAL

# CHOOSEN LIST 
@app.route("/choosenlist/<string:musicid>/<string:musicname>/<string:musicartist>",methods=["POST","GET"])
def choosenlist(musicid,musicname,musicartist):
    session['musicid'] = musicid
    session['musicname'] = musicname
    session['musicartist'] = musicartist
    return render_template("choosenlist.html")
# CHOOSEN LIST FINAL

# ADD MUSIC TO THE LIST
@app.route("/addmusictothelist/<string:listid>",methods=["POST","GET"])
def addmusictothelist(listid):
    print(session['musicid'])
    print(listid)
    musicid = session['musicid']
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO playlistmusic(userplaylistid,musicid) VALUES(%s, %s)""", (listid,musicid))
    connection.commit()
    cursor.close()
    return mylist(listid)
# ADD MUSIC TO THE LIST FINAL

# REMOVE MUSIC FROM LIST
@app.route("/removemusicfromlist/<string:musicidd>",methods=["POST","GET"])
def removemusicfromlist(musicidd):
    listid = session['listid']
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM playlistmusic WHERE userplaylistid = %s AND musicid = %s """, (listid,musicidd))
    connection.commit()
    cursor.close()
    return mylist(listid)
# REMOVE MUSIC FROM LIST FINAL

# DELETE LIST
@app.route("/deletelist/<string:listid>",methods=["POST","GET"])
def deletelist(listid):
    connection = dbapi2.connect(url)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM userplaylist WHERE playlist_id = %s""", [listid])
    connection.commit()
    cursor.close()
    return redirect(url_for("profile"))
# DELETE LIST FINAL

if __name__ == "__main__":
    app.debug = True
    app.run()
