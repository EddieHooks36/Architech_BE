from flask import Flask, abort, request
from config import db
import config
from bson import ObjectId
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

@app.get("/api/users")
def users():
    print(db.list_collection_names())
    users = db.Users.find()
    user_list = []
    for user in users:
        user_list.append(fix_id(user))
    return json.dumps(user_list)


app.run(debug=True)