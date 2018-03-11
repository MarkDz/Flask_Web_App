#-*- encoding: utf-8 -*-

"""
About :

"""

__author__ = "Mark Dziwirek"
__email__ = "marekdz@gmail.com"
__company__ = ""
__copyright__ = "Copyright (C) 2018 {a}".format(a=__author__)
__credits__ = ""
__license__ = "GPLv3"
__version__ = "1.00"
__lastdate__ = "2018-3-10"

file_change_log = ''' '''

# ----------------------------------------------------------------------------------------------------------------------
#
# Supporting libraries
#

import datetime
import flask
import hashlib
import os
import sqlite3
import sys
import time
import uuid
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

# ----------------------------------------------------------------------------------------------------------------------
#
# Flask initialization
#

app = flask.Flask(__name__)

# Set the flask static folder location
app._static_folder = os.path.dirname(__file__) + '/static'

# Server Side Session Handling
flask_sessions = {}

# ----------------------------------------------------------------------------------------------------------------------
#
# Flask Routes
#

@app.route('/')
def page_Index():

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:
            pass

        else:

            return flask.redirect('/login')

    else:
        return flask.redirect('/login')
    

@app.route('/login', methods=['GET','POST'])
def page_Login():

    if flask.request.method == 'POST':

        # We force the username to lower case....
        user_name = flask.request.form['username'].lower()

        user_pwd = flask.request.form['password']

        user_ip_address = flask.request.remote_addr

        # The password that was supplied in the form, we now hash it to pass to SQL for lookup
        password_hash = hashlib.sha512(user_pwd.encode('utf-8')).hexdigest()

        try:
            sqlite_db_file = 'mplay.db'
            db_conn = sqlite3.connect(sqlite_db_file)

            # This line allows us to reference the field by name, ie..."user_id"...and not the index value of 0
            db_conn.row_factory = sqlite3.Row

            cur = db_conn.cursor()
            cur.execute('''SELECT user_id
                             FROM tbl_users
                            WHERE LOWER(user_name) = ?
                              AND user_pwd = ?;''', (user_name, password_hash))

            user_record = cur.fetchone()
            db_conn.close()

        except sqlite3.Error as e:
            print(e)

        else:
            if user_record is None:
                return flask.redirect(flask.url_for('page_Login'))

            else:
                user_id = user_record['user_id']

                # We are now logged in !
                flask.session['logged_in'] = True

                # Generate a UUID for the session ID
                session_id = str(uuid.uuid4())

                flask_sessions[session_id] = {'User ID': user_id,
                                              'Username': user_name,
                                              'Remote IP': user_ip_address,
                                              'Connected Time': time.time()
                                              }

                # Setup our response to client, with a redirect to home page, using the function name, not route name
                response = flask.make_response(flask.redirect(flask.url_for('page_Playlists')))

                # Set session expiration time...must be delta days not minutes, or the set.cookie fails....!!!!
                expire_date = datetime.datetime.now() + datetime.timedelta(days=1)

                # Set cookie data
                response.set_cookie('Session ID', value=session_id)

                return response

    else:

        if 'Session ID' in flask.request.cookies:

            session_id = flask.request.cookies.get('Session ID')

            remote_ip = flask.request.remote_addr

            if session_id in flask_sessions:

                return flask.redirect('/playlists')

            else:

                return flask.render_template('/login.html')
        return flask.render_template('/login.html')


@app.route('/playlists', methods=['GET'])
def page_Playlists():

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:

            print(session_id)

            user_id = flask_sessions[session_id]['User ID']
            user_name = flask_sessions[session_id]['Username']

            try:
                sqlite_file = 'mplay.db'
                db_conn = sqlite3.connect(sqlite_file)

                # This line allows us to reference the field by name, ie..."user_id"...and not the index value of 0
                db_conn.row_factory = sqlite3.Row

                cur = db_conn.cursor()
                cur.execute('''SELECT playlist_id, playlist_name FROM tbl_user_playlists WHERE user_id = ?;''', (user_id,))
                my_playlists = cur.fetchall()
                db_conn.close()

            except sqlite3.Error as e:
                print(e)

            else:

                # for row in my_playlists:
                #    print(row['playlist_id'], row['playlist_id'])

                return flask.render_template("playlists.html", my_playlists=my_playlists, user=user_name)

        else:

            return flask.redirect('/login')

    else:
        return flask.redirect('/login')


@app.route('/play_music/<playlist_id>', methods=['GET'])
def page_PlayMusic(playlist_id):

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:

            user_id = flask_sessions[session_id]['User ID']

            try:
                sqlite_file = 'mplay.db'
                db_conn = sqlite3.connect(sqlite_file)

                # This line allows us to reference the field by name, ie..."user_id"...and not the index value of 0
                db_conn.row_factory = sqlite3.Row

                cur = db_conn.cursor()
                cur.execute('''SELECT tbl_user_playlists.playlist_name,
                                      tbl_artists.artist_name,
                                      tbl_albums.album_name,
                                      tbl_albums.album_poster,
                                      tbl_tracks.track_name,
                                              tbl_tracks.file_name
                                         FROM tbl_tracks
                                   INNER JOIN tbl_user_playlists_tracks ON tbl_tracks.track_id = tbl_user_playlists_tracks.track_id
                                   INNER JOIN tbl_albums ON tbl_tracks.album_id = tbl_albums.album_id
                                   INNER JOIN tbl_artists ON tbl_albums.artist_id = tbl_artists.artist_id
                                   INNER JOIN tbl_user_playlists ON tbl_user_playlists_tracks.playlist_id = tbl_user_playlists.playlist_id
                                        WHERE tbl_user_playlists_tracks.playlist_id = ?
                                     ORDER BY tbl_user_playlists_tracks.order_number ASC''', (playlist_id,))
                playlist_tracks = cur.fetchall()
                db_conn.close()

            except sqlite3.Error as e:
                print(e)

            else:

                playlist = ''

                playlist_name = ''

                for row in playlist_tracks:
                    playlist += '''
                     {
                            '''

                    artist_name = row['artist_name']
                    album_name = row['album_name']
                    album_poster = row['album_poster']
                    track_name = row['track_name'] + ' - ' + album_name
                    file_name = row['file_name']

                    playlist_name = row['playlist_name']

                    full_file_path = '/static/Music/' + artist_name + '/' + album_name + '/' + file_name

                    album_poster_path = '/static/Music/' + artist_name + '/' + album_name + '/' + album_poster

                    playlist += '''
            	  	   title: "{tn}",
            		   artist: "{an}",
            		   mp3: "{f}",
            		   poster: "{p}"
                       '''.format(tn=track_name,
                                  an=artist_name,
                                  f=full_file_path,
                                  p=album_poster_path
                                  )
                    playlist += '''
                     },
            '''

            return flask.render_template('play_music.html', playlist=playlist, playlist_name=playlist_name)

        else:

            return flask.redirect('/login')

    else:
        return flask.redirect('/login')


