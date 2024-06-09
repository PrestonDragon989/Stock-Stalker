from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from datetime import datetime

from database.user import *


URI = "mongodb+srv://Any:Stalker777@stalker.khes7qw.mongodb.net/?retryWrites=true&w=majority&appName=STALKER"

client = MongoClient(URI, server_api=ServerApi('1'))

connected = False
try:
    client.admin.command('ping')
    connected = True
    print("CONNECTED TO SERVER -- " + datetime.today().strftime("%Y-%m-%d, %H:%M:%S"))
except Exception as e:
    print(e)

database = client['user_data']

stock_data = database['stocks']
user_data = database['users']
request_data = database["account_requests"]
