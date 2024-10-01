from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated databases
users = []
tracks = []
playlists = []

# USER ENDPOINTS
@app.route("/get-user/<user_id>", methods=["GET"])
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
@app.route("/get-track/<int:track_id>", methods=["GET"])
def get_track(track_id):
    track = next((track for track in tracks if track["id"] == track_id), None)
    if track:
        return jsonify(track), 200
    else:
        return jsonify({"error": "Track not found"}), 404

@app.route("/create-track", methods=["POST"])
def create_track():
    track_data = request.get_json()
    track_data["id"] = len(tracks) + 1
    tracks.append(track_data)
    return jsonify(track_data), 201

# PLAYLIST ENDPOINTS
@app.route("/create-playlist", methods=["POST"])
def create_playlist():
    playlist_data = request.get_json()
    playlist_data["id"] = len(playlists) + 1
    playlist_data["tracks"] = []
    playlists.append(playlist_data)
    return jsonify(playlist_data), 201

@app.route("/add-track-to-playlist/<int:playlist_id>", methods=["POST"])
def add_track_to_playlist(playlist_id):
    track_data = request.get_json()
    playlist = next((playlist for playlist in playlists if playlist["id"] == playlist_id), None)
    if not playlist:
        return jsonify({"error": "Playlist not found"}), 404
    playlist["tracks"].append(track_data)
    return jsonify(playlist), 200

# SEARCH ENDPOINTS
@app.route("/search-tracks", methods=["GET"])
def search_tracks():
    query = request.args.get("query")
    matching_tracks = [track for track in tracks if query.lower() in track["title"].lower() or query.lower() in track["artist"].lower()]
    if matching_tracks:
        return jsonify(matching_tracks), 200
    else:
        return jsonify({"error": "No matching tracks found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
