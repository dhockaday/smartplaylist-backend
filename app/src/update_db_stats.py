import os
import sys
from datetime import datetime, timezone

import imports.db as db
from imports.logging import get_logger

log = get_logger(os.path.basename(__file__))
db_connection, cursor = db.init_connection()


def get_track_count():
    cursor.execute("SELECT count(*) as tracks_count FROM tracks")
    return cursor.fetchone()[0]


def get_tracks_updated_at_minmax():
    cursor.execute("SELECT min(updated_at) as min, max(updated_at) as max FROM tracks")
    return cursor.fetchone()


def get_tracks_created_at_minmax():
    cursor.execute("SELECT min(created_at) as min, max(created_at) as max FROM tracks")
    return cursor.fetchone()


def get_tracks_with_audiofeatures_count():
    cursor.execute("SELECT count(*) FROM tracks WHERE energy IS NOT NULL")
    return cursor.fetchone()


def get_album_count():
    cursor.execute("SELECT count(*) FROM albums")
    return cursor.fetchone()


def get_albums_updated_at_minmax():
    cursor.execute("SELECT min(updated_at) as min, max(updated_at) as max FROM albums")
    return cursor.fetchone()


def get_albums_created_at_minmax():
    cursor.execute("SELECT min(created_at) as min, max(created_at) as max FROM albums")
    return cursor.fetchone()


def get_artist_count():
    cursor.execute("SELECT count(*) FROM artists")
    return cursor.fetchone()


def get_artists_updated_at_minmax():
    cursor.execute("SELECT min(updated_at) as min, max(updated_at) as max FROM artists")
    return cursor.fetchone()


def get_artists_created_at_minmax():
    cursor.execute("SELECT min(created_at) as min, max(created_at) as max FROM artists")
    return cursor.fetchone()


def get_artists_album_updated_at_minmax():
    cursor.execute(
        "SELECT min(albums_updated_at) as min, max(albums_updated_at) as max FROM artists"
    )
    return cursor.fetchone()


def main():

    track_count = get_track_count()
    tracks_with_audiofeatures_count = get_tracks_with_audiofeatures_count()
    tracks_updated_at_minmax = get_tracks_updated_at_minmax()
    tracks_created_at_minmax = get_tracks_created_at_minmax()

    album_count = get_album_count()
    albums_updated_at_minmax = get_albums_updated_at_minmax()
    albums_created_at_minmax = get_albums_created_at_minmax()

    artist_count = get_artist_count()
    artists_updated_at_minmax = get_artists_updated_at_minmax()
    artists_created_at_minmax = get_artists_created_at_minmax()
    artists_album_updated_at_minmax = get_artists_album_updated_at_minmax()

    try:
        cursor.execute(
            """INSERT INTO db_stats (
                total_tracks, total_albums, total_artists, tracks_with_audiofeature,
                track_min_updated_at, track_max_updated_at,
                track_min_created_at, track_max_created_at,
                album_min_updated_at, album_max_updated_at,
                album_min_created_at, album_max_created_at,
                artist_min_updated_at, artist_max_updated_at,
                artist_min_created_at, artist_max_created_at,
                artist_albums_updated_at_min, artist_albums_updated_at_max
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (
                track_count,
                album_count,
                artist_count,
                tracks_with_audiofeatures_count,
                tracks_updated_at_minmax[0],
                tracks_updated_at_minmax[1],
                tracks_created_at_minmax[0],
                tracks_created_at_minmax[1],
                albums_updated_at_minmax[0],
                albums_updated_at_minmax[1],
                albums_created_at_minmax[0],
                albums_created_at_minmax[1],
                artists_updated_at_minmax[0],
                artists_updated_at_minmax[1],
                artists_created_at_minmax[0],
                artists_created_at_minmax[1],
                artists_album_updated_at_minmax[0],
                artists_album_updated_at_minmax[1],
            ),
        )

    except Exception as e:
        log.exception("Unhandled exception", exception=e, exc_info=True)
    else:
        log.info(
            "📈 Saved stats",
        )

    db.close_connection(db_connection, cursor)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ## If file exists, delete it ##
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