@app.route('/add_playlist', methods=['GET', 'POST'])
def page_Add_Playlists():

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:

            if flask.request.method == 'POST':

                playlist_name = flask.request.form['playlist_name']

                user_id = flask.request.form['user_id']

                print(playlist_name, user_id)

                try:
                    sqlite_file = 'mplay.db'
                    db_conn = sqlite3.connect(sqlite_file)

                    with db_conn:
                        cur = db_conn.cursor()
                        cur.execute("INSERT INTO tbl_user_playlists (user_id, playlist_name) VALUES (?, ?);", (user_id, playlist_name))

                    db_conn.close()

                except sqlite3.Error as e:
                    print(e)

                else:
                    return flask.redirect('/playlists')

            else:

                user_id = flask_sessions[session_id]['User ID']

                return flask.render_template('add_playlist.html', user_id=user_id)

        else:

            return flask.redirect('/login')

    else:
        return flask.redirect('/login')


@app.route('/delete_playlist/<playlist_id>', methods=['GET'])
def page_delete_playlist(playlist_id):

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:

            try:
                sqlite_file = 'mplay.db'
                db_conn = sqlite3.connect(sqlite_file)

                with db_conn:
                    cur = db_conn.cursor()
                    cur.execute("DELETE FROM tbl_user_playlists_tracks WHERE playlist_id = ?;", (playlist_id,))
                    cur.execute("DELETE FROM tbl_user_playlists WHERE playlist_id = ?;", (playlist_id))

                db_conn.close()

            except sqlite3.Error as e:
                print(e)

            else:
                return flask.redirect('/playlists')

        else:

            return flask.redirect('/login')

    else:
        return flask.redirect('/login')

# ----------------------------------------------------------------------------------------------------------------------

@app.route('/add_song', methods=['POST'])
def page_Add_Song():

    if flask.request.method == 'POST':

        playlist_id = flask.request.form['playlist_id']
        track_id = flask.request.form['track_id']

        print(playlist_id, track_id)

        try:
            sqlite_file = 'mplay.db'
            db_conn = sqlite3.connect(sqlite_file)

            with db_conn:
                cur = db_conn.cursor()
                cur.execute("INSERT INTO tbl_user_playlists_tracks (playlist_id, track_id) VALUES (?, ?);",
                            (playlist_id, track_id))

            db_conn.close()

        except sqlite3.Error as e:
            print(e)

        else:
            path = '/update_playlist/{id}'.format(id=playlist_id)

            print(path)

            return flask.redirect(path)

@app.route('/update_playlist/<playlist_id>')
def page_Update_Playlists(playlist_id):

    if 'Session ID' in flask.request.cookies:

        session_id = flask.request.cookies.get('Session ID')

        remote_ip = flask.request.remote_addr

        if session_id in flask_sessions:

            sqlite_file = 'mplay.db'
            db_conn = sqlite3.connect(sqlite_file)

            # This line allows us to reference the field by name, ie..."user_id"...and not the index value of 0
            db_conn.row_factory = sqlite3.Row

            cur = db_conn.cursor()
            cur.execute('''SELECT tbl_tracks.track_id,
                                  tbl_artists.artist_name,
                                  tbl_albums.album_name,
                                  tbl_albums.album_poster,
                                  tbl_tracks.track_name,
                                  tbl_tracks.file_name
                             FROM tbl_tracks
                       INNER JOIN tbl_albums ON tbl_tracks.album_id = tbl_albums.album_id
                       INNER JOIN tbl_artists ON tbl_albums.artist_id = tbl_artists.artist_id
                         ORDER BY tbl_albums.album_release_year''')
            system_music = cur.fetchall()
            db_conn.close()

            return flask.render_template('update_playlist.html', system_music=system_music, playlist_id=playlist_id)

        else:
            return flask.redirect('/login')

    else:
        return flask.redirect('/login')

@app.route("/about")
def about():
    return flask.render_template('about.html')


@app.route("/logout")
def logout():

    flask.session['logged_in'] = False

    # Setup our response to client, with a redirect to home page, using the function name, not route name
    response = flask.make_response(flask.redirect(flask.url_for('page_Login')))

    # Set cookie data
    response.set_cookie('Session ID', value='')

    return response


# ----------------------------------------------------------------------------------------------------------------------
#
# Main program
#

if __name__ == "__main__":

    #password = 'password'
    #password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    #print(password_hash)

    app.secret_key = os.urandom(12)

    app.run (debug=True, threaded=True)



