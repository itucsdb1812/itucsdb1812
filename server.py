from flask import Flask, render_template, url_for, redirect, request, session, flash
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
import psycopg2 as dbapi2
import os

app = Flask(__name__, static_url_path = "/imgs", static_folder = "imgs")
app.secret_key = "super secret key"

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is not None:
    config = DATABASE_URL
else:
    config = """dbname='postgres' user='postgres' password='1'"""

# INDEX
@app.route("/")
def index():
    return render_template("index.html",methods=["POST","GET"])
# INDEX FINAL

# SEARCH CLASS
class SearchForm(Form):
    choices = [('musicname','Music Name'),('artist','Artist'),('musictype','Type'),('releasedate','Date'),
               ('albumname','Album'),('musiclanguage','Language'),('musiccountry','Country')]
    select = SelectField('',choices=choices)
    search = StringField('')
# SEARCH CLASS FINAL

# MUSIC HTML
@app.route("/music",methods=["POST","GET"])
def musics():
    search = SearchForm(request.form)
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM music""")
    getmusics = cursor.fetchall()
    session['getmusics'] = getmusics

    if request.method == 'POST':
        selecting = search.select.data
        searchtext = search.search.data
        if searchtext== '':
            cursor.execute("""SELECT * FROM music""")
            getmusics = cursor.fetchall()
            session['getmusics'] = getmusics
            cursor.close()
        else:
            cursor.execute("""SELECT * FROM music WHERE """ + selecting + """ LIKE '""" + searchtext + """%'""")
            getmusics = cursor.fetchall()
            session['getmusics'] = getmusics
            cursor.close()
    cursor.close()
    return render_template("musics.html",form=search)
# MUSICS FINAL

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

        connection = dbapi2.connect(config)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE username = %s """,[username])
        if cursor.rowcount > 0:
            flash('Username already exist!','danger')
            return redirect(url_for("register"))
        else:
            cursor.execute("""SELECT * FROM users WHERE email = %s """, [email])
            if cursor.rowcount > 0:
                flash('E-mail already exist!', 'danger')
                cursor.close()
                return redirect(url_for("register"))
            else:
                cursor.execute("""INSERT INTO users(email,username,password) VALUES(%s, %s, %s)""",
                               (email, username, password))
                connection.commit()
                cursor.close()
                flash('You are registered.', 'success')
                return redirect(url_for("login"))

    return render_template("register.html", form=form)


# REGISTER FINAL ----------

# LOGIN
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password_form = request.form['password']

        connection = dbapi2.connect(config)
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
                #
                return redirect(url_for("profile"))
            else:
                flash('Username or Password is incorrect!','danger')
                return render_template("login.html")
            cursor.close()
        else:
            flash('Username or Password is incorrect!', 'danger')
            return render_template("login.html")

    return render_template("login.html")
# LOGIN FINAL

# PROFILE

class userplaylist(Form):
    listname = StringField('Listname', [validators.Length(min=4, max=50)])

@app.route("/profile", methods=["POST","GET"])
def profile():
    userid = session['userid']
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM userplaylist WHERE userid = %s ORDER BY playlist_id""", [userid])
    userlists = cursor.fetchall()
    session['userlists'] = userlists

    form = userplaylist(request.form)
    if request.method == 'POST' and form.validate():
        listname = form.listname.data
        connection = dbapi2.connect(config)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM userplaylist WHERE playlistname = %s""",[listname])
        if cursor.rowcount > 0:
            flash('This list already exists!', 'warning')
        else:
            cursor.execute("""INSERT INTO userplaylist(playlistname,userid,is_favorite) VALUES(%s, %s, %s)""", (listname, userid, '0'))
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
    connection = dbapi2.connect(config)
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
    if (session) and (session['username'] == 'alican' or session['username'] == 'enes'):
        form2 = MusicForm(request.form)

        if request.method == 'POST' and form2.validate():
            musicname = form2.musicname.data
            artist = form2.artist.data
            musictype = form2.musictype.data
            date = form2.date.data
            albumname = form2.albumname.data
            language = form2.language.data
            country = form2.country.data

            connection = dbapi2.connect(config)
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM music WHERE musicname = %s""", [musicname])
            if cursor.rowcount > 0:
                m = cursor.fetchall()
                for row in m:
                    if row[2].lower() == artist.lower():
                        flash('The music is already in the list.','warning')
                        cursor.close()
                        return redirect(url_for('addmusic'))
            else:
                cursor.execute(
                    """INSERT INTO music(musicname,artist,musictype,releasedate,albumname,musiclanguage,musiccountry) VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                    (musicname, artist, musictype, date, albumname, language, country))
                connection.commit()
                cursor.close()
                flash('Music Added to List.', 'success')
                return redirect(url_for('addmusic'))

        return render_template("addmusic.html", form=form2)
    else:
        flash('You are not admin!', 'warning')
        return render_template("index.html")
