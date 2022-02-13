import os
import spotipy
import imports.broker as broker
import imports.db as db


QUEUE_NAME = "artists"


def main():
    broker_connection, channel = broker.create_channel(QUEUE_NAME)
    db_connection, cursor = db.init_connection()
    sp = spotipy.Spotify(auth=os.environ["SPOTIFY_OAUTH_TOKEN"])

    # Iterate over results to get the full list
    results = sp.current_user_followed_artists(limit=50)
    followed_artists = results["artists"]["items"]
    while results["artists"]["next"]:
        results = sp.next(results["artists"])
        followed_artists.extend(results["artists"]["items"])

    # Iterate over results, save to Postgres, push to Rabbit
    for i, item in enumerate(followed_artists):
        try:
            cursor.execute(
                "INSERT INTO followed_artists (spotify_id, name, popularity, followers, genres, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, now(), now());",
                (
                    item["id"],
                    item["name"],
                    item["popularity"],
                    item["followers"]["total"],
                    " ".join(item["genres"]),
                ),
            )
            channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=item["id"])
            print("Saved ", i, item["name"])
        except Exception as e:
            print("👨🏽‍🎤 skipped ", i, item["name"], e)

    # Clean up and close connections
    broker.close_connection(broker_connection)
    db.close_connection(db_connection, cursor)


if __name__ == "__main__":
    main()
