from flask import Flask, request, jsonify, Blueprint

track_blueprint = Blueprint('tracks', __name__) #just to tell flask to use the files using Blueprint

# Simulated databases
users = []
playlists = []


# Preloaded list of 10 songs
tracks = [
    {"id": 1, "title": "Karma Police", "artist": "Pierce The Veil", "album": "Karma Police", "genre": "Rock", "path": "ProjAPI\music\Karma Police - Pierce The Veil.mp3"},
    {"id": 2, "title": "Blow Out", "artist": "RadioHead", "album": "Pablo Honey", "genre": "Rock", "path": "ProjAPI\music\Blow Out.mp3"},
    {"id": 3, "title": "SOFALOVE", "artist": "Javi Vera", "album": "Junior Varsity", "genre": "Rock", "path": "ProjAPI\music\SOFALOVE.mp3"},
    {"id": 4, "title": "EXCUSEMEMADAME", "artist": "Javi Vera", "album": "Junior Varsity", "genre": "Rock", "path": "ProjAPI\music\EXCUSEMEMADAME.mp3"},
    {"id": 4, "title": "Basement Jack", "artist": "Steve Lacy", "album": "Apollo XXI", "genre": "R&B", "path": ""},
    
    # Add more songs but first figure out how to play them
]


@track_blueprint.route("/get-ALL-tracks", methods=["GET"])
def get_songs():
    return jsonify(tracks), 200

# USER ENDPOINTS / Just learning basics
@track_blueprint.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    user_data = {
        "user_id": user_id,
        "name": "Jorge Doe",
        "email": "email@Example.com" # add more features for a more detailed profile
    }
    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data), 200

#make a new app route for creating users, though idk if i need it atm

# TRACK ENDPOINTS
#Get a single track, if u have the ID
@track_blueprint.route("/get-track/<int:track_id>", methods=["GET"])
def get_track(track_id):
    track = next((track for track in tracks if track["id"] == track_id), None)
    if track:
        return jsonify(track), 200
    else:
        return jsonify({"error": "Track not found"}), 404

@track_blueprint.route("/search-track", methods=["GET"])
def search_song():
    title_query = request.args.get("title", "").lower()  # Get search query and convert to lowercase
    artist_query2 = request.args.get("artist", "").lower()
    album_query3 = request.args.get("album", "").lower()
    # Checking if all queries are empty, return error if nothing is provided
    print(f"Received title_query: '{title_query}', artist_query: '{artist_query2}', album_query: '{album_query3}'")

    if not title_query and not artist_query2 and not album_query3:
        return jsonify({"error": "No search query provided"}), 400

    # Searching for tracks that match any of the queries
    # matching_tracks = [
    #     track for track in tracks
    #     #THESE ARE ALL TRUE?
    #     if (not title_query or title_query in track["title"].lower()) and 
    #        (not artist_query2 or artist_query2 in track["artist"].lower()) and
    #        (not album_query3 or album_query3 in track["album"].lower())
    # ]
    # IFFFF There is no search query for the title (not title_query), then it won't filter by title.
    #  OR, if a title_query is provided, it then checks if the title_query is found within the track's title (title_query in track["title"].lower()).

    #This is a WAY more flexible since it is using OR (will in include stuff, that will even remotley resembles it)
    matching_tracks = [
    track for track in tracks
        if (title_query and title_query in track["title"].lower()) or 
           (artist_query2 and artist_query2 in track["artist"].lower()) or
           (album_query3 and album_query3 in track["album"].lower())
]
    if matching_tracks:
        return jsonify(matching_tracks), 200
    else:
        return jsonify({"error": "No matching songs found"}), 404

@track_blueprint.route("/create-track", methods=["POST"])
def create_track():
    track_data = request.get_json()
    track_data["id"] = len(tracks) + 1
    tracks.append(track_data)
    return jsonify(track_data), 201

# PLAYLIST ENDPOINTS
@track_blueprint.route("/create-playlist", methods=["POST"])
def create_playlist():
    playlist_data = request.get_json()
    playlist_data["id"] = len(playlists) + 1
    playlist_data["tracks"] = []
    playlists.append(playlist_data)
    return jsonify(playlist_data), 201

@track_blueprint.route("/add-track-to-playlist/<int:playlist_id>", methods=["POST"])
def add_track_to_playlist(playlist_id):
    track_data = request.get_json()
    playlist = next((playlist for playlist in playlists if playlist["id"] == playlist_id), None)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    playlist["tracks"].append(track_data)
    return jsonify(playlist), 200

# SEARCH ENDPOINTS
@track_blueprint.route("/search-tracks", methods=["GET"])
def search_tracks():
    query = request.args.get("query")
    matching_tracks = [track for track in tracks if query.lower() in track["title"].lower() or query.lower() in track["artist"].lower()]
    if matching_tracks:
        return jsonify(matching_tracks), 200
    else:
        return jsonify({"error": "No matching tracks found"}), 404