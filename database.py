from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from termcolor import colored

class Database:
    def __init__(self):
        load_dotenv()
        mongo_password = os.getenv("MONGO_DB_PASSWORD")  # Fetch the actual password from the environment variables
        mongo_username = os.getenv("MONGO_DB_USERNAME")
        uri = f"mongodb+srv://{mongo_username}:{mongo_password}@cloudetl.bsf0c4z.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['SaaS']
        self.users_collection = self.db['SaaS.UserAuth']
    
    def checkConnection(self):
        try:
            self.client.admin.command('ping')
            print(colored("Pinged your deployment. You successfully connected to MongoDB!", 'green', attrs = ['bold']))
        except Exception as e:
            print(colored(e, "red", attrs=['bold']))
            

    