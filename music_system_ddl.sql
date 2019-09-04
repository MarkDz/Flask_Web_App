/*

Author      : Mark Dziwirek
Email       : marekdz@gmail.com
Date        : 2018-3-10

Description : Flask Webb App

  SQlite Database DDL DB Creation Script 

*/

/**************************************************************************************************/

CREATE TABLE IF NOT EXISTS tbl_users (
  user_id                  INTEGER PRIMARY KEY,
  user_name                VARCHAR (100),
  user_pwd                 VARCHAR (128),
  user_since               DATE,
  notes                    TEXT,
  ctime                    BIGINT,
  mtime                    BIGINT   
);

CREATE TRIGGER insert_tbl_users 
  AFTER INSERT
    ON tbl_users
  BEGIN
    UPDATE tbl_users
       SET ctime = strftime('%s', 'now') 
     WHERE (rowid = NEW.rowid AND  ctime IS NULL);
  END;

CREATE TRIGGER update_tbl_users
  AFTER UPDATE OF user_pwd, user_since, notes 
    ON tbl_users
    FOR EACH ROW
  BEGIN
    UPDATE tbl_users
       SET mtime = strftime('%s', 'now') 
     WHERE rowid = NEW.rowid;
  END;

/* We now add the admin account to our database. Passwords are hashes of SHA512 */
INSERT INTO tbl_users (user_name, user_pwd) VALUES ('admin', 'b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86');

/**************************************************************************************************/
  
CREATE TABLE IF NOT EXISTS tbl_artists (
  artist_id                INTEGER PRIMARY KEY,
  artist_name              VARCHAR (100),
  notes                    TEXT,
  ctime                    BIGINT,
  mtime                    BIGINT  
);
  
CREATE TRIGGER insert_tbl_artists
  AFTER INSERT
    ON tbl_artists
  BEGIN
    UPDATE tbl_artists
       SET ctime = strftime('%s', 'now') 
     WHERE (rowid = NEW.rowid AND  ctime IS NULL);
  END;

CREATE TRIGGER update_tbl_artists
  AFTER UPDATE OF artist_name, notes 
    ON tbl_artists
    FOR EACH ROW
  BEGIN
    UPDATE tbl_artists
       SET mtime = strftime('%s', 'now') 
     WHERE rowid = NEW.rowid;
  END;

INSERT INTO tbl_artists (artist_id, artist_name) VALUES 
  (  1, 'Van Halen'); 

/**************************************************************************************************/
  
CREATE TABLE IF NOT EXISTS tbl_albums (
  artist_id                INTEGER,
  album_id                 INTEGER PRIMARY KEY,
  album_name               VARCHAR (100),
  album_poster             TEXT,
  album_release_year       INTEGER,
  music_genre              VARCHAR(50),
  notes                    TEXT,
  ctime                    BIGINT,
  mtime                    BIGINT  
);  
  
CREATE TRIGGER insert_tbl_albums
  AFTER INSERT
    ON tbl_albums
  BEGIN
    UPDATE tbl_albums
       SET ctime = strftime('%s', 'now') 
     WHERE (rowid = NEW.rowid AND  ctime IS NULL);
  END;

CREATE TRIGGER update_tbl_albums
  AFTER UPDATE OF album_name, album_poster, album_release_year, music_genre, notes 
    ON tbl_albums
    FOR EACH ROW
  BEGIN
    UPDATE tbl_albums
       SET mtime = strftime('%s', 'now') 
     WHERE rowid = NEW.rowid;
  END;
  
INSERT INTO tbl_albums (artist_id, album_id, album_name, album_poster, album_release_year, music_genre) VALUES 
  ( 1, 1, 'Van Halen', 'Van_Halen_-_Van_Halen_(Front).jpg', '1978', 'Rock'),
  ( 1, 2, '1984', 'Van_Halen_-_1984_(Front).jpg', '1978', 'Rock');

/**************************************************************************************************/
  
  
CREATE TABLE IF NOT EXISTS tbl_tracks (
  album_id                 INTEGER,
  track_id                 INTEGER PRIMARY KEY,
  track_number             INTEGER,
  track_name               VARCHAR(100),
  track_length_sec         INTEGER,
  file_name                VARCHAR(250),
  notes                    TEXT,
  ctime                    BIGINT,
  mtime                    BIGINT  
);

CREATE TRIGGER insert_tbl_tracks
  AFTER INSERT
    ON tbl_tracks
  BEGIN
    UPDATE tbl_tracks
       SET ctime = strftime('%s', 'now') 
     WHERE (rowid = NEW.rowid AND  ctime IS NULL);
  END;

