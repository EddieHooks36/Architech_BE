import pymongo
import certifi


con_str = "mongodb+srv://jgarcia:3696@cluster0.sk2upyw.mongodb.net/?retryWrites=true&w=majority" 

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("Architechs")
users_collection = db.get_collection("Users")
bids_collection = db.get_collection("Bids")
bidders_collection = db.get_collection("Bidders")