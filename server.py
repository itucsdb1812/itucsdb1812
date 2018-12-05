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
    cursor.execute("SELECT * FROM music")
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
        exist = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        row_count = 0
        for row in cursor:
            row_count += 1
        exist = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
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


if __name__ == "__main__":
    app.debug = True
    app.run()