CREATE TRIGGER update_tbl_tracks
  AFTER UPDATE OF track_number, track_name,  notes 
    ON tbl_tracks
    FOR EACH ROW
  BEGIN
    UPDATE tbl_tracks
       SET mtime = strftime('%s', 'now') 
     WHERE rowid = NEW.rowid;
  END;

INSERT INTO tbl_tracks (album_id, track_id, track_number, track_name, file_name) VALUES
  (1,  1,  1, 'Runnin'' With The Devil', 'Van Halen - Van Halen - 01 - Runnin'' With The Devil.mp3'),
  (1,  2,  2, 'Eruption', 'Van Halen - Van Halen - 02 - Eruption.mp3'),
  (1,  3,  3, 'You Really Got Me', 'Van Halen - Van Halen - 03 - You Really Got Me.mp3'),
  (1,  4,  4, 'Ain''t Talkin'' ''Bout Love', 'Van Halen - Van Halen - 04 - Ain''t Talkin'' ''Bout Love.mp3'),
  (1,  5,  5, 'I''m The One', 'Van Halen - Van Halen - 05 - I''m The One.mp3'),
  (1,  6,  6, 'Jamie''s Cryin''', 'Van Halen - Van Halen - 06 - Jamie''s Cryin''.mp3'),
  (1,  7,  7, 'Atomic Punk', 'Van Halen - Van Halen - 07 - Atomic Punk.mp3'),
  (1,  8,  8, 'Feel Your Love Tonight', 'Van Halen - Van Halen - 08 - Feel Your Love Tonight.mp3'),
  (1,  9,  9, 'Little Dreamer', 'Van Halen - Van Halen - 09 - Little Dreamer.mp3'),
  (1, 10, 10, 'Ice Cream Man', 'Van Halen - Van Halen - 09 - Ice Cream Man.mp3'),
  (1, 11, 11, 'On Fire', 'Van Halen - Van Halen - 11 - On Fire.mp3'),

  (2, 12,  1, '1984', 'Van Halen - 1984 - 01 - 1984.mp3'),
  (2, 13,  2, 'Jump', 'Van Halen - 1984 - 02 - Jump.mp3'),
  (2, 14,  3, 'Panama', 'Van Halen - 1984 - 03 - Panama.mp3'),
  (2, 15,  4, 'Top Jimmy', 'Van Halen - 1984 - 04 - Top Jimmy.mp3'),
  (2, 16,  5, 'Drop Dead Legs', 'Van Halen - 1984 - 05 - Drop Dead Legs.mp3'),
  (2, 17,  6, 'Hot For Teacher', 'Van Halen - 1984 - 06 - Hot For Teacher.mp3'),
  (2, 18,  7, 'I''ll Wait', 'Van Halen - 1984 - 07 - I''ll Wait.mp3'),
  (2, 19,  8, 'Girl Gone Bad', 'Van Halen - 1984 - 08 - Girl Gone Bad.mp3'),
  (2, 20,  9, 'House Of Pain', 'Van Halen - 1984 - 09 - House Of Pain.mp3');
  
/**************************************************************************************************/

CREATE TABLE IF NOT EXISTS tbl_user_playlists (
  user_id                  INTEGER,
  playlist_id              INTEGER PRIMARY KEY,
  playlist_name            VARCHAR(100),
  notes                    TEXT,
  ctime                    BIGINT,
  mtime                    BIGINT  
);

CREATE TRIGGER insert_tbl_user_playlists
  AFTER INSERT
    ON tbl_user_playlists
  BEGIN
    UPDATE tbl_user_playlists
       SET ctime = strftime('%s', 'now') 
     WHERE (rowid = NEW.rowid AND  ctime IS NULL);
  END;

CREATE TRIGGER update_tbl_user_playlists
  AFTER UPDATE OF playlist_name,  notes 
    ON tbl_user_playlists
    FOR EACH ROW
  BEGIN
    UPDATE tbl_user_playlists
       SET mtime = strftime('%s', 'now') 
     WHERE rowid = NEW.rowid;
  END;


INSERT INTO tbl_user_playlists (user_id, playlist_id, playlist_name) VALUES
  (1, 1, 'Van Halen Mix');


CREATE TABLE IF NOT EXISTS tbl_user_playlists_tracks (
  playlist_id              INTEGER,
  track_id                 INTEGER,
  order_number             INTEGER
);

INSERT INTO tbl_user_playlists_tracks (playlist_id, track_id, order_number) VALUES
  (1, 1, 1),
  (1, 2, 2),
  (1, 3, 3),
  (1, 12, 4),
  (1, 13, 5),
  (1, 14, 6),
  (1, 17, 7);

/**************************************************************************************************/