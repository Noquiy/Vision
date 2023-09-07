from database import Database


class User:
    def __init__(self):
        self.db = Database()
        return
    
    def createNewUser(self, username, password):
        newUser = {
            "username": username,
            "password": password
        }
        self.db.users_collection.insert_one(newUser)
    
    def checkIfUserExists(self, username):
        if self.db.users_collection.find_one({ "username": f"{username}"}):
            return True
    
    def getUserPassword(self, username):
        userData = self.db.users_collection.find_one({ "username": f"{username}"})
        if userData:
            return userData["password"]
        
