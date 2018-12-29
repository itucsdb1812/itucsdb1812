.. include:: <isonum.txt>
.. role:: sql(code)
   :language: sql
   :class: highlight

Parts Implemented by Enes Boynukalın
=====================================

**Tables**
***********

Users Table
------------

This table holds a users information when they register to the site.


Attributes of Users Table
^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`UserID`
    - :sql:`SERIAL PRIMARY KEY`
    - *Explanation:* Primary key of the :sql:`USERS` table.
* :sql:`EMAIL`  
    - *Type:* :sql:`VARCHAR(100)`
    - *Constraint:* :sql:`UNIQUE`
    - *Explanation:* Email of the user.
* :sql:`USERNAME`
    - *Type:* :sql:`VARCHAR(100)`
    - *Constraint:* :sql:`UNIQUE`
    - *Explanation:* Username of the user.
* :sql:`PASSWORD`
    - *Type:* :sql:`VARCHAR(100)`
    - *Explanation:* Password of the user.


Initialization of Users Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: sql
 

 INIT_STATEMENTS = [

    """CREATE TABLE IF NOT EXISTS USERS (
       ID         SERIAL PRIMARY KEY,
       EMAIL          VARCHAR(100) UNIQUE,
       USERNAME       VARCHAR(100) UNIQUE,
       PASSWORD       VARCHAR(100)       
   )"""




Music Table
------------

This table holds the various information relating to a music.

Attributes of Music Table
^^^^^^^^^^^^^^^^^^^^^^^^^^


* :sql:`MUSIC_ID`
    - *Type:* :sql:`SERIAL PRIMARY KEY`
    - *Explanation:* Primary key of the :sql:`MUSIC` table.
* :sql:`MUSICNAME`  
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Name of the music.
* :sql:`ARTIST`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Artist of the music.
* :sql:`MUSICTYPE`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Type of the music.
* :sql:`RELEASEDATE`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Release date of the music.
* :sql:`ALBUMNAME`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Album name of the music.
* :sql:`MUSICLANGUAGE`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Language of the music.
* :sql:`MUSICCOUNTRY`
    - *Type:* :sql:`VARCHAR(50)`
    - *Explanation:* Country where the music is from.
* :sql:`UNIQUE (MUSICNAME, ARTIST, ALBUMNAME)`
	- *Constraint:* :sql:`UNIQUE`
	- *Explanation:* These three attributes are unique in combination because
	  they can not all be the same for different rows in the database.

Initialization of Music Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: sql

    """         
    CREATE TABLE IF NOT EXISTS MUSIC (
        MUSIC_ID         SERIAL PRIMARY KEY,
        MUSICNAME        VARCHAR(50),
        ARTIST           VARCHAR(50),
        MUSICTYPE        VARCHAR(50),
        RELEASEDATE      VARCHAR(50),
        ALBUMNAME        VARCHAR(50),
        MUSICLANGUAGE    VARCHAR(50),
        MUSICCOUNTRY     VARCHAR(50),
        UNIQUE (MUSICNAME, ARTIST, ALBUMNAME)
    )  """


**Functions Implementation**
******************************


Add Music to the database
-----------------------------------------

This function deals with  the adding music process, however only the admins are allowed. It is not allowed to add the same ``MusicName``, ``Artist`` and ``Albumname`` for a music.

.. code-block:: python

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

A class was created using the ``wtforms`` library. The fields in the music table were defined as fields of the object and validators were used. Validators allow error checking for wrong character inputs as well as the maximum and minimum number of characters.

Next the database connection is activated. If no page is processed with ``POST`` method, the ``html`` page is set the usual way. However, when we fill in the required fields and press the Add button, the ``POST`` method is activated. And the addition is done.

The ``user input`` from the ``html`` is taken and given to certain variables, then checked whether such a music has already been added. If already added, the flash message will show an error. If there is no duplicate data already, :sql:`INSERT` query is done successfully and the music is added to the table. If a non-admin attempts to enter the add music page with the ``GET`` method, an error message that they should be admin to the user is displayed.



Delete Music from the database
-----------------------------------------
Deletes the desired music from the table. This authorization is defined only for the ``admins``.

.. code-block:: python

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

In the ``html`` page, when the delete button is clicked by the ``admin``, the id is sent to this function and the deletion is done by the :sql:`DELETE` query.


Search or list the whole music database
-----------------------------------------

Music can be listed according to the desired search query. Detailed search is possible for the following attributes:

* ``Music Name``
* ``Artist``
* ``Type``
* ``Release Date``
* ``Album name``
* ``Language``
* ``Country``


.. code-block:: python

	class SearchForm(Form):
	    choices = [('musicname','Music Name'),('artist','Artist'),('musictype','Type'),('releasedate','Date'),
	               ('albumname','Album'),('musiclanguage','Language'),('musiccountry','Country')]
	    select = SelectField('',choices=choices)
	    search = StringField('')


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
	            cursor.execute("""SELECT * FROM music WHERE """ + selecting + """ iLIKE '""" + searchtext + """%'""")
	            getmusics = cursor.fetchall()
	            session['getmusics'] = getmusics
	            cursor.close()
	    cursor.close()
	    return render_template("musics.html",form=search)

In this function, music is listed and searched as requested. In this function we used a class which contains a listbox and a textbox. The selected field in the listbox and the string in the textbox are taken and when the search is submitted using the ``POST`` method, the :sql:`SELECT` query performs the actual search operation.


User login
-----------------------------------------

Standard login process is done. If you have already registered to the site you can log in otherwise it will give an error.


.. code-block:: python

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

It takes the string values entered in the input fields on the html page and the username is searched in the USERS table and password checked. If the password matches the ``session->loggid_in`` becomes ``True``, ``session->username`` and ``session->userid`` are synchronized to the id of the logged-in user. If the person trying to log in incorrectly enters the username or password field, he or she will receive a flash error message and will not be able to log in.



User logout
-----------------------------------------

Standard logout process is done.

.. code-block:: python

	@app.route("/logout",methods=["POST","GET"])
	def logout():
	    session.clear()
	    return redirect(url_for("index"))

When the user clicks on logout, the session object is cleared.


User Register
-----------------------------------------
If the user is not a member of the site, he / she cannot login and benefit from many things (play music, create playlists etc.). Therefore they should be registered. It is the process of becoming a standard member.

.. code-block:: python

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

Again a class was created using the ``wtforms`` library. ``Validator`` checks were performed. Records of the entered username and email are checked. If there is, an error that a user exits with these credentials is given and the user is asked to retry the registration with an unused email and username. If there is no problem with the :sql:`INSERT` query, the user is added to the table and forwarded to the login screen.


User change password
-----------------------------------------

After logging in, users can click on their name to go to their profile page and change some information. One of them is the password field. Once the user has entered the old password, he / she can write the new password 2 times and change the password.


.. code-block:: python

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

The fields that the user enters are passed to variables when ``POST`` method is executed, (when the sumbit button is pressed). Validity checks are made from the table through these variables. The username of the logged-in user is kept in the ``session->username``, and the :sql:`SELECT` query finds this user. When the password field from the table is checked and matched with the ``oldpassword field``, the ``new password`` fields are checked and if they match the :sql:`UPDATE` query will update the user's password.


User change email address
-----------------------------------------

It works similarly to the change password function, but it is enough to enter only new E-mails. New email is entered 2 times only to prevent it from entering wrong and e-mail is changed.

.. code-block:: python

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


When the ``POST`` method is executed, the values entered into the field are passed to the variables if they satisfy the validator conditions. If the entered e-mails are not the same, it gives an error. However, if they match, the current e-mail address of the user is replaced by the :sql:`UPDATE` query.

