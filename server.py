from flask import Flask, abort, request, jsonify, session
from config import db
import config, secrets
from bson import ObjectId
import json
from flask_cors import CORS, cross_origin
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app, origins="http://localhost:3000", supports_credentials=True)

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# to fix the ObjectId error
def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# to get all users
@app.get("/api/users")
def users():
    print(db.list_collection_names())
    users = db.Users.find()
    user_list = []
    for user in users:
        user_list.append(fix_id(user))
    return json.dumps(user_list)

# to get the total number of users
@app.get("/api/users/total")
def total_users():
    users = db.Users.find()
    user_list = []
    for user in users:
        user_list.append(fix_id(user))
    return json.dumps(len(user_list))

# to add a user
@app.post("/api/saveUsers")
def save_user():
    data = request.get_json()
    params = data['params']
    name = params['name']
    email = params['email']
    password = params['password']
    db.Users.insert_one({"name": name, "email": email, "password": password})
    return jsonify("User Added!")

# to verify a users email
@app.get("/api/users/verifyEmail/<email>")
def verify_email(email):
    verified = False
    check_email = db.Users.find_one({"email": email})
    if check_email:
        verified = True
    return json.dumps(verified)

# to verify a users email and password
@app.get("/api/users/verifyUser")
def verify_user():
    email = request.args.get('email')
    password = request.args.get('password')
    verified = False
    check = db.Users.find_one({"email": email, "password": password})
    if check:
        verified = True
        session['loggedInUser'] = fix_id(check)
    return json.dumps(verified)

# to get the logged in user
@app.get("/api/users/loggedInUser")
def get_logged_in_user():
    userLoggedIn = session.get('loggedInUser')
    print("loggedInUser is ", userLoggedIn)
    return jsonify(userLoggedIn)

# to log out the user
@app.post("/api/users/logout")
def logout():
    session.pop('loggedInUser', None)
    session.clear()
    session.modified = True
    print(session.get('loggedInUser'))
    return jsonify("Logged Out!")

# to find a user by name
@app.get("/api/users/find/<name>")
def find_user(name):
    users = db.Users.find({"name": name})
    user_list = []
    for user in users:
        user_list.append(fix_id(user))
    return json.dumps(user_list)

# to find user by id
@app.get("/api/users/findById/<id>")
def find_user_by_id(id):
    user = db.Users.find_one({"_id": ObjectId(id)})
    return json.dumps(fix_id(user))

# to change the requested user id
@app.get("/api/users/requestedUserId/<id>")
def change_requested_user_id(id):
    requestedUserId = id
    return requestedUserId

# to get the requested user id
@app.get("/api/users/requestedUserId")
def get_requested_user_id():
    requestedUserId = None
    return json.dumps(requestedUserId)

# to get all the bids
@app.get("/api/bids")
def bids():
    bids = db.Bids.find()
    bid_list = []
    for bid in bids:
        bid_list.append(fix_id(bid))
    return json.dumps(bid_list)

@app.get("/api/bids/bid/<id>")
def get_bid_by_id(id):
    bid = db.Bids.find_one({"_id": ObjectId(id)})
    return json.dumps(fix_id(bid))

# to get the total number of bids
@app.get("/api/bids/total")
def total_bids():
    bids = db.Bids.find()
    bid_list = []
    for bid in bids:
        bid_list.append(fix_id(bid))
    return json.dumps(len(bid_list))

# to add a bid
@app.post("/api/bids/saveBids")
def save_bid():
    data = request.get_json()
    params = data['params']
    originalPosterId = params['originalPosterId']
    name = params['name']
    description = params['description']
    bidAmount = params['bidAmount']
    image = params['bidImage']
    db.Bids.insert_one({"originalPosterId": originalPosterId, "name": name, "description": description, "bidAmount": bidAmount, "bidImage": image})
    return jsonify("Bid Added!")

@app.post("/api/bids/bidOnProject")
def bid_on_project():
    data = request.json
    params = data['params']
    bidId = params['bidId']
    bidderId = params['bidderId']
    bidderName = params['bidderName']
    bidAmount = params['bidAmount']
    bidDate = datetime.now().strftime("%m/%d/%Y %H:%M")
    db.Bidders.insert_one({"bidId": bidId, "bidderId": bidderId, "bidderName": bidderName, "bidAmount": bidAmount, "bidDate": bidDate})
    db.Bids.update_one(
        {"_id": ObjectId(bidId)},
          {"$set": {
                  "bidderId": bidderId,
                    "bidderName": bidderName,
                      "bidAmount": bidAmount,
                        "lastBidDate": bidDate}})
    return jsonify("Bid Added!")

# returns the current date/time
@app.get("/api/currentDateTime")
def current_date_time():
    currentDateTime = datetime.now().strftime("%m/%d/%Y %H:%M")
    return jsonify(currentDateTime)

        

app.run(debug=True)