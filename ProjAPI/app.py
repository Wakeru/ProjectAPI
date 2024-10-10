from flask import Flask
from routes.track_routes import track_blueprint

app = Flask(__name__)

# Register the blueprint from track_routes.py
app.register_blueprint(track_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
