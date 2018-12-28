.. include:: <isonum.txt>
.. role:: sql(code)
   :language: sql
   :class: highlight



Parts Implemented by Alican Kurt
================================


**Tables**
***********

UserPlaylist Table
-------------------

This table holds a users playlists and a boolean for if the playlist is a favorite one.


Attributes of UserPlaylist Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :sql:`PLAYLIST_ID`
    - :sql:`SERIAL PRIMARY KEY`
    - *Explanation:* Primary key of the :sql:`USERPLAYLIST` table.
* :sql:`USERID`  
    - *Type:* :sql:`FOREIGN KEY`
    - *Explanation:* References Users table (Id)
* :sql:`IS_FAVOURITE`
    - *Type:* :sql:`VARCHAR(1)`
    - *Explanation:* Favourite flag for the users playlists.
* :sql:`UNIQUE(PLAYLISTNAME, USERID)`
	- *Constraint:* :sql:`UNIQUE`
	- *Explanation:* These two attributes are unique in combination because
	  they can not all be the same for different rows in the database.


Initialization of UserPlaylist Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: sql
 

    """
    CREATE TABLE IF NOT EXISTS USERPLAYLIST (
        PLAYLIST_ID    SERIAL PRIMARY KEY,
        PLAYLISTNAME   VARCHAR(50),
        USERID         INTEGER REFERENCES USERS (ID)
                       ON UPDATE CASCADE
                       ON DELETE CASCADE,
        IS_FAVORITE    VARCHAR(1),
        UNIQUE(PLAYLISTNAME, USERID)
    )  """




PlaylistMusic Table
---------------------

This table holds the music information inside a users playlist.

Attributes of PlaylistMusic Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* :sql:`PLAYLISTMUSIC_ID`
    - *Type:* :sql:`SERIAL PRIMARY KEY`
    - *Explanation:* Primary key of the :sql:`PLAYLISTMUSIC` table.
* :sql:`USERPLAYLISTID`  
    - *Type:* :sql:`FOREIGN KEY`
    - *Explanation:* References UserPlaylist table (Playlist_Id).
* :sql:`MUSICID`
    - *Type:* :sql:`FOREIGN KEY`
    - *Explanation:* References Music table (Music_Id).
* :sql:`UNIQUE(USERPLAYLISTID, MUSICID)`
	- *Constraint:* :sql:`UNIQUE`
	- *Explanation:* These two attributes are unique in combination because
	  they can not all be the same for different rows in the database.


Initialization of PlaylistMusic Table
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: sql

	    """         
	CREATE TABLE IF NOT EXISTS PLAYLISTMUSIC (
	    ID               SERIAL PRIMARY KEY,
	    USERPLAYLISTID   INTEGER REFERENCES USERPLAYLIST (PLAYLIST_ID)
	                     ON UPDATE CASCADE
	                     ON DELETE CASCADE,
	    MUSICID          INTEGER REFERENCES MUSIC (MUSIC_ID)
	                     ON UPDATE CASCADE
	                     ON DELETE CASCADE,
	    UNIQUE(USERPLAYLISTID, MUSICID)                  
	)  """


**Functions Implementation**
******************************


User My lists Page
-----------------------------------------

This field displays the user's playlists in my playlists page. It can create a new list and enter them.

.. code-block:: python

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

A class was created using the ``Wtforms module``. From this class only ``listname`` was received. The ``userid`` information is taken from the session variable when the user wants to create a new playlist and that user's entire list is sent to the ``session->userlists`` object. This list is printed out on its corresponding ``html`` page row by row. The ``POST`` method runs when prompted to create a playlist, and the user is prompted to enter a ``listname``. If there is a list with the same name, it gives an error message. At least 4 characters are required. If there is no problem, the list is added to the table with :sql:`INSERT` method and the page is refreshed. The newly added list now appears in the my lists page.


Show Playlist songs
-----------------------------------------

The function used to list the contents of the lists, in other words, the songs in them. Clicking on any list goes to that list.

.. code-block:: python

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


The function used to list the contents of the lists, in other words, the songs in them. Clicking on any list goes to that list.
The ``ID`` of the list is sent to this function. All songs in the list belonging to this ``ID`` are then passed to a variable with the :sql:`SELECT` query. A music array is then created as each music will be sorted. The array is then filled with the for loop. This array is then added to the session and displayed in a table in ``html``.


Choose which PlayList to add the Music to
-------------------------------------------
When a user wants to add a song to the playlist, all Playlists that the user has are shown and asked to select a playlist.

.. code-block:: python

	@app.route("/choosenlist/<string:musicid>/<string:musicname>/<string:musicartist>",methods=["POST","GET"])
	def choosenlist(musicid,musicname,musicartist):
	    if session.get('logged_in') != True:
	        return redirect(url_for("login"))
	    session['musicid'] = musicid
	    session['musicname'] = musicname
	    session['musicartist'] = musicartist
	    return render_template("choosenlist.html")

The ``ID``, ``music name`` and ``artist`` information of the music to be added is sent to the function and this information is stored into the session object. Then, the user is expected to select a list.


Add Music to Playlist
-----------------------------------------

This function works when the user chooses any list from the choose playlists page. If there is not a duplicate of the music to be added to the selected list, it is added without any errors. But if there is already a duplicate, a flash message error is given.


.. code-block:: python

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


The ``ID`` of the music that the user wants to add is taken from ``session->musicid``. With the :sql:`SELECT` query, the selected list is compared to all music in the database. If there's no match, the :sql:`INSERT` query will add the music to the selected list.




