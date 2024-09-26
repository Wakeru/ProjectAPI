from flask import Flask, request, jsonify

app = Flask(__name__) #initializing the API

@app.route("/get-user/<user_id>")
def get_user(user_id): #GET MOETHOD
    user_data = {
        "user_id": user_id,
        "name": "Jorge Doe",
        "email": "email@Example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra

    return jsonify(user_data), 200 #jsonify is for parsing it into a json file

@app.route("/create-user", methods = ["POST"]) #POST METHOD
def create_user():
    data = request.get_json()

    return jsonify(data), 201
 

if __name__ == "__main__": #runnin the API
    app.run(debug=True)