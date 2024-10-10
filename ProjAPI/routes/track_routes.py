from flask import Flask, request, jsonify, Blueprint

track_blueprint = Blueprint('tracks', __name__) #just to tell flask to use the files using Blueprint

# Simulated databases
users = []
playlists = []


# Preloaded list of 10 songs
tracks = [
    {"id": 1, "title": "Karma Police", "artist": "Pierce The Veil", "album": "Karma Police", "genre": "Rock"},
    {"id": 2, "title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "genre": "Rock"},
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