Remove Music from Playlist
-----------------------------------------

The person can remove any of the music in his / her own lists.


.. code-block:: python

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


When the remove button is pressed, the ``ID`` of the music in the selected row is taken and the information of that music is deleted with the :sql:`DELETE` query from the playlistmusic table.



Delete Playlist
-----------------------------------------

User can easily delete their own lists by clicking the `delete` button.

.. code-block:: python

	@app.route("/deletelist/<string:listid>",methods=["POST","GET"])
	def deletelist(listid):
	    connection = dbapi2.connect(config)
	    cursor = connection.cursor()
	    cursor.execute("""DELETE FROM userplaylist WHERE playlist_id = %s""", [listid])
	    connection.commit()
	    cursor.close()
	    flash('Chosen list has been removed.', 'success')
	    return redirect(url_for("profile"))


The `ID` of the list that the user wants to delete is sent to the function and then it is deleted from the table with :sql:`DELETE` query. All of the information in that list is deleted from the table when this operation is performed.



Play Music from Playlist
-----------------------------------------

When the play button of the songs in the user playlists is pressed, it performs the task of showing the song playing in the navigation panel on the upper side.


.. code-block:: python


	@app.route("/playmusicfrommylist/<string:playmusicid>/<string:musicname>/<string:artist>",methods=["POST","GET"])
	def playmusicfrommylist(playmusicid,musicname,artist):
	    session['playmusic'] = True
	    session['playmusicid'] = playmusicid
	    session['playmusicname'] = musicname
	    session['playmusicartist'] = artist
	    return redirect(url_for("mylist", id=session['listid']))


When the function is executed by the ``POST`` method, the ``playmusicid``, ``musicname`` and ``artist`` information is sent to the function. These values are assigned to the session object. Navigation shows the song played on the top by taking the information from the session.


Play Music from Music Database
-----------------------------------------

When the play button of the songs in the music database list is pressed, it performs the task of showing the song playing in the navigation.

.. code-block:: python

	@app.route("/playmusicfrommusics/<string:playmusicid>/<string:musicname>/<string:artist>",methods=["POST","GET"])
	def playmusicfrommusics(playmusicid,musicname,artist):
	    if session.get('logged_in') != True:
	        return redirect(url_for("login"))
	    session['playmusic'] = True
	    session['playmusicid'] = playmusicid
	    session['playmusicname'] = musicname
	    session['playmusicartist'] = artist
	    return redirect(request.referrer)

When the function is executed by the ``POST`` method, the ``playmusicid``, ``musicname`` and ``artist`` information is sent to the function. These values are assigned to the session object. Navigation panel shows the song played on the top by taking the information from the session.




Go to next Music while playing from a Playlist
-------------------------------------------------

If a music is playing, a next button appears. Next button will move to the next song according to where it is playing. When a music is played from a playlist in this function, the next song in the list is played with the next button.


.. code-block:: python

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

There is a for loop which has a max iteration of the amount of songs in that playlist. The ``ID`` of the playing song is in that list and plays the next song in the list. If the current song is the last song, the playlist returns to the beginning and plays the first song.


Go to next Music while play from the Database
------------------------------------------------

If a music is playing, a next button appears. Next button will move to the next song according to where it is playing. In this function, the next song in the playlist is played with the next button when a music is played in the music list.

.. code-block:: python

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

There is a for loop which has a max iteration of the amount of songs in the music database. The ``ID`` of the playing song is in that list and plays the next song in the list. If the current song is the last song, the playlist returns to the beginning and plays the first song.

Stop playing Music
-----------------------------------------

Stops the playing song.

.. code-block:: python

	@app.route("/stopmusic",methods=["POST","GET"])
	def stopmusic():
	    session['playmusic'] = False
	    return redirect(request.referrer)

``Session->playmusic`` value is cleared. After this, the song is stopped.


Choose a Playlist as favourite
-----------------------------------------
The users can choose to make a playlist as favorite from their playlists. The selected favorite lists are shown ready for quick access on the left panel.

.. code-block:: python


	@app.route("/is_favorite/<string:listid>",methods=["POST","GET"])
	def is_favorite(listid):
	    connection = dbapi2.connect(config)
	    cursor = connection.cursor()
	    cursor.execute("""UPDATE userplaylist SET is_favorite = '1' WHERE playlist_id = '""" + listid + """'""")
	    connection.commit()
	    cursor.close()
	    return redirect(url_for('profile'))

Clicking on the favorite button next to each list will send the id of that list to this function. And this playlist table is given a 1 (True) value in the ``Is_Favourite`` attribute.


Choose Playlist as not favourite
-----------------------------------------

The user may decide that his favorite playlists are no longer favorites and may want to remove some of the lists from the left panel. This function is activated here and is removed from the favorite lists.

.. code-block:: python


	@app.route("/isnot_favorite/<string:listid>",methods=["POST","GET"])
	def isnot_favorite(listid):
	    connection = dbapi2.connect(config)
	    cursor = connection.cursor()
	    cursor.execute("""UPDATE userplaylist SET is_favorite = '0' WHERE playlist_id = '""" + listid + """'""")
	    connection.commit()
	    cursor.close()
	    return redirect(url_for('profile'))

A list appears green when a favorite is made. And again, when it is not a favorite it returns to the blue state. The ``Is_Favourite`` attribute is returned to the value 0 with the :sql:`UPDATE` query.