# ADD MUSIC BY ADMIN FINAL

# DELETE MUSIC BY ADMIN
@app.route("/deletemusic/<string:musicid>",methods=["POST","GET"])
def deletemusic(musicid):
    if session['username'] == 'alican' or session['username'] == 'enes':
        connection = dbapi2.connect(config)
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM music WHERE music_id = %s""", [musicid])
        connection.commit()
        cursor.close()
        flash('Chosen music has been deleted.', 'success')
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
    musicid = session['musicid']
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM playlistmusic WHERE userplaylistid = %s""",[listid])
    if cursor.rowcount > 0:
        m = cursor.fetchall()
        for row in m:
            if row[2] == int(musicid):
                flash('There is already music in the chosen list!','warning')
                cursor.close()
                return choosenlist(musicid,session['musicname'],session['musicartist'])
    cursor.execute("""INSERT INTO playlistmusic(userplaylistid,musicid) VALUES(%s, %s)""", (listid, musicid))
    connection.commit()
    cursor.close()
    flash('Chosen music is added to the list.', 'success')
    return redirect(url_for("mylist",id=listid))
# ADD MUSIC TO THE LIST FINAL

# REMOVE MUSIC FROM LIST
@app.route("/removemusicfromlist/<string:musicidd>",methods=["POST","GET"])
def removemusicfromlist(musicidd):
    listid = session['listid']
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM playlistmusic WHERE userplaylistid = %s AND musicid = %s """, (listid,musicidd))
    connection.commit()
    cursor.close()
    flash('Chosen music has been removed from the list.','success')
    return mylist(listid)
# REMOVE MUSIC FROM LIST FINAL

# DELETE LIST
@app.route("/deletelist/<string:listid>",methods=["POST","GET"])
def deletelist(listid):
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM userplaylist WHERE playlist_id = %s""", [listid])
    connection.commit()
    cursor.close()
    flash('Chosen list has been removed.', 'success')
    return redirect(url_for("profile"))
# DELETE LIST FINAL


# PLAY MUSIC FROM LIST
@app.route("/playmusicfrommylist/<string:playmusicid>/<string:musicname>/<string:artist>",methods=["POST","GET"])
def playmusicfrommylist(playmusicid,musicname,artist):
    session['playmusic'] = True
    session['playmusicid'] = playmusicid
    session['playmusicname'] = musicname
    session['playmusicartist'] = artist
    return redirect(url_for("mylist", id=session['listid']))
# PLAY MUSIC FROM LIST FINAL

# NEXT MUSIC FROM LIST
@app.route("/nextmusic",methods=["POST","GET"])
def nextmusic():
    for x in range(len(session['musiclist'])):
        if session['musiclist'][x][0] == int(session['playmusicid']):
            if x == (len(session['musiclist'])-1):
                session['playmusicid'] = str(session['musiclist'][0][0])
                session['playmusicname'] = session['musiclist'][0][1]
                session['playmusicartist'] = session['musiclist'][0][2]
            else:
                session['playmusicid'] = str(session['musiclist'][x+1][0])
                session['playmusicname'] = session['musiclist'][x+1][1]
                session['playmusicartist'] = session['musiclist'][x+1][2]
            break
    return render_template("mylist.html")
# NEXT MUSIC FROM LIST FINAL

# PLAY MUSIC FROM MUSICS
@app.route("/playmusicfrommusics/<string:playmusicid>/<string:musicname>/<string:artist>",methods=["POST","GET"])
def playmusicfrommusics(playmusicid,musicname,artist):
    session['playmusic'] = True
    session['playmusicid'] = playmusicid
    session['playmusicname'] = musicname
    session['playmusicartist'] = artist
    return redirect(request.referrer)
# PLAY MUSIC FROM MUSICS FINAL


# NEXT MUSIC FROM MUSICS
@app.route("/nextallmusic",methods=["POST","GET"])
def nextallmusic():
    for x in range(len(session['getmusics'])):
        if session['getmusics'][x][0] == int(session['playmusicid']):
            if x == (len(session['getmusics'])-1):
                session['playmusicid'] = str(session['getmusics'][0][0])
                session['playmusicname'] = session['getmusics'][0][1]
                session['playmusicartist'] = session['getmusics'][0][2]
            else:
                session['playmusicid'] = str(session['getmusics'][x+1][0])
                session['playmusicname'] = session['getmusics'][x+1][1]
                session['playmusicartist'] = session['getmusics'][x+1][2]
            break
    return redirect(url_for("musics"))
# NEXT MUSIC FROM MUSICS


# STOP MUSIC
@app.route("/stopmusic",methods=["POST","GET"])
def stopmusic():
    session['playmusic'] = False
    return redirect(request.referrer)
# STOP MUSIC FINAL

# SETTINGS PAGE
@app.route("/settings",methods=["POST","GET"])
def settings():
    return render_template("settings.html")
# SETTINGS PAGE FINAL

# CHANGE PASSWORD
@app.route("/changepassword",methods=["POST","GET"])
def changepassword():
    if request.method == "POST":
        oldpassword = request.form['oldpassword']
        newpasswordfirst = request.form['newpasswordfirst']
        newpasswordsecond = request.form['newpasswordsecond']

        connection = dbapi2.connect(config)
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE username = %s""", [session['username']])
        user = cursor.fetchone()
        if oldpassword != user[3]:
            flash('Old password does not match!', 'danger')
            cursor.close()
            redirect(url_for("changepassword"))
        elif newpasswordfirst != newpasswordsecond:
            flash('New passwords does not match!','danger')
            cursor.close()
            redirect(url_for("changepassword"))
        else:
            cursor.execute("""UPDATE users SET password = '""" + newpasswordfirst + """' WHERE username = '""" + session['username'] + """'""" )
            connection.commit()
            cursor.close()
            flash('Changed Password.', 'success')
            return redirect(url_for("settings"))
    return render_template("changepassword.html")
# CHANGE PASSWORD FINAL

# CHANGE E-MAIL
@app.route("/changeemail",methods=["POST","GET"])
def changeemail():
    if request.method == "POST":
        newemailfirst = request.form['newemailfirst']
        newemailsecond = request.form['newemailsecond']


        if newemailfirst != newemailsecond:
            flash('New E-mail does not match!','danger')
            redirect(url_for("changeemail"))
        else:
            connection = dbapi2.connect(config)
            cursor = connection.cursor()
            cursor.execute("""UPDATE users SET email = '""" + newemailfirst + """' WHERE username = '""" + session['username'] + """'""" )
            connection.commit()
            cursor.close()
            flash('Changed E-mail.', 'success')
            return redirect(url_for("settings"))
    return render_template("changeemail.html")
# CHANGE E-MAIL FINAL


# IS_FAVORITE

@app.route("/is_favorite/<string:listid>",methods=["POST","GET"])
def is_favorite(listid):
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""UPDATE userplaylist SET is_favorite = '1' WHERE playlist_id = '""" + listid + """'""")
    connection.commit()
    cursor.close()
    return redirect(url_for('profile'))

@app.route("/isnot_favorite/<string:listid>",methods=["POST","GET"])
def isnot_favorite(listid):
    connection = dbapi2.connect(config)
    cursor = connection.cursor()
    cursor.execute("""UPDATE userplaylist SET is_favorite = '0' WHERE playlist_id = '""" + listid + """'""")
    connection.commit()
    cursor.close()
    return redirect(url_for('profile'))

# IS_FAVORITE FINAL

if __name__ == "__main__":
    app.debug = True
    app.run()